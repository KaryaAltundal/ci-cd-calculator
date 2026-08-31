from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_calculate():
    response = client.get("/calculate?a=10&b=5")

    assert response.status_code == 200
    assert response.json() == {"result": 15}