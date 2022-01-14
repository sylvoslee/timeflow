from fastapi.testclient import TestClient
import pytest
import os
from ..main import app, session
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from ..api.epic import get_session


@pytest.mark.order(1)
def test_post_epic(client):
    response = client.post(
        "/api/epics/",
        json={"name": "[dyvenia]branding", "work_area": "DYV", "client_id": 1},
    )
    data = response.json()
    assert response.status_code == 200
    assert data == {
        "id": 1,
        "client_id": 1,
        "name": "[dyvenia]branding",
        "work_area": "DYV",
    }


def test_read_epics(client):
    response = client.get("/api/epics/[dyvenia]branding")
    data = response.json()
    assert response.status_code == 200
    assert data == {
        "id": 1,
        "client_id": 1,
        "name": "[dyvenia]branding",
        "work_area": "DYV",
    }


def test_update_epic(client):
    response = client.put("api/epics/?epic_id=1&work_area=DYV&client_new_id=2")
    data = response.json()
    assert response.status_code == 200
    assert data == {
        "id": 1,
        "client_id": 2,
        "name": "[dyvenia]branding",
        "work_area": "DYV",
    }


def test_get_epic_list(client):
    response = client.get("/api/epics/")
    data = response.json()
    assert response.status_code == 200
    assert data == [
        {"id": 1, "client_id": 2, "name": "[dyvenia]branding", "work_area": "DYV"}
    ]


@pytest.mark.order(-1)
def test_delete_epics(client):
    response = client.delete("/api/epics/?epic_name=[dyvenia]branding")
    assert response.status_code == 200
