import pandas as pd
import hashlib
import json
import os
import re
import logging
from graphrag_sdk import GraphRAG
from graphrag_sdk.source import LocalSource
import chromadb
import pytesseract
from pdf2image import convert_from_path
from advanced_extraction import AdvancedExtractor

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
    logger.info(f"Starting KG refinement for input: {input_path}")
    # Detect input type
    if input_path.endswith('.pdf'):
        logger.info("Detected PDF input, performing OCR")
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
        logger.info("Detected CSV input")
        # Assume CSV
        df = pd.read_csv(input_path)

    # Preprocess text
    logger.info("Preprocessing text for PII masking and error correction")
    df['text'] = df['text'].apply(preprocess_text)

    # Initialize ChromaDB for vector store
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    vector_store = chroma_client.get_or_create_collection(name="legal_docs")

    # Initialize GraphRAG with FalkorDB
    grag = GraphRAG(
        llm="ollama/llama3.2",  # Offline LLM
        source=LocalSource(type="csv", file_path=input_path),
        vector_store=vector_store,
        graph_store="falkordb"
    )

    # Build knowledge graph
    grag.build()

    # Initialize advanced extractor for psychological/investigative analysis
    advanced_extractor = AdvancedExtractor()

    # Extract nodes and edges with proof tokens (extensible hash)
    logger.info("Extracting nodes and edges from text")
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

        # Advanced psychological and investigative analysis
        psych_analysis = advanced_extractor.analyze_psychology(text)
        evidence_cats = advanced_extractor.categorize_evidence(text)
        strategic_reasoning = advanced_extractor.strategic_reasoning(text)

        # Use GraphRAG to extract entities/relationships
        entities = grag.extract_entities(text)
        for entity in entities:
            node_id = f"{entity['type'].lower()}_{entity['id']}_{doc_id}"
            if not any(n['id'] == node_id for n in nodes):
                nodes.append({"id": node_id, "type": entity['type'], "name": entity['name']})
                logger.debug(f"Added node: {node_id}")

        relationships = grag.extract_relationships(text)
        for rel in relationships:
            source = f"{rel['source_type'].lower()}_{rel['source']}_{doc_id}"
            target = f"{rel['target_type'].lower()}_{rel['target']}_{doc_id}"
            if not any(e['source'] == source and e['target'] == target for e in edges):
                edges.append({"source": source, "target": target, "relationship": rel['type'], "proof": proof})
                logger.debug(f"Added edge: {source} -> {target}")

        # Enhanced entity extraction with psychological insights
        parties = re.findall(r'Party [A-Z]', text)
        for party in parties:
            node_id = f"{party.lower()}_{doc_id}"
            if not any(n['id'] == node_id for n in nodes):  # Avoid duplicates
                nodes.append({"id": node_id, "type": "Party", "name": party})
                logger.debug(f"Added node: {node_id}")

        contracts = re.findall(r'contract', text, re.IGNORECASE)
        if contracts:
            node_id = f"contract_{doc_id}"
            if not any(n['id'] == node_id for n in nodes):
                nodes.append({"id": node_id, "type": "Contract", "name": f"Contract {doc_id}"})
                logger.debug(f"Added node: {node_id}")

        # Add psychological and investigative nodes
        if psych_analysis['motive_indicators']:
            for motive, count in psych_analysis['motive_indicators'].items():
                if count > 0:
                    node_id = f"motive_{motive}_{doc_id}_p{page}"
                    if not any(n['id'] == node_id for n in nodes):
                        nodes.append({"id": node_id, "type": "Motive", "name": motive.replace('_', ' ').title()})
                        logger.debug(f"Added motive node: {node_id}")

        if psych_analysis['communication_style']['dominant'] != 'assertive':
            node_id = f"comm_style_{psych_analysis['communication_style']['dominant']}_{doc_id}_p{page}"
            if not any(n['id'] == node_id for n in nodes):
                nodes.append({"id": node_id, "type": "CommunicationStyle", "name": psych_analysis['communication_style']['dominant'].title()})
                logger.debug(f"Added communication style node: {node_id}")

        if strategic_reasoning['risk_assessment']['level'] != 'low':
            node_id = f"context_risk_{strategic_reasoning['risk_assessment']['level']}_{doc_id}_p{page}"
            if not any(n['id'] == node_id for n in nodes):
                nodes.append({"id": node_id, "type": "Context", "name": f"Risk Level: {strategic_reasoning['risk_assessment']['level'].title()}"})
                logger.debug(f"Added context node: {node_id}")

        # Enhanced relationships with strategic connections
        if parties and contracts:
            for party in parties:
                source = f"{party.lower()}_{doc_id}"
                target = f"contract_{doc_id}"
                if not any(e['source'] == source and e['target'] == target for e in edges):  # Avoid duplicates
                    edges.append({"source": source, "target": target, "relationship": "CONTRACTED_PARTY", "proof": proof})
                    logger.debug(f"Added edge: {source} -> {target}")

        # Add psychological and strategic relationships
        for motive, count in psych_analysis['motive_indicators'].items():
            if count > 0:
                for party in parties:
                    source = f"{party.lower()}_{doc_id}"
                    target = f"motive_{motive}_{doc_id}_p{page}"
                    if not any(e['source'] == source and e['target'] == target for e in edges):
                        edges.append({"source": source, "target": target, "relationship": "INFLUENCES", "proof": proof})
                        logger.debug(f"Added psychological edge: {source} -> {target}")

        if psych_analysis['communication_style']['dominant'] != 'assertive':
            for party in parties:
                source = f"{party.lower()}_{doc_id}"
                target = f"comm_style_{psych_analysis['communication_style']['dominant']}_{doc_id}_p{page}"
                if not any(e['source'] == source and e['target'] == target for e in edges):
                    edges.append({"source": source, "target": target, "relationship": "COMMUNICATES_VIA", "proof": proof})
                    logger.debug(f"Added communication edge: {source} -> {target}")

        # Strategic relationships from reasoning
        for rel in strategic_reasoning['relationships']:
            source = f"{rel['party1'].lower()}_{doc_id}"
            target = f"{rel['party2'].lower()}_{doc_id}"
            if not any(e['source'] == source and e['target'] == target for e in edges):
                edges.append({"source": source, "target": target, "relationship": rel['type'], "proof": proof})
                logger.debug(f"Added strategic edge: {source} -> {target}")

        # Fallback: basic document node
        if not parties and not contracts:
            node_id = f"doc_{doc_id}_p{page}"
            if not any(n['id'] == node_id for n in nodes):
                nodes.append({"id": node_id, "type": "Document", "name": f"Document {doc_id} Page {page}"})
                logger.debug(f"Added node: {node_id}")

    # Sort deterministically
    logger.info("Sorting nodes and edges deterministically")
    nodes_df = pd.DataFrame(nodes)
    if not nodes_df.empty:
        nodes_df = nodes_df.sort_values(by=['id'])
    edges_df = pd.DataFrame(edges)
    if not edges_df.empty:
        edges_df = edges_df.sort_values(by=['source', 'target'])

    logger.info(f"Writing {len(nodes_df)} nodes to kg/nodes_final.csv")
    nodes_df.to_csv("kg/nodes_final.csv", index=False)
    logger.info(f"Writing {len(edges_df)} edges to kg/edges_final.csv")
    edges_df.to_csv("kg/edges_final.csv", index=False)

    # Generate SHA256SUMS.txt
    logger.info("Generating SHA256SUMS.txt for integrity")
    with open("SHA256SUMS.txt", "w") as f:
        for file in ["kg/nodes_final.csv", "kg/edges_final.csv"]:
            with open(file, "rb") as fb:
                hash = hashlib.sha256(fb.read()).hexdigest()
            f.write(f"{hash}  {file}\n")
    logger.info("KG refinement completed successfully")

if __name__ == "__main__":
    import sys
    input_path = sys.argv[1] if len(sys.argv) > 1 else "messages.csv"
    refine_kg(input_path)
