import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Hero's Journey API"}

def test_start_journey(client):
    response = client.post(
        "/wizard/start",
        json={"protagonist_desire": "To find inner peace", "helper_description": "A wise old sage"}
    )
    assert response.status_code == 200
    assert "challenge" in response.json()
