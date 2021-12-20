from fastapi import APIRouter
from utils import engine
from sqlmodel import Session, select, SQLModel
from sqlalchemy.exc import NoResultFound
from models.client import Client

router = APIRouter()
session = Session(engine)

# Post new client
@router.post("/api/clients/create")
async def client(client: Client):
    statement = select(Client).where(Client.name == client.name)
    try:
        result = session.exec(statement).one()
        return False
    except NoResultFound:
        session.add(client)
        session.commit()
        return True


# Get client by name
@router.get("/api/clients/read")
async def read_clients(client_name: str = None):
    statement = select(Client).where(Client.name == client_name)
    try:
        result = session.exec(statement).one()
        return result
    except NoResultFound:
        msg = f"""There is no client named {client_name}"""
        return msg


# Get list of clients
@router.get("/api/clients/list")
async def list_clients(list_name: str):
    if list_name == "clients":
        statement = select(Client.id, Client.name)
    results = session.exec(statement).all()
    return results


# Update client
@router.put("/api/clients/update")
async def update_clients(client_name: str, new_client_name: str):
    statement = select(Client).where(Client.name == client_name)
    client_to_update = session.exec(statement).one()
    print(client_to_update)
    client_to_update.name = new_client_name
    session.add(client_to_update)
    session.commit()
    session.refresh(client_to_update)
    return True


# Delete users
@router.delete("/api/clients/delete")
async def delete_clients(client_name: str = None):
    statement = select(Client).where(Client.name == client_name)
    results = session.exec(statement)
    client_to_delete = results.one()
    session.delete(client_to_delete)
    session.commit()
    return True