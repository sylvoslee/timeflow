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
        "/api/roles",
        json={
            "short_name": "asd",
            "name": "Senior Data Analyst",
            "created_at": "2022-03-04T16:52:51.332Z",
            "updated_at": "2022-03-04T16:52:51.332Z",
            "is_active": True,
        },
    )
    data = response.json()
    assert response.status_code == 200
    assert data == {
        "id": 1,
        "short_name": "asd",
        "created_at": "2022-03-04T16:52:51.332000",
        "is_active": True,
        "name": "Senior Data Analyst",
        "updated_at": "2022-03-04T16:52:51.332000",
    }


# def test_read_teams(client):
#     response = client.get("/api/teams/juniors")
#     data = response.json()
#     assert response.status_code == 200
#     assert data == {
#         "id": 1,
#         "user_id": 1,
#         "name": "juniors",
#         "short_name": "jrs",
#         "is_active": True,
#     }


# def test_update_team(client):
#     response = client.put(
#         "api/teams/?id=1&name=juniors&short_name=jrs&active=True&new_user_id=2"
#     )
#     data = response.json()
#     assert response.status_code == 200
#     assert data == {
#         "id": 1,
#         "user_id": 2,
#         "name": "juniors",
#         "short_name": "jrs",
#         "is_active": True,
#     }


# def test_get_team(client):
#     response = client.get("/api/teams/")
#     data = response.json()
#     assert response.status_code == 200
#     assert data == [
#         {
#             "id": 1,
#             "user_id": 2,
#             "name": "juniors",
#             "short_name": "jrs",
#             "is_active": True,
#         }
#     ]


# @pytest.mark.order(-1)
# def test_deactivate_teams(client):
#     response = client.put("/api/teams/juniors/deactivate")
#     assert response.status_code == 200
