from fastapi.testclient import TestClient
import pytest
import os
from ..main import app, session
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from ..utils import get_session
from datetime import datetime


@pytest.mark.order(1)
def test_post_role(client):
    response = client.post(
        "/api/roles/",
        json={
            "short_name": "sda",
            "name": "Senior Data Analyst",
            "created_at": "2022-03-07T10:00:50.800Z",
            "updated_at": "2022-03-07T10:00:50.800Z",
            "is_active": True,
        },
    )
    data = response.json()
    assert response.status_code == 200
    assert data == {
        "id": 1,
        "short_name": "sda",
        "created_at": "2022-03-07T10:00:50.800000",
        "is_active": True,
        "name": "Senior Data Analyst",
        "updated_at": "2022-03-07T10:00:50.800000",
    }


def test_read_roles(client):
    response = client.get(
        "/api/roles/",
        json=[
            {
                "id": 1,
                "short_name": "sda",
                "created_at": "2022-03-07T10:00:50.800000",
                "is_active": True,
                "name": "Senior Data Analyst",
                "updated_at": "2022-03-07T10:00:50.800000",
            }
        ],
    )


def test_deactivate_role(client):
    response = client.put("/api/roles/1/deactivate")
    assert response.status_code == 200


def test_activate_role(client):
    response = client.put("/api/roles/1/activate")
    assert response.status_code == 200


def test_update_role(client):
    response = client.put(
        "api/roles/?id=1&new_name=mde&new_short_name=Mid%20Data%20Engineer&is_active=true"
    )
    assert response.status_code == 200
