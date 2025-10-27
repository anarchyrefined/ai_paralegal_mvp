# Implementation Plan

Implement v0.2 of the AI Paralegal MVP, enhancing the knowledge graph with advanced extraction incorporating strategic reasoning, psychological analysis, and investigative principles, adding persistence and queuing for orchestration, implementing hybrid search, and building a KG Studio UI with Cytoscape visualization and filters.

This plan builds on the existing v0.1 foundation, which includes basic KG refinement, LangGraph orchestration, FastAPI with RBAC, and PII masking. The implementation focuses on integrating GraphRAG SDK with advanced entity/relationship extraction using first principles of criminal/business psychology, Bloom's taxonomy, neurolinguistic programming, predictive analytics, evidence categorization, and lawyer communication skills for deeper context understanding. Additional features include job persistence and queuing for scalability, hybrid graph-vector search, and a visual KG Studio interface. All changes maintain the core principles of determinism, auditability, and offline capability, with guardrails for proof tokens and SSOT conformance enforced throughout.

[Types]
Extend existing schemas in ai_paralegal_ssot/graph.schema.json to include new node types for psychological and investigative elements (e.g., Motive, Context, EvidenceCategory, PsychologicalProfile). Add relationship types for strategic connections (e.g., Influences, Predicts, CommunicatesVia). Extend edge proof token pattern to support additional hash types (e.g., BLAKE3) and include metadata for reasoning depth (e.g., Bloom's level, NLP patterns).

[Files]
New files: kg/kg_queries.py (hybrid search implementation), api/service/auth.py (JWT authentication), api/service/jobs.py (job persistence and queuing), ui/pages/kg-studio.js (Cytoscape visualization), ui/components/FilterPanel.js (UI filters), scripts/setup_db.py (SQLite setup), tests/test_kg_studio.py (UI tests), tests/test_auth.py (auth tests), tests/test_jobs.py (job persistence tests), kg/advanced_extraction.py (custom extraction logic for psychology/investigation). Existing files modified: kg/refine_kg.py (integrate GraphRAG SDK with advanced extraction), api/service/main.py (add auth middleware, job endpoints), ui/pages/orchestrator.js (add KG Studio link), requirements.txt (add new dependencies), .pre-commit-config.yaml (add new hooks), ai_paralegal_ssot/graph.schema.json (extend schemas).

[Functions]
New functions: kg_queries.hybrid_search(query, graph_store, vector_store) in kg/kg_queries.py, auth.authenticate_user(token) in api/service/auth.py, jobs.create_job(task, persona) and jobs.get_job_status(job_id) in api/service/jobs.py, FilterPanel.apply_filters(nodes, edges, criteria) in ui/components/FilterPanel.js, advanced_extraction.analyze_psychology(text) and advanced_extraction.categorize_evidence(text) in kg/advanced_extraction.py. Modified functions: refine_kg.refine_kg() in kg/refine_kg.py to use GraphRAG SDK with custom advanced extraction, main.run_langgraph_workflow() in api/service/main.py to persist checkpoints in SQLite, main.run_orchestration() in api/service/main.py to require JWT auth.

[Classes]
New classes: KGStudio (React component for Cytoscape rendering in ui/pages/kg-studio.js), JobQueue (Celery-based class in api/service/jobs.py for async task handling), HybridSearch (class in kg/kg_queries.py combining graph and vector queries), AdvancedExtractor (class in kg/advanced_extraction.py for psychological/investigative analysis). No modifications to existing classes.

[Dependencies]
New packages: graphrag-sdk (for KG extraction), celery (job queuing), redis (Celery broker), sqlite3 (persistence), cytoscape (UI visualization), cytoscape-cose-bilkent (layout), pyjwt (authentication), chromadb (vector store integration), nltk (NLP for psychology analysis), scikit-learn (predictive analytics). Update graphrag-sdk[all] to latest if available.

[Testing]
Add test files: tests/test_kg_studio.py (unit tests for KG queries and hybrid search), tests/test_auth.py (JWT auth validation), tests/test_jobs.py (job persistence and queuing), tests/test_advanced_extraction.py (unit tests for psychological analysis). Modify tests/test_api.py to include auth headers in requests. Use pytest fixtures for mock GraphRAG and Celery. Validate conformance report after each KG change, including new schema validations.

[Implementation Order]

1. Extend ai_paralegal_ssot/graph.schema.json with new types for psychology/investigation.
2. Create kg/advanced_extraction.py with custom logic for psychological analysis, evidence categorization, and strategic reasoning.
3. Enhance KG extraction in kg/refine_kg.py with GraphRAG SDK integration and advanced extraction.
4. Add job persistence with SQLite in api/service/jobs.py and update main.py.
5. Implement job queuing with Celery in api/service/jobs.py.
6. Add JWT authentication in api/service/auth.py and middleware in main.py.
7. Implement hybrid search in kg/kg_queries.py.
8. Build KG Studio UI with Cytoscape in ui/pages/kg-studio.js and filters in FilterPanel.js.
9. Update UI orchestrator to link to KG Studio.
10. Add new tests and update existing ones.
11. Update requirements.txt and pre-commit hooks.
12. Test PDF OCR pipeline and generate final conformance report.
