import pytest
from fastapi.testclient import TestClient
from api.service.main import app

client = TestClient(app)

def test_get_personas():
    response = client.get("/api/personas")  # Correct path
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_run_orchestration_valid():
    payload = {"task": "Analyze contract", "persona": "LegalAnalyst"}
    response = client.post("/orchestrate/run", json=payload)
    assert response.status_code == 200
    assert "job_id" in response.json()

def test_run_orchestration_invalid_persona():
    payload = {"task": "Analyze contract", "persona": "Invalid"}
    response = client.post("/orchestrate/run", json=payload)
    assert response.status_code == 400

def test_pii_masking():
    # Mock result with PII
    # In real test, mock the workflow
    pass  # Placeholder
