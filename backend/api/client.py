from fastapi import APIRouter, Depends
from ..utils import engine, get_session
from sqlmodel import Session, select, SQLModel
from sqlalchemy.exc import NoResultFound
from ..models.client import Client
from ..models.epic import Epic


router = APIRouter(prefix="/api/clients")
session = Session(engine)

# Post new client
@router.post("/")
async def post_client(*, client: Client, session: Session = Depends(get_session)):
    statement = select(Client).where(Client.name == client.name)
    try:
        result = session.exec(statement).one()
        return False
    except NoResultFound:
        session.add(client)
        session.commit()
        session.refresh(client)
        return client


# Get list of all clients
@router.get("/")
async def read_clients(session: Session = Depends(get_session)):
    statement = select(Client)
    results = session.exec(statement).all()
    return results


# Get client by id
@router.get("/{client_id}")
async def read_clients(
    *, client_id: int = None, session: Session = Depends(get_session)
):
    statement = select(Client).where(Client.id == client_id)
    try:
        result = session.exec(statement).one()
        return result
    except NoResultFound:
        msg = f"""There is no client with id = {client_id}"""
        return msg


# Get all selected client's epics
@router.get("/{client_id}/epics/")
async def read_clients_epics(
    client_id: int = None, session: Session = Depends(get_session)
):
    statement = (
        select(Client.id, Client.name, Epic.name)
        .select_from(Client)
        .join(Epic)
        .where(Client.id == client_id)
    )
    results = session.exec(statement).all()
    return results


# Update client
@router.put("/{client_id}")
async def update_clients(client_id: int = None, new_client_name: str = None):
    statement = select(Client).where(Client.id == client_id)
    client_to_update = session.exec(statement).one()
    print(client_to_update)
    client_to_update.name = new_client_name
    session.add(client_to_update)
    session.commit()
    session.refresh(client_to_update)
    return True


# Delete users
@router.delete("/")
async def delete_clients(client_name: str = None):
    statement = select(Client).where(Client.name == client_name)
    results = session.exec(statement)
    client_to_delete = results.one()
    session.delete(client_to_delete)
    session.commit()
    return True
