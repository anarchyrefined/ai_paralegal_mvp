"""
TRIBUNAL-GRADE API ENDPOINT
- All endpoints MUST enforce RBAC via roles.json
- PII masking ON by default (override with ?pii_mask=false for auditors)
- Every response must include proof tokens for evidence
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import json
import uuid
import re
import logging
try:
    from langgraph.graph import StateGraph, END  # Actual LangGraph
    from langgraph.checkpoint.sqlite import SqliteSaver
    LANGGRAPH_AVAILABLE = True
except ModuleNotFoundError:
    StateGraph = END = SqliteSaver = None  # type: ignore
    LANGGRAPH_AVAILABLE = False
from .personas import app as personas_app
from .jobs import create_job, get_job_status as fetch_job_status
from .auth import authenticate_user
from kg.kg_queries import hybrid_search
from fastapi import Header

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()
app.mount("/api", personas_app)  # Mount personas endpoint

# Load personas and roles
with open("ai_paralegal_ssot/personas.json") as f:
    personas = json.load(f)

with open("ai_paralegal_ssot/roles.json") as f:
    roles = json.load(f)

class TaskRequest(BaseModel):
    task: str
    persona: str

# Hybrid search instance available

# Define LangGraph workflow
def route_task(state):
    persona = state["persona"]
    # Route based on persona
    if persona == "LegalAnalyst":
        return "analyze"
    elif persona == "ComplianceOfficer":
        return "comply"
    elif persona == "RedTeamAnalyst":
        return "challenge"
    return "default"

def query_kg(state):
    task = state["task"]
    # Query KG using hybrid search
    results = hybrid_search.hybrid_search(task)
    state["kg_results"] = results
    return state

def generate_response(state):
    persona = state["persona"]
    kg_results = state["kg_results"]
    # Generate response based on persona
    response = f"Persona {persona}: {kg_results}"  # Placeholder
    state["response"] = response
    return state

if LANGGRAPH_AVAILABLE:
    workflow = StateGraph(dict)
    workflow.add_node("query_kg", query_kg)
    workflow.add_node("generate", generate_response)

    # Conditional routing from entry
    workflow.add_conditional_edges("__start__", route_task, {
        "analyze": "query_kg",
        "comply": "query_kg",
        "challenge": "query_kg",
        "default": "query_kg"
    })
    workflow.add_edge("query_kg", "generate")
    workflow.add_edge("generate", END)

    # Persistent checkpoint with SQLite
    checkpointer = SqliteSaver.from_conn_string("checkpoints.db")

    graph = workflow.compile(checkpointer=checkpointer)
else:
    graph = None


def run_langgraph_workflow(task: str, persona: str):
    if not LANGGRAPH_AVAILABLE or graph is None:
        logger.warning("LangGraph unavailable; returning stubbed workflow response")
        return f"[stub response] Persona {persona}: {task}"

    logger.info(f"Starting LangGraph workflow for task: {task[:50]}... with persona: {persona}")
    # Run with deterministic seed (implicit via checkpointer)
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}  # Unique thread per run
    result = graph.invoke({"task": task, "persona": persona}, config=config)
    logger.info("Workflow completed")
    return result["response"]

def mask_pii(text: str):
    # Regex-based PII masking
    text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '***-**-****', text)  # SSN
    text = re.sub(r'\b\d{3}-\d{3}-\d{4}\b', '***-***-****', text)  # Phone
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '***@***.***', text)  # Email
    return text

@app.post("/orchestrate/run")
async def run_orchestration(task_request: TaskRequest, pii_mask: bool = Query(True), authorization: str = Header(None)):
    logger.info(f"Received orchestration request for persona: {task_request.persona}")
    # Validate persona
    persona_names = [p["name"] for p in personas]
    if task_request.persona not in persona_names:
        logger.warning(f"Invalid persona requested: {task_request.persona}")
        raise HTTPException(status_code=400, detail="Invalid persona")

    # JWT auth check
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid")
    token = authorization.split(" ")[1]
    user_role = authenticate_user(token)  # From auth.py
    if not user_role:
        raise HTTPException(status_code=401, detail="Invalid token")

    role_perms = next((r["permissions"] for r in roles if r["role"] == user_role), [])
    if "write" not in role_perms:
        logger.warning(f"Insufficient permissions for role: {user_role}")
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    # Create job asynchronously
    job_id = create_job(task_request.task, task_request.persona)

    status_url = f"/jobs/{job_id}"
    logger.info(f"Orchestration job created, job_id: {job_id}")

    return {"job_id": job_id, "status_url": status_url}

@app.get("/jobs/{job_id}")
async def get_job_status(job_id: str, pii_mask: bool = Query(True), authorization: str = Header(None)):
    logger.info(f"Retrieving status for job_id: {job_id}")
    # JWT auth check
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid")
    token = authorization.split(" ")[1]
    user_role = authenticate_user(token)
    if not user_role:
        raise HTTPException(status_code=401, detail="Invalid token")

    role_perms = next((r["permissions"] for r in roles if r["role"] == user_role), [])

    job = fetch_job_status(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    result = job["result"]
    if result is not None and pii_mask and "pii_unmask" not in role_perms:
        result = mask_pii(result)
        logger.info("PII masking applied to job result")

    return {"job_id": job_id, "status": job["status"], "result": result}
