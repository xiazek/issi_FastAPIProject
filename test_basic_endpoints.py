"""These are only the base endpoints covered."""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_read_movies():
    response = client.get("/movies")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_orm_movies():
    response = client.get("/orm/movies")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
