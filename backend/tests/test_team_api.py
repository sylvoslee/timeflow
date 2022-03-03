import pytest
from ..main import app, session


@pytest.mark.order(1)
def test_post_team(client):
    response = client.post(
        "/api/teams",
        json={
            "user_id": 1,
            "name": "juniors",
            "short_name": "jrs",
            "is_active": True,
        },
    )
    data = response.json()
    assert response.status_code == 200
    assert data == {
        "id": 1,
        "user_id": 1,
        "name": "juniors",
        "short_name": "jrs",
        "is_active": True,
    }


def test_read_teams(client):
    response = client.get("/api/teams/juniors")
    data = response.json()
    assert response.status_code == 200
    assert data == {
        "id": 1,
        "user_id": 1,
        "name": "juniors",
        "short_name": "jrs",
        "is_active": True,
    }


def test_update_team(client):
    response = client.put(
        "api/teams/?id=1&name=juniors&short_name=jrs&active=True&new_user_id=2"
    )
    data = response.json()
    assert response.status_code == 200
    assert data == {
        "id": 1,
        "user_id": 2,
        "name": "juniors",
        "short_name": "jrs",
        "is_active": True,
    }


def test_get_team(client):
    response = client.get("/api/teams/")
    data = response.json()
    assert response.status_code == 200
    assert data == [
        {
            "id": 1,
            "user_id": 2,
            "name": "juniors",
            "short_name": "jrs",
            "is_active": True,
        }
    ]


@pytest.mark.order(-1)
def test_deactivate_teams(client):
    response = client.put("/api/teams/juniors/deactivate")
    assert response.status_code == 200
