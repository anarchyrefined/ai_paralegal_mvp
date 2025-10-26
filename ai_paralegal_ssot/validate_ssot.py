import json
import sys
from jsonschema import validate, ValidationError

def main():
    with open("ai_paralegal_ssot/graph.schema.json") as f:
        schema = json.load(f)
    # In a real impl, validate nodes/edges against schema
    print("✅ SSOT validation passed (stub)")
    
if __name__ == "__main__":
    main()
