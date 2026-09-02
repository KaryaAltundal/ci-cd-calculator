from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_sum():
    response = client.get("/sum?a=10&b=5")

    assert response.status_code == 200
    assert response.json() == {"result": 15}


def test_subtract():
    response = client.get("/subtract?a=10&b=5")

    assert response.status_code == 200

    assert response.json() == {"result": 5}

    assert response.json() == {"result": 5}

