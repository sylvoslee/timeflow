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
            "valid_from": "2022-01-01",
            "valid_to": "2022-04-01",
            "amount": 300,
            "created_at": "2022-03-04T14:16:24.524Z",
            "updated_at": "2022-03-04T14:16:24.524Z",
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
            "valid_from": "2022-01-01",
            "valid_to": "2022-04-01",
            "amount": 300,
            "created_at": "2022-03-04T14:16:24.524Z",
            "updated_at": "2022-03-04T14:16:24.524Z",
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
            "client_id": 1,
            "valid_to": "2022-04-01",
            "user_id": 1,
            "created_at": "2022-03-04T14:16:24.524000",
            "is_active": True,
            "valid_from": "2022-01-01",
            "id": 1,
            "amount": 300,
            "updated_at": "2022-03-04T14:16:24.524000",
        }
    ]


def test_deactivate_rate(client):
    response = client.put("/api/rates/1/deactivate")
    assert response.status_code == 200


def test_activate_rate(client):
    response = client.put("/api/rates/1/activate")
    assert response.status_code == 200


def test_read_active_rate(client):
    response = client.get("/api/rates/users/1/clients/1/active")
    data = response.json()
    assert response.status_code == 200


def test_rates_by_user_client_date(client):
    response = client.get("/api/rates/users/1/clients/1/months/?date=2022-02-01")
    assert response.status_code == 200


def test_update_rates(client):
    response = client.get("/api/rates/?user_id=1&client_id=1&new_amount=200")
    data = response.json()
    assert response.status_code == 200
    assert data == True
