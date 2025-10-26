import pandas as pd
import hashlib
import json
from graphrag_sdk import GraphRAG
from graphrag_sdk.source import LocalSource

def refine_kg():
    # Load input CSV
    df = pd.read_csv("messages.csv")

    # Initialize GraphRAG with FalkorDB
    grag = GraphRAG(
        llm="ollama/llama3.2",  # Offline LLM
        source=LocalSource(type="csv", file_path="messages.csv"),
        vector_store="chromadb",
        graph_store="falkordb"
    )

    # Build knowledge graph
    grag.build()

    # Extract nodes and edges with proof tokens
    nodes = []
    edges = []

    for idx, row in df.iterrows():
        doc_id = row['doc_id']
        page = row['page']
        text = row['text']
        sha256 = hashlib.sha256(text.encode()).hexdigest()
        proof = f"doc:{doc_id}|page:{page}|sha256={sha256}"

        # Placeholder for node/edge extraction (using GraphRAG SDK)
        # In real impl, parse entities and relationships from text
        nodes.append({"id": f"doc_{doc_id}_p{page}", "type": "Document", "name": f"Document {doc_id} Page {page}"})
        # Add more nodes based on extracted entities

        # Add edges with proof
        # Placeholder
        edges.append({"source": f"doc_{doc_id}_p{page}", "target": "some_target", "relationship": "PART_OF", "proof": proof})

    # Save outputs
    nodes_df = pd.DataFrame(nodes)
    edges_df = pd.DataFrame(edges)

    nodes_df.to_csv("kg/nodes_final.csv", index=False)
    edges_df.to_csv("kg/edges_final.csv", index=False)

    # Generate SHA256SUMS.txt
    with open("SHA256SUMS.txt", "w") as f:
        for file in ["kg/nodes_final.csv", "kg/edges_final.csv"]:
            with open(file, "rb") as fb:
                hash = hashlib.sha256(fb.read()).hexdigest()
            f.write(f"{hash}  {file}\n")

if __name__ == "__main__":
    refine_kg()
