import pytest
from fastapi.testclient import TestClient
from api.service.main import app
from api.service.auth import create_access_token

client = TestClient(app)

def test_get_personas():
    response = client.get("/personas")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_personas_with_auth():
    token = create_access_token({"sub": "test_user", "role": "user"})
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/personas", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_run_orchestration_requires_auth():
    payload = {"task": "Analyze contract", "persona": "LegalAnalyst"}
    response = client.post("/orchestrate/run", json=payload)
    assert response.status_code in [401, 403]

def test_run_orchestration_valid_with_auth():
    token = create_access_token({"sub": "test_user", "role": "user"})
    headers = {"Authorization": f"Bearer {token}"}

    payload = {"task": "Analyze contract", "persona": "LegalAnalyst"}
    response = client.post("/orchestrate/run", json=payload, headers=headers)
    assert response.status_code == 200
    assert "job_id" in response.json()

def test_run_orchestration_invalid_persona_with_auth():
    token = create_access_token({"sub": "test_user", "role": "user"})
    headers = {"Authorization": f"Bearer {token}"}

    payload = {"task": "Analyze contract", "persona": "Invalid"}
    response = client.post("/orchestrate/run", json=payload, headers=headers)
    assert response.status_code == 400

def test_get_job_status():
    # First create a job
    token = create_access_token({"sub": "test_user", "role": "user"})
    headers = {"Authorization": f"Bearer {token}"}

    payload = {"task": "Test job", "persona": "LegalAnalyst"}
    response = client.post("/orchestrate/run", json=payload, headers=headers)
    job_id = response.json()["job_id"]

    # Then get status
    response = client.get(f"/jobs/{job_id}", headers=headers)
    assert response.status_code == 200
    assert "status" in response.json()

def test_pii_masking_default():
    # Test that PII is masked by default
    # This would require mocking the workflow response
    pass  # Placeholder for now

def test_pii_unmasking_for_auditor():
    token = create_access_token({"sub": "auditor_user", "role": "auditor"})
    headers = {"Authorization": f"Bearer {token}"}

    # Test endpoint that might return PII
    response = client.get("/personas?pii_mask=false", headers=headers)
    # Should allow unmasking for auditors
    assert response.status_code == 200

def test_pii_unmasking_denied_for_user():
    token = create_access_token({"sub": "regular_user", "role": "user"})
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/personas?pii_mask=false", headers=headers)
    # Should deny unmasking for regular users
    assert response.status_code == 403

def test_kg_nodes_endpoint():
    token = create_access_token({"sub": "test_user", "role": "user"})
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/kg/nodes", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_kg_edges_endpoint():
    token = create_access_token({"sub": "test_user", "role": "user"})
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/kg/edges", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_kg_stats_endpoint():
    token = create_access_token({"sub": "test_user", "role": "user"})
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/kg/stats", headers=headers)
    assert response.status_code == 200
    stats = response.json()
    assert "total_nodes" in stats
    assert "total_edges" in stats
    assert "avg_connections" in stats

def test_kg_search_endpoint():
    token = create_access_token({"sub": "test_user", "role": "user"})
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/kg/search?q=contract", headers=headers)
    assert response.status_code == 200
    results = response.json()
    assert "graph_results" in results
    assert "vector_results" in results
    assert "combined_insights" in results
