from fastapi.testclient import TestClient
import pytest
import os
from ..main import app, session
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from ..utils import get_session

db_name = "test_db.sqlite"
test_con = f"sqlite:///{db_name}"
test_engine = create_engine(
    test_con, connect_args={"check_same_thread": False}, echo=True
)


@pytest.fixture(name="create_db", scope="session")
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
