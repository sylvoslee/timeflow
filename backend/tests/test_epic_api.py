from fastapi.testclient import TestClient
from ..main import app, session
from sqlmodel import SQLModel, Session, create_engine
from ..api.epic import get_session

test_con = f"sqlite:///backend/tests/test_db.sqlite"
test_engine = create_engine(
    test_con, connect_args={"check_same_thread": False}, echo=True
)


def get_session_override():
    session = Session(test_engine)
    return session


client = TestClient(app)


def create_test_db():
    SQLModel.metadata.create_all(test_engine)
    return True


def test_post_epic():
    create_test_db()
    app.dependency_overrides[get_session] = get_session_override

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


def test_get_epic_list():
    app.dependency_overrides[get_session] = get_session_override
    response = client.get("/api/epics/")
    app.dependency_overrides.clear()
    data = response.json()
    assert response.status_code == 200
    assert data == [
        {"id": 1, "client_id": 1, "name": "[dyvenia]branding", "work_area": "DYV"}
    ]


def test_delete_epics():
    app.dependency_overrides[get_session] = get_session_override
    response = client.delete("/api/epics/?epic_name=[dyvenia]branding")
    assert response.status_code == 200
    app.dependency_overrides.clear()
