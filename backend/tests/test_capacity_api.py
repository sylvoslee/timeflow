from fastapi.testclient import TestClient
import pytest
from ..main import app, session
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from ..api.client import get_session


def test_post_capacity(client):
    response = client.post(
        "/api/capacities/",
        json={
            "user_id": 1,
            "team_id": 1,
            "year": 2022,
            "month": 3,
            "days": 18,
            "created_at": "2022-03-15T13:46:24.344Z",
            "updated_at": "2022-03-15T13:46:24.344Z",
            "is_locked": False,
        },
    )
    data = response.json()
    assert response.status_code == 200
    assert data == {
        "id": 1,
        "user_id": 1,
        "team_id": 1,
        "year": 2022,
        "month": 3,
        "days": 18,
        "created_at": "2022-03-15T13:46:24.344000",
        "updated_at": "2022-03-15T13:46:24.344000",
        "is_locked": False,
    }


def test_get_capacities(client):
    response = client.get("/api/capacities/")
    data = response.json()
    assert data == [
        {
            "id": 1,
            "user_id": 1,
            "team_id": 1,
            "year": 2022,
            "month": 3,
            "days": 18,
            "created_at": "2022-03-15T13:46:24.344000",
            "updated_at": "2022-03-15T13:46:24.344000",
            "is_locked": False,
        }
    ]


def test_delete_capacity(client):
    response = client.delete("/api/capacities/?capacity_id=1")
    assert response.status_code == 200
