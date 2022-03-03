from fastapi.testclient import TestClient
import pytest
import os
from ..main import app, session
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from ..utils import get_session
from datetime import datetime


@pytest.mark.order(1)
def test_post_rate(client):
    response1 = client.post(
        "/api/rates/",
        json={
            "user_id": 1,
            "client_id": 1,
            "year": 2022,
            "month": 1,
            "amount": 300,
            "created_at": "2022-03-03T11:06:08.053Z",
            "updated_at": "2022-03-03T11:06:08.053Z",
            "is_active": True,
        },
    )
    data1 = response1.json()
    assert response1.status_code == 200
    assert data1 == True
    response2 = client.post(
        "/api/rates/",
        json={
            "user_id": 1,
            "client_id": 1,
            "year": 2022,
            "month": 1,
            "amount": 300,
            "created_at": "2022-03-03T11:06:08.053Z",
            "updated_at": "2022-03-03T11:06:08.053Z",
            "is_active": True,
        },
    )
    data2 = response2.json()
    assert response2.status_code == 200
    assert data2 == False


def test_read_rates(client):
    response = client.get("/api/rates/")
    data = response.json()
    assert data == [
        {
            "id": 1,
            "user_id": 1,
            "client_id": 1,
            "year": 2022,
            "month": 1,
            "amount": 300.0,
            "created_at": "2022-03-03T11:06:08.053000",
            "updated_at": "2022-03-03T11:06:08.053000",
            "is_active": True,
        }
    ]


def test_deactivate_rate(client):
    response = client.put("/api/rates/1/deactivate")
    assert response.status_code == 200


def test_activate_rate(client):
    response = client.put("/api/rates/1/activate")
    assert response.status_code == 200
