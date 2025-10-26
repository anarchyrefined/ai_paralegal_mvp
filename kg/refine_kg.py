import pandas as pd
import hashlib
import json
import os
import re
# from graphrag_sdk import GraphRAG  # Placeholder - not available
# from graphrag_sdk.source import LocalSource
import pytesseract
from pdf2image import convert_from_path

def preprocess_text(text):
    # Basic error-correction for OCR errors
    text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '***-**-****', text)  # SSN masking
    text = re.sub(r'\b\d{3}-\d{3}-\d{4}\b', '***-***-****', text)  # Phone masking
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '***@***.***', text)  # Email masking
    # Common OCR fixes
    text = text.replace('l', '1').replace('O', '0').replace('I', '1')
    return text

def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img) + "\n"
    return text

def refine_kg(input_path="messages.csv"):
    # Detect input type
    if input_path.endswith('.pdf'):
        # OCR for PDF
        raw_text = extract_text_from_pdf(input_path)
        # Convert to CSV-like structure (assume page-based)
        lines = raw_text.split('\n')
        df = pd.DataFrame({
            'doc_id': [os.path.basename(input_path).replace('.pdf', '')] * len(lines),
            'page': list(range(1, len(lines) + 1)),
            'text': lines
        })
    else:
        # Assume CSV
        df = pd.read_csv(input_path)

    # Preprocess text
    df['text'] = df['text'].apply(preprocess_text)

    # Initialize GraphRAG with FalkorDB (placeholder)
    # grag = GraphRAG(
    #     llm="ollama/llama3.2",  # Offline LLM
    #     source=LocalSource(type="csv", file_path=input_path),
    #     vector_store="chromadb",
    #     graph_store="falkordb"
    # )

    # Build knowledge graph (placeholder)
    # grag.build()

    # Extract nodes and edges with proof tokens (extensible hash)
    nodes = []
    edges = []

    for idx, row in df.iterrows():
        doc_id = row['doc_id']
        page = row['page']
        text = row['text']
        # Extensible hash: default SHA-256, but allow others
        hash_type = "sha256"
        hash_value = hashlib.sha256(text.encode()).hexdigest()
        proof = f"doc:{doc_id}|page:{page}|{hash_type}={hash_value}"

        # Use GraphRAG to extract entities/relationships (placeholder)
        # entities = grag.extract_entities(text)  # Assume method exists
        # for entity in entities:
        #     nodes.append({"id": entity['id'], "type": entity['type'], "name": entity['name']})

        # relationships = grag.extract_relationships(text)
        # for rel in relationships:
        #     edges.append({"source": rel['source'], "target": rel['target'], "relationship": rel['type'], "proof": proof})

        # Basic entity extraction (regex-based placeholder)
        parties = re.findall(r'Party [A-Z]', text)
        for party in parties:
            nodes.append({"id": f"{party.lower()}_{doc_id}", "type": "Party", "name": party})

        contracts = re.findall(r'contract', text, re.IGNORECASE)
        if contracts:
            nodes.append({"id": f"contract_{doc_id}", "type": "Contract", "name": f"Contract {doc_id}"})

        # Basic relationships
        if parties and contracts:
            for party in parties:
                edges.append({"source": f"{party.lower()}_{doc_id}", "target": f"contract_{doc_id}", "relationship": "CONTRACTED_PARTY", "proof": proof})

        # Fallback: basic document node
        if not parties and not contracts:
            nodes.append({"id": f"doc_{doc_id}_p{page}", "type": "Document", "name": f"Document {doc_id} Page {page}"})

    # Sort deterministically
    nodes_df = pd.DataFrame(nodes)
    if not nodes_df.empty:
        nodes_df = nodes_df.sort_values(by=['id'])
    edges_df = pd.DataFrame(edges)
    if not edges_df.empty:
        edges_df = edges_df.sort_values(by=['source', 'target'])

    nodes_df.to_csv("kg/nodes_final.csv", index=False)
    edges_df.to_csv("kg/edges_final.csv", index=False)

    # Generate SHA256SUMS.txt
    with open("SHA256SUMS.txt", "w") as f:
        for file in ["kg/nodes_final.csv", "kg/edges_final.csv"]:
            with open(file, "rb") as fb:
                hash = hashlib.sha256(fb.read()).hexdigest()
            f.write(f"{hash}  {file}\n")

if __name__ == "__main__":
    import sys
    input_path = sys.argv[1] if len(sys.argv) > 1 else "messages.csv"
    refine_kg(input_path)
