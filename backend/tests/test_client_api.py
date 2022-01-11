from fastapi.testclient import TestClient
import pytest
import os
from ..main import app, session
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from ..api.client import get_session


@pytest.mark.order(2)
def test_post_client(client):
    response1 = client.post(
        "/api/clients/",
        json={"name": "dyvenia"},
    )
    data1 = response1.json()
    assert response1.status_code == 200
    assert data1 == {
        "name": "dyvenia",
        "id": 1,
    }
    response2 = client.post(
        "/api/clients/",
        json={"name": "dyvenia"},
    )
    data2 = response2.json()
    assert response2.status_code == 200
    assert data2 == False


def test_read_clients(client):
    response = client.get("/api/clients/")
    data = response.json()
    assert data == [{"name": "dyvenia", "id": 1}]


def test_read_clients_epics(client):
    response = client.get("api/clients/1/epics")
    data = response.json()
    assert data == [{"id": 1, "name": "dyvenia", "name_1": "[dyvenia]branding"}]
