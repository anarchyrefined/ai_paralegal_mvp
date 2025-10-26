import subprocess
import sys

def run_validation(script):
    try:
        result = subprocess.run([sys.executable, script], capture_output=True, text=True)
        return result.returncode == 0, result.stdout.strip()
    except Exception as e:
        return False, str(e)

def main():
    # Run SSOT validation
    ssot_ok, ssot_msg = run_validation("ai_paralegal_ssot/validate_ssot.py")
    invalid_nodes = 0 if ssot_ok else "N/A"  # Placeholder
    invalid_edges = 0 if ssot_ok else "N/A"

    # Run proof token validation
    proof_ok, proof_msg = run_validation("kg/validate_proof_tokens.py")
    proof_compliant = "100% compliant" if proof_ok else "Non-compliant"

    with open("conformance_report.md", "w") as f:
        f.write("# Conformance Report\n\n")
        f.write(f"- Invalid nodes: {invalid_nodes}\n")
        f.write(f"- Invalid edges: {invalid_edges}\n")
        f.write(f"- Proof tokens: {proof_compliant}\n")
        if not ssot_ok:
            f.write(f"\nSSOT Validation Error: {ssot_msg}\n")
        if not proof_ok:
            f.write(f"\nProof Token Validation Error: {proof_msg}\n")

    print("✅ conformance_report.md generated")

if __name__ == "__main__":
    main()
