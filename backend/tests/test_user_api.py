from fastapi.testclient import TestClient
import pytest
import os
from ..main import app, session
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from ..api.epic import get_session


def test_post_user(client):
    response = client.post(
        "/api/users/",
        json={
            "short_name": "jsmith",
            "first_name": "John",
            "last_name": "Smith",
            "email": "jsmith@dyvenia.com",
            "role_id": 1,
            "team_id": 1,
            "start_date": "2022-03-10",
            "created_at": "2022-03-10T10:33:43.308Z",
            "updated_at": "2022-03-10T10:33:43.308Z",
            "is_active": True,
        },
    )
    data = response.json()
    assert response.status_code == 200
    assert data == {
        "short_name": "jsmith",
        "last_name": "Smith",
        "role_id": 1,
        "team_id": 1,
        "created_at": "2022-03-10T10:33:43.308000",
        "is_active": True,
        "id": 1,
        "email": "jsmith@dyvenia.com",
        "first_name": "John",
        "start_date": "2022-03-10",
        "updated_at": "2022-03-10T10:33:43.308000",
    }


def test_get_users(client):
    response = client.get("/api/users/")
    data = response.json()
    assert data == [
        {
            "short_name": "jsmith",
            "last_name": "Smith",
            "role_id": 1,
            "team_id": 1,
            "created_at": "2022-03-10T10:33:43.308000",
            "is_active": True,
            "id": 1,
            "first_name": "John",
            "email": "jsmith@dyvenia.com",
            "start_date": "2022-03-10",
            "updated_at": "2022-03-10T10:33:43.308000",
        }
    ]


def test_update_user(client):
    response1 = client.put("api/users/1/?is_active=false")
    assert response1.status_code == 200
    response2 = client.put("api/users/1/?is_active=true")
    assert response2.status_code == 200
    response3 = client.put("api/users/1/?new_email=jnowak")
    assert response3.status_code == 200
