from fastapi.testclient import TestClient
import pytest
import os
from ..main import app, session
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from ..api.client import get_session


@pytest.mark.order(2)
def test_post_client(client):
    response1 = client.post(
        "/api/clients/",
        json={"name": "dyvenia"},
    )
    data1 = response1.json()
    assert response1.status_code == 200
    assert data1 == {
        "name": "dyvenia",
        "id": 1,
    }
    response2 = client.post(
        "/api/clients/",
        json={"name": "dyvenia"},
    )
    data2 = response2.json()
    assert response2.status_code == 200
    assert data2 == False


def test_read_clients_all(client):
    response = client.get("/api/clients/")
    data = response.json()
    assert data == [{"name": "dyvenia", "id": 1}]


def test_read_client_id(client):
    response1 = client.get("/api/clients/1")
    data1 = response1.json()
    assert data1 == {
        "name": "dyvenia",
        "id": 1,
    }
    response2 = client.get("/api/clients/0")
    data2 = response2.json()
    assert data2 == "There is no client with id = 0"


def test_read_clients_epics(client):
    response = client.get("api/clients/1/epics")
    data = response.json()
    assert data == [{"id": 1, "name": "dyvenia", "name_1": "[dyvenia]branding"}]


def test_update_clients(client):
    response = client.put("api/clients/1/new-name?new_client_name=dyvenia_update")
    data = response.json()
    assert data == {"id": 1, "name": "dyvenia_update"}


def test_delete_clients(client):
    response = client.delete("/api/clients/1?client_name=dyvenia_update")
    data = response.json()
    assert data == True


# # Delete clients
# @router.delete("/{client_id}")
# async def delete_clients(
#     *, client_id: int, client_name: str, session: Session = Depends(get_session)
# ):
#     statement = (
#         select(Client).where(Client.name == client_name).where(Client.id == client_id)
#     )
#     client_to_delete = session.exec(statement).one()
#     session.delete(client_to_delete)
#     session.commit()
#     return True
