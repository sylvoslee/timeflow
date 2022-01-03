from fastapi.testclient import TestClient
import pytest
import os
from ..main import app, session
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from ..api.epic import get_session

db_name = "test_db.sqlite"
test_con = f"sqlite:///{db_name}"
test_engine = create_engine(
    test_con, connect_args={"check_same_thread": False}, echo=True
)

# Creates the DB and Deletes it after ALL tests are run thanks to scope=module
@pytest.fixture(name="create_db", scope="module")
def create_db():
    # setup
    SQLModel.metadata.create_all(test_engine)
    yield
    # teardown
    os.remove(db_name)


@pytest.fixture(name="session")
def session_fixture(create_db):
    create_db

    with Session(test_engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_post_epic(client):
    response = client.post(
        "/api/epics/",
        json={"name": "[dyvenia]branding", "work_area": "DYV", "client_id": 1},
    )
    app.dependency_overrides.clear()

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


def test_delete_epics(client):
    response = client.delete("/api/epics/?epic_name=[dyvenia]branding")
    assert response.status_code == 200
