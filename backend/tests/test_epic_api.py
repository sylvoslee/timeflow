from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)


def test_get_epic_list():
    response = client.get("/api/epics/")
    assert response.status_code == 200


def test_get_epic_list():
    response = client.get("/api/epics/{epic_name}")
    assert response.status_code == 200
