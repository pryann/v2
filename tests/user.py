from fastapi.testclient import TestClient
from main import app  # replace with the actual location of your FastAPI app
import pytest

client = TestClient(app)


def test_list_users():
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_find_user():
    response = client.get("/users/1")
    assert response.status_code == 200
    assert "id" in response.json()


def test_create_user():
    user_data = {
        "email": "test@example.com",
        "password": "testpassword",
    } 
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"


def test_create_existing_user():
    user_data = {
        "email": "test@example.com",
        "password": "testpassword",
    }  
    response = client.post("/users/", json=user_data)
    assert response.status_code == 409
