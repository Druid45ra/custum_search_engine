from api.app import create_app


def test_api_client():
    app = create_app()
    client = app.test_client()
    response = client.get("/search?q=test")
    assert response.status_code in [200, 400]
