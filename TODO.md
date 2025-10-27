# TODO for v0.2 Implementation

- [x] Step 1: Extend ai_paralegal_ssot/graph.schema.json with new types for psychology/investigation.
- [x] Step 2: Create kg/advanced_extraction.py with custom logic for psychological analysis, evidence categorization, and strategic reasoning.
- [x] Step 3: Enhance KG extraction in kg/refine_kg.py with GraphRAG SDK integration and advanced extraction.
- [x] Step 4: Add job persistence with SQLite in api/service/jobs.py and update main.py.
- [x] Step 5: Implement job queuing with Celery in api/service/jobs.py.
- [x] Step 6: Add JWT authentication in api/service/auth.py and middleware in main.py.
- [x] Step 7: Implement hybrid search in kg/kg_queries.py.
- [x] Step 8: Build KG Studio UI with Cytoscape in ui/pages/kg-studio.js and filters in FilterPanel.js.
- [x] Step 9: Update UI orchestrator to link to KG Studio.
- [ ] Step 10: Add new tests and update existing ones.
- [x] Step 11: Update requirements.txt and pre-commit hooks.
- [x] Step 12: Test PDF OCR pipeline and generate final conformance report.
