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
from langgraph.graph import StateGraph, END  # Actual LangGraph
from langgraph.checkpoint.memory import MemorySaver
from .personas import app as personas_app
# from graphrag_sdk import GraphRAG  # For KG queries - commented out for testing

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

# Initialize GraphRAG for KG queries (placeholder)
# grag = GraphRAG(
#     llm="ollama/llama3.2",
#     graph_store="falkordb"
# )

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
    # Query KG using GraphRAG (placeholder)
    # results = grag.query(task)  # Assume query method
    results = "Mock KG results for task: " + task  # Placeholder
    state["kg_results"] = results
    return state

def generate_response(state):
    persona = state["persona"]
    kg_results = state["kg_results"]
    # Generate response based on persona
    response = f"Persona {persona}: {kg_results}"  # Placeholder
    state["response"] = response
    return state

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

# Deterministic checkpoint
checkpointer = MemorySaver()

graph = workflow.compile(checkpointer=checkpointer)

def run_langgraph_workflow(task: str, persona: str):
    # Run with deterministic seed (implicit via checkpointer)
    config = {"configurable": {"thread_id": "test_thread"}}  # For testing
    result = graph.invoke({"task": task, "persona": persona}, config=config)
    job_id = str(uuid.uuid4())
    return {"job_id": job_id, "status": "completed", "result": result["response"]}

def mask_pii(text: str):
    # Regex-based PII masking
    text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '***-**-****', text)  # SSN
    text = re.sub(r'\b\d{3}-\d{3}-\d{4}\b', '***-***-****', text)  # Phone
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '***@***.***', text)  # Email
    return text

@app.post("/orchestrate/run")
async def run_orchestration(task_request: TaskRequest, pii_mask: bool = Query(True)):
    # Validate persona
    persona_names = [p["name"] for p in personas]
    if task_request.persona not in persona_names:
        raise HTTPException(status_code=400, detail="Invalid persona")

    # RBAC check (mock: assume auditor role for tests; in real, from JWT)
    user_role = "auditor"  # TODO: Extract from auth
    role_perms = next((r["permissions"] for r in roles if r["role"] == user_role), [])
    if "write" not in role_perms:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    # Start LangGraph workflow
    result = run_langgraph_workflow(task_request.task, task_request.persona)

    # PII masking
    if pii_mask and "pii_unmask" not in role_perms:
        result["result"] = mask_pii(result["result"])

    status_url = f"/jobs/{result['job_id']}"

    return {"job_id": result["job_id"], "status_url": status_url}

@app.get("/jobs/{job_id}")
async def get_job_status(job_id: str, pii_mask: bool = Query(True)):
    # Mock: in real, retrieve from DB
    result = "Completed analysis with proof tokens: doc:123|page:1|sha256=abc123..."
    if pii_mask:
        result = mask_pii(result)
    return {"job_id": job_id, "status": "completed", "result": result}
