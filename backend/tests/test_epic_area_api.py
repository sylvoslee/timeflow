from fastapi.testclient import TestClient
import pytest
import os
from ..main import app, session
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from ..api.epic_area import get_session


@pytest.mark.order(1)
def test_post_epic_area(client):
    response = client.post(
        "/api/epic_areas/",
        json={
            "epic_id": 1,
            "name": "graphics",
            "is_active": True,
        },
    )
    data = response.json()
    assert response.status_code == 200
    assert data == {
        "id": 1,
        "epic_id": 1,
        "name": "graphics",
        "is_active": True,
    }


def test_read_epic_areas(client):
    response = client.get("/api/epics/graphics")
    data = response.json()
    assert response.status_code == 200
    assert data == {
        "id": 1,
        "epic_id": 1,
        "name": "graphics",
        "is_active": True,
    }


def test_update_epic_area(client):
    response = client.put("api/epics/?id=1&name=graphics&is_active=True&new_epic_id=2")
    data = response.json()
    assert response.status_code == 200
    assert data == {
        "id": 1,
        "epic_id": 2,
        "name": "graphics",
        "is_active": True,
    }


def test_get_epic_list(client):
    response = client.get("/api/epic_areas/")
    data = response.json()
    assert response.status_code == 200
    assert data == [
        {
            "id": 1,
            "epic_id": 2,
            "name": "graphics",
            "is_active": True,
        }
    ]


@pytest.mark.order(-1)
def test_deactivate_epics(client):
    response = client.put("/api/epic_areas/graphics/deactivate")
    assert response.status_code == 200
