# UI Design Prompt for AI Paralegal Assistant MVP

Based on my analysis of the application files, here's a comprehensive prompt you can use in ChatGPT to generate a UI design blueprint for your AI Paralegal Assistant MVP. This prompt incorporates the app's core features, existing UI structure, personas, knowledge graph schema, and architectural details to ensure the design aligns with the tribunal-grade legal analysis focus.

---

**ChatGPT Prompt:**

"Design a comprehensive UI blueprint for an AI Paralegal Assistant MVP application. This is a tribunal-grade, deterministic AI-assisted legal analysis tool with full auditability, built for offline operation. The app focuses on legal document analysis, knowledge graph exploration, and task orchestration using specialized AI personas.

Key app features and components:

- **Purpose**: Submit legal analysis tasks to AI personas that query a knowledge graph (KG) built from legal documents. Ensure deterministic, auditable workflows with PII masking and RBAC.
- **Tech Stack**: Frontend in Next.js/React, backend in FastAPI with LangGraph orchestration, KG powered by GraphRAG-SDK and FalkorDB, vector store in ChromaDB. UI includes Cytoscape for graph visualization.
- **Main Pages/Screens**:
  1. **Orchestrator Page**: Task submission interface. Includes a form with:
     - Textarea for task description (e.g., 'Analyze contract disputes involving Party A and Party B').
     - Dropdown to select AI persona (fetched from API).
     - Submit button with loading state.
     - Result display: Job ID, status URL link, success message.
     - Link to KG Studio.
     - Styling: Clean, professional, with padding, borders, and responsive design.
  2. **KG Studio Page**: Knowledge graph visualization and exploration.
     - Statistics panel: Total nodes, edges, average connections.
     - Search bar: Input for querying the KG.
     - Advanced filters panel: Dropdowns/inputs for node types (e.g., Party, Contract, Document, Motive, Context, PsychologicalProfile, etc.), relationships (e.g., PART_OF, ALLEGED_MISCONDUCT, PSYCHOLOGICAL_LINK), and text filters for motives/contexts.
     - Cytoscape graph container: Interactive visualization with nodes colored by type (e.g., party: red, contract: teal), edges with labels and proof tokens. Click nodes to highlight connections.
     - Instructions section: Tips on interaction (click nodes, use filters, search).
- **AI Personas** (from personas.json):
  - LegalAnalyst: Analyzes documents for key facts, parties, claims.
  - ComplianceOfficer: Reviews for regulatory adherence.
  - RedTeamAnalyst: Challenges conclusions for weaknesses/biases.
- **Knowledge Graph Schema** (from graph.schema.json):
  - Node Types: Document, Party, Contract, Statute, Event, Location, Motive, Context, EvidenceCategory, PsychologicalProfile, CommunicationStyle, PredictiveIndicator.
  - Relationship Types: PART_OF, CONTRACTED_PARTY, REFERRED_TO_STATUTE, OCCURRED_AT_LOCATION, ALLEGED_MISCONDUCT, INFLUENCES, PREDICTS, COMMUNICATES_VIA, EVIDENCE_OF, PSYCHOLOGICAL_LINK, STRATEGIC_CONNECTION.
  - Includes proof tokens for auditability (e.g., doc:ID|page:X|sha256=HASH).
- **Design Principles**:
  - Professional, legal/tribunal aesthetic: Neutral colors (blues, grays), clean typography, high contrast for accessibility.
  - Responsive: Mobile-friendly, tablet/desktop optimized.
  - User Roles: Support user, auditor, admin (auditors can unmask PII).
  - Auditability: Show proof tokens, job statuses, deterministic outputs.
  - Offline-Capable: No reliance on external web calls in UI.
- **Additional Context**:
  - Roadmap: v0.1 focuses on KG pipeline and orchestration; v0.2 adds KG Studio and filters.
  - Existing UI: Basic inline styles in React components; expand to a full design system.
  - Target Users: Legal professionals, tribunals; emphasize trust, verifiability.

Create a detailed blueprint including:

- Wireframes or mockups for each page/screen (describe layouts, components, interactions in text or simple ASCII art).
- Color scheme, typography, iconography suggestions.
- Navigation flow between pages.
- Accessibility considerations (e.g., screen reader support, keyboard navigation).
- Mobile responsiveness details.
- How to integrate advanced features like graph filtering, search results highlighting.
- Suggestions for branding (e.g., logo, tagline like 'Tribunal-Grade AI Legal Analysis').

Ensure the design is scalable for future features like job queues, hybrid search, and full audit trails. Base the blueprint on modern UI/UX best practices for enterprise legal tools."
