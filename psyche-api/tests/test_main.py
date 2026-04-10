import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../psyche-core')))
from main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client

def test_health_check_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "agents" in data

def test_recommend_endpoint_missing_payload(client):
    response = client.post("/recommend")
    assert response.status_code == 422

def test_recommend_endpoint_success(client):
    response = client.post("/recommend", json={"user_id": "test_user", "n": 5})
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert "agent_weights" in data
    assert "listener_state" in data

def test_integrity_check(client):
    response = client.get("/integrity/check/track123")
    assert response.status_code == 200
    data = response.json()
    assert "track_id" in data
    assert "passed" in data

def test_explainability(client):
    response = client.get("/explain/track123?user_id=test_user")
    assert response.status_code == 200
    data = response.json()
    assert "explanation" in data
