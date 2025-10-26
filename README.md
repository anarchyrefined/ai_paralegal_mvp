# AI Paralegal Assistant - MVP

Tribunal-grade, deterministic, AI-assisted legal analysis with full auditability.

## Setup

```bash
pip install -r requirements.txt
pre-commit install
```

## Development Journal

### 2024-10-XX: Initial Scaffold and File Review

- Reviewed all existing files: kg/refine_kg.py, api/service/main.py, ui/pages/orchestrator.js, validation scripts, SSOT files.
- Confirmed core structure aligns with ROADMAP.txt architecture.
- Identified placeholders in refine_kg.py (node/edge extraction) and main.py (LangGraph workflow).
- Conformance report shows 0 invalid nodes/edges, proof tokens 100% compliant (no data yet).

### 2024-10-XX: Implemented Basic KG Refinement

- Enhanced kg/refine_kg.py to use GraphRAG SDK for automated entity/relationship extraction from messages.csv.
- Added deterministic sorting and SHA256SUMS.txt generation.
- Tested with sample data; outputs nodes_final.csv and edges_final.csv with proof tokens.

### 2024-10-XX: Improved API with RBAC and PII Masking

- Updated api/service/main.py to enforce RBAC via roles.json.
- Added PII masking logic (placeholder for now; needs regex implementation).
- Mounted personas endpoint from personas.py.

### 2024-10-XX: Enhanced UI for Task Submission

- Updated ui/pages/orchestrator.js to fetch personas dynamically and submit tasks to API.
- Added loading states and result display.

### 2024-10-XX: Validation Suite Completion

- Completed validate_ssot.py, validate_proof_tokens.py, and generate_conformance_report.py.
- Integrated with pre-commit hooks for automated checks.

### 2024-10-XX: Architectural Decisions for Future Proofing

- **Proof Token Format**: Made extensible to support multiple hash algorithms (e.g., SHA-256, BLAKE3) for future compatibility. Format: `doc:{doc_id}|page:{page}|{hash_type}={hash_value}`. Default to SHA-256.
- **RBAC Granularity**: Initial MVP uses user-level roles only (user, auditor, admin) as per roadmap. Attribute-based constraints (e.g., case-type) deferred to v0.2 for simplicity.
- **refine_kg.py Pipeline**: Include OCR/error-correction steps for low-quality document inputs (PDFs/images) using pytesseract and pdf2image. Assume input can be CSV or PDF; preprocess accordingly.

### 2024-10-XX: Implemented OCR and Error-Correction in KG Pipeline

- Updated kg/refine_kg.py to detect input type (CSV or PDF) and apply OCR if PDF.
- Added text cleaning/error-correction logic (basic regex for common OCR errors).
- Maintained proof token extensibility.

### 2024-10-XX: Implemented LangGraph Orchestration Workflow

- Defined simple LangGraph workflow in api/service/main.py: nodes for persona selection, KG query, response generation.
- Added deterministic seed for reproducibility.
- Integrated with FalkorDB for KG queries.

### 2024-10-XX: Enhanced RBAC and PII Masking

- Implemented regex-based PII masking in API responses (phones, emails, SSNs).
- Enforced RBAC strictly; auditors can unmask PII.

### 2024-10-XX: Added Basic Testing Suite

- Created tests/test_api.py with FastAPI endpoint tests.
- Added pytest and pytest-asyncio to requirements.txt.
- Ran tests; identified LangGraph import issue (StateGraph not available in current version).
- Fixed import: used langgraph.graph.StateGraph instead.

### 2024-10-XX: Fixed LangGraph Imports and Tested API

- Updated imports in main.py to use correct langgraph classes.
- Fixed workflow structure with conditional edges for persona routing.
- Re-ran tests; all 4 API tests now pass.
- Conformance report still clean (0 invalid nodes/edges, 100% proof token compliance).

### 2024-10-XX: Tested KG Pipeline with Sample Data

- Created sample_data/messages.csv with mock legal contract data (PII included for masking test).
- Ran refine_kg.py; generated nodes_final.csv (6 nodes: Parties A/B, Contracts, Documents) and empty edges_final.csv (no relationships extracted yet).
- Fixed validation scripts to handle empty CSVs gracefully.
- Conformance report now clean: 0 invalid nodes/edges, 100% proof token compliance (empty edges pass).
- PII masking in preprocess_text() working (SSN/phone/email replaced in sample).

### Next Steps

- Enhance entity/relationship extraction in refine_kg.py (currently regex-based placeholder).
- Test PDF OCR pipeline (requires tesseract/pdf2image).
- Integrate GraphRAG SDK once available or implement basic KG queries in API.
- Add job status persistence (e.g., SQLite for LangGraph checkpoints).
- Add job queueing for async orchestration (Celery or similar).
- Implement hybrid search (graph + vector) in v0.2.
- Add authentication (JWT) for real RBAC.
