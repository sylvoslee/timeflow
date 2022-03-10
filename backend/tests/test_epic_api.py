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
        json={
            "short_name": "dadmin",
            "name": "[dyvenia]admin",
            "team_id": 1,
            "sponsor_id": 1,
            "start_date": "2022-03-08",
            "is_active": True,
            "created_at": "2022-03-08T12:43:28.006Z",
            "updated_at": "2022-03-08T12:43:28.006Z",
        },
    )
    data = response.json()
    assert response.status_code == 200
    assert data == {
        "id": 1,
        "short_name": "dadmin",
        "name": "[dyvenia]admin",
        "team_id": 1,
        "sponsor_id": 1,
        "start_date": "2022-03-08",
        "is_active": True,
        "created_at": "2022-03-08T12:43:28.006000",
        "updated_at": "2022-03-08T12:43:28.006000",
    }


def test_get_epics_list(client):
    response = client.get("/api/epics/")
    data = response.json()
    assert response.status_code == 200
    assert data == [
        {
            "sponsor_id": 1,
            "name": "[dyvenia]admin",
            "short_name": "dadmin",
            "is_active": True,
            "updated_at": "2022-03-08T12:43:28.006000",
            "id": 1,
            "team_id": 1,
            "start_date": "2022-03-08",
            "created_at": "2022-03-08T12:43:28.006000",
        }
    ]


def test_get_active_epics_list(client):
    response = client.get("/api/epics/active")
    data = response.json()
    assert response.status_code == 200
    assert data == [
        {
            "sponsor_id": 1,
            "name": "[dyvenia]admin",
            "short_name": "dadmin",
            "is_active": True,
            "updated_at": "2022-03-08T12:43:28.006000",
            "id": 1,
            "team_id": 1,
            "start_date": "2022-03-08",
            "created_at": "2022-03-08T12:43:28.006000",
        }
    ]


# def test_get_client_name_by_epic_id(client):
#     response = client.get("api/epics/1/client-name")
#     data = response.json()
#     assert response.status_code == 200
#     assert data == {"client_name": "dyvenia", "client_id": 1}


def test_deactivate_epic(client):
    response = client.put("api/epics/1/deactivate")
    assert response.status_code == 200


def test_activate_epic(client):
    response = client.put("api/epics/1/activate")
    assert response.status_code == 200


def test_update_epic(client):
    response = client.put("api/epics/?epic_id=1&new_short_name=new_sn&new_name=new_n")
    assert response.status_code == 200
