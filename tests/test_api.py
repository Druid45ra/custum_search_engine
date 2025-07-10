import pytest
from api.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_search_endpoint(client):
    response = client.get("/search?q=test")
    assert response.status_code in [200, 400]
    if response.status_code == 200:
        assert "results" in response.json


def test_crawl_endpoint(client):
    response = client.post("/crawl", json={"url": "https://example.com"})
    assert response.status_code == 200
    assert "message" in response.json
