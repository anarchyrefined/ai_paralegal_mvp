# Knowledge Graph Derivation Rules

## Entity Extraction
- If text contains a person's name + title (e.g., "John Doe, CEO"), create `Party` node.
- If text references a law (e.g., "pursuant to 18 U.S.C. § 242"), create `Statute` node.

## Relationship Extraction
- If snippet contains "fired for [reason]", create edge with `relationship: "ALLEGED_MISCONDUCT"`.
- If contract mentions "Party A agrees to pay Party B", create `CONTRACTED_PARTY` edge.

## Proof Token Format
Every edge must include:
`proof: "doc:{doc_id}|page:{page_number}|sha256={sha256(text_snippet)}"`
