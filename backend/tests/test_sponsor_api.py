import pytest
from ..main import app, session


@pytest.mark.order(1)
def test_post_sponsor(client):
    response = client.post(
        "/api/sponsors",
        json={
            "client_id": 1,
            "name": "facebook",
            "short_name": "fb",
            "is_active": True,
        },
    )
    data = response.json()
    assert response.status_code == 200
    assert data == {
        "client_id": 1,
        "name": "facebook",
        "short_name": "fb",
        "is_active": True,
    }


def test_read_sponsors(client):
    response = client.get("/api/sponsors/facebook")
    data = response.json()
    assert response.status_code == 200
    assert data == {
        "id": 1,
        "client_id": 1,
        "name": "facebook",
        "short_name": "fb",
        "is_active": True,
    }


def test_update_sponsor(client):
    response = client.put(
        "api/sponsors/?id=1&name=facebook&short_name=fb&active=True&new_client_id=2"
    )
    data = response.json()
    assert response.status_code == 200
    assert data == {
        "id": 1,
        "client_id": 2,
        "name": "facebook",
        "short_name": "fb",
        "is_active": True,
    }


def test_get_sponsor(client):
    response = client.get("/api/sponsors/")
    data = response.json()
    assert response.status_code == 200
    assert data == [
        {
            "id": 1,
            "client_id": 2,
            "name": "facebook",
            "short_name": "fb",
            "is_active": True,
        }
    ]


@pytest.mark.order(-1)
def test_deactivate_teams(client):
    response = client.put("/api/sponsors/facebook/deactivate")
    assert response.status_code == 200
