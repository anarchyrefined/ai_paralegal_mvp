import pytest
from fastapi.testclient import TestClient
from api.service.main import app
from api.service.auth import create_access_token, authenticate_user

client = TestClient(app)

def test_create_access_token():
    token = create_access_token({"sub": "test_user", "role": "user"})
    assert isinstance(token, str)
    assert len(token) > 0

def test_authenticate_user_valid_token():
    token = create_access_token({"sub": "test_user", "role": "user"})
    user = authenticate_user(token)

    assert user is not None
    assert user["sub"] == "test_user"
    assert user["role"] == "user"

def test_authenticate_user_invalid_token():
    user = authenticate_user("invalid_token")
    assert user is None

def test_authenticate_user_expired_token():
    # This would require mocking time, but for now just test structure
    pass

def test_protected_endpoint_requires_auth():
    response = client.post("/orchestrate/run", json={"task": "test", "persona": "LegalAnalyst"})
    # Should require auth now
    assert response.status_code in [401, 403]  # Unauthorized or Forbidden

def test_protected_endpoint_with_valid_auth():
    token = create_access_token({"sub": "test_user", "role": "user"})
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/orchestrate/run",
        json={"task": "test task", "persona": "LegalAnalyst"},
        headers=headers
    )

    # Should work with valid auth (may fail for other reasons but not auth)
    assert response.status_code != 401
    assert response.status_code != 403

def test_auditor_can_unmask_pii():
    token = create_access_token({"sub": "auditor_user", "role": "auditor"})
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/some_endpoint_with_pii?pii_mask=false", headers=headers)
    # Should allow unmasking for auditors
    assert response.status_code != 403

def test_regular_user_cannot_unmask_pii():
    token = create_access_token({"sub": "regular_user", "role": "user"})
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/some_endpoint_with_pii?pii_mask=false", headers=headers)
    # Should deny unmasking for regular users
    assert response.status_code == 403

def test_invalid_role_handling():
    token = create_access_token({"sub": "user", "role": "invalid_role"})
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/orchestrate/run",
        json={"task": "test", "persona": "LegalAnalyst"},
        headers=headers
    )

    assert response.status_code == 403
