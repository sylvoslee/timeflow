from fastapi.testclient import TestClient
from ..main import app
from sqlmodel import SQLModel, Session, create_engine

client = TestClient(app)

test_con = f"sqlite:///backend/tests/test_db.sqlite"
test_engine = create_engine(test_con, echo=True)


def create_test_db():
    SQLModel.metadata.create_all(test_engine)
    return True


def test_post_epic():
    create_test_db()
    response = client.post(
        "/api/epics/", json={"name": "bricks", "work_area": "lego", "client_id": 1}
    )
    data = response.json()
    assert response.status_code == 200
    assert data == {"id": 1, "client_id": 1, "name": "bricks", "work_area": "lego"}


def test_get_epic_list():
    response = client.get("/api/epics/")
    data = response.json()
    assert response.status_code == 200
    assert data == [{"id": 1, "client_id": 1, "name": "bricks", "work_area": "lego"}]


def test_delete_epics():
    response = client.delete("/api/epics/?epic_name=bricks")
    assert response.status_code == 200
