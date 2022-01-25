from fastapi.testclient import TestClient
import pytest
import os
from ..main import app, session
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from ..api.epic import get_session


@pytest.post("/")
def test_post_user(client):
    response = client.post(
        "/api/users/",
        json={"username": "anowak", "name": "adam", "surname": "nowak", "email": "anowak@dyvenia.com"}
    )
    data = response.json()
    assert response.status_code == 200
    assert data == {
        "id": 1,
        "username": "anowak", 
        "name": "adam", 
        "surname": "nowak", 
        "email": "anowak@dyvenia.com"
    }

def test_get_users_list(client):
    response = client.get("/api/users/")
    data = response.json()
    assert data == {
        "id": 1,
        "username": "anowak", 
        "name": "adam", 
        "surname": "nowak", 
        "email": "anowak@dyvenia.com"
    }


def test_update_users(client):
    response = client.put("api/users/?username=anowak&email=adam.nowak%40dyvenia.com")
    data = response.json()
    assert data == {
        "id": 1,
        "username": "anowak", 
        "name": "adam", 
        "surname": "nowak", 
        "email": "adam.nowak@dyvenia.com"
    }

def test_delete_users(client):
    response = client.delete("/api/users/?username=anowak")
    assert response.status_code == 200