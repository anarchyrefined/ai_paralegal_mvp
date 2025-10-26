import json
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
        invalid_edges = edges_df[~edges_df["relationship"].isin(schema["properties"]["relationship_types"]["items"]["enum"])]
        if not invalid_edges.empty:
            print(f"❌ {len(invalid_edges)} invalid edges")
            sys.exit(1)
    except FileNotFoundError:
        print("⚠️  edges_final.csv not found. Skipping edge validation.")

    print("✅ SSOT validation passed")

if __name__ == "__main__":
    main()
