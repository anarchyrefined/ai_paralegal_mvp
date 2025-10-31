Prompt Title: Build, Test, and Document the Tribunal-Grade AI Paralegal Assistant MVP

Objective:

Develop a fully functional MVP for a tribunal-grade AI Paralegal Assistant based on the ROADMAP.txt blueprint. The system must be deterministic, auditable, offline-capable, and verifiable through proof tokens. Prioritize low-to-no-code methods using AI-native tools, ensuring all components integrate seamlessly. After building, conduct thorough testing (including critical-path and edge-case scenarios), then produce effective documentation and journaling for the project.

Key Constraints and Principles:

Determinism and Auditability: Use LangGraph for explicit graph-based workflows with checkpointing and HITL support. Every decision must be traceable via proof tokens (format: doc:{doc_id}|page:{page}|sha256={sha256(text_snippet)}).
Offline Capability: No external web calls by default; rely on local LLMs (e.g., via Ollama), FalkorDB, and ChromaDB.
Modularity: Follow the exact file structure in ROADMAP.txt. Validate against ai_paralegal_ssot/graph.schema.json and personas.json.
Guardrails: Enforce PII masking in UI/API outputs (unless ?pii_mask=false for auditors). Generate SHA256SUMS.txt for deterministic sorting. Fail builds on non-conformance.
AI-Assisted Development: Leverage .ai-context/ files (project.schema.json, persona_templates.yaml, kg_rules.md) for consistent code generation.
Testing Scope: Include unit tests, integration tests, and end-to-end validation. Simulate offline environments.
Documentation: Produce runbooks, API docs, and a project journal with build logs, test results, and audit trails.
Step-by-Step Build Plan:

Setup Environment and Dependencies:

Install requirements from requirements.txt (LangGraph, GraphRAG-SDK, FalkorDB, ChromaDB, FastAPI, etc.).
Set up pre-commit hooks via .pre-commit-config.yaml for linting and validation.
Initialize FalkorDB and ChromaDB locally. Ensure Ollama is configured for offline LLMs.
Validate SSOT: Run ai_paralegal_ssot/validate_ssot.py to confirm personas.json and graph.schema.json compliance.
Implement Core Components:

Knowledge Graph (kg/):
Enhance kg/refine_kg.py to process messages.csv (columns: doc_id, page, text) into nodes_final.csv (id, type, name) and edges_final.csv (source, target, relationship, proof).
Integrate GraphRAG-SDK with FalkorDB for automated ontology creation and multi-hop reasoning.
Add kg/validate_proof_tokens.py to regex-validate proof tokens on all edges.
API Service (api/service/):
Build api/service/main.py as a FastAPI app with RBAC (using roles.json). Implement POST /orchestrate/run endpoint: Accepts {task, persona}, returns job_id and status_url.
Add PII masking middleware.
Integrate personas from api/service/personas.py (load from ai_paralegal_ssot/personas.json).
Orchestration (LangGraph):
Create a LangGraph workflow in a new file (e.g., orchestration/workflow.py) for task execution with personas (e.g., LegalAnalyst). Include HITL nodes for human review.
Connect to KG and vector store for retrieval.
UI (ui/pages/):
Develop ui/pages/orchestrator.js as a simple web interface for task input and persona selection. Use vanilla JS/HTML for offline compatibility.
Scripts and Validation:
Implement scripts/generate_conformance_report.py to output conformance_report.md (invalid nodes/edges, proof compliance).
Ensure CI in .github/workflows/ runs validation on pushes/PRs.
Integration and Bootstrapping:

Wire components: API calls orchestration, which queries KG/vector store.
Add offline LLM integration (e.g., load models via Ollama).
Generate initial KG from sample data (create a sample messages.csv if needed).
Testing Plan:

Unit Tests: Test individual functions (e.g., proof token validation, KG refinement). Use pytest.
Integration Tests: Validate KG pipeline (input CSV → output CSVs), API endpoints (curl requests for /orchestrate/run), and orchestration flow.
End-to-End Tests: Simulate full workflows (e.g., submit task via UI, verify response with proof tokens). Test offline mode (disconnect internet).
Edge Cases: Invalid inputs, PII detection, schema violations.
Performance: Benchmark KG queries and API response times.
Auditability: Verify checkpoints, logs, and proof tokens in outputs.
Run generate_conformance_report.py post-tests; ensure 0 invalid items.
Documentation and Journaling:

Runbooks (docs/runbooks/): Create setup.md (environment install), audit.md (traceability checks), offline_operation.md (Ollama usage).
API Docs: Auto-generate from FastAPI (e.g., via Swagger). Document endpoints, auth, and PII flags.
Project Journal: Maintain a journal.md with:
Build logs (steps taken, issues resolved).
Test results (pass/fail, coverage metrics).
Audit trail (proof tokens verified, conformance reports).
Lessons learned (e.g., LangGraph HITL benefits).
Version history aligned with roadmap (v0.1 core, v0.2 UI, v0.3 deployment).
Update README.md with usage examples, architecture overview, and deployment instructions.
Final Validation:

Run full CI pipeline locally.
Confirm offline operation (no external calls).
Output: Functional MVP, test reports, and complete docs/journal.
AI Context Files:

Reference .ai-context/project.schema.json for schema adherence, persona_templates.yaml for agent rules, and kg_rules.md for graph logic. Generate code that matches these specs exactly.import json
import sys
import pandas as pd
from jsonschema import validate, ValidationError

def main():
    # Validate graph schema
    with open("ai_paralegal_ssot/graph.schema.json") as f:
        schema = json.load(f)

    # Validate nodes
    try:
        nodes_df = pd.read_csv("kg/nodes_final.csv")
        invalid_nodes = nodes_df[~nodes_df["type"].isin(schema["properties"]["node_types"]["items"]["enum"])]
        if not invalid_nodes.empty:
            print(f"❌ {len(invalid_nodes)} invalid nodes")
            sys.exit(1)
    except FileNotFoundError:
        print("⚠️  nodes_final.csv not found. Skipping node validation.")

    # Validate edges
    try:
        edges_df = pd.read_csv("kg/edges_final.csv")
        if not edges_df.empty:
            invalid_edges = edges_df[~edges_df["relationship"].isin(schema["properties"]["relationship_types"]["items"]["enum"])]
            if not invalid_edges.empty:
                print(f"❌ {len(invalid_edges)} invalid edges")
                sys.exit(1)
    except FileNotFoundError:
        print("⚠️  edges_final.csv not found. Skipping edge validation.")
    except pd.errors.EmptyDataError:
        print("⚠️  edges_final.csv is empty. Skipping edge validation.")

    print("✅ SSOT validation passed")

if __name__ == "__main__":
    main()
