from fastapi import APIRouter, Depends
from ..utils import engine, get_session
from sqlmodel import Session, select, SQLModel
from sqlalchemy.exc import NoResultFound
from ..models.client import Client
from ..models.epic import Epic
from datetime import datetime

router = APIRouter(prefix="/api/clients", tags=["client"])
session = Session(engine)


@router.post("/")
async def post_client(*, client: Client, session: Session = Depends(get_session)):
    """Post a new client"""
    statement = select(Client).where(Client.name == client.name)
    try:
        result = session.exec(statement).one()
        return False
    except NoResultFound:
        session.add(client)
        session.commit()
        session.refresh(client)
        return client


@router.get("/")
async def read_clients(session: Session = Depends(get_session)):
    """Get a list of all clients"""
    statement = select(Client)
    results = session.exec(statement).all()
    return results


@router.get("/active")
async def read_clients(session: Session = Depends(get_session)):
    """Get a list of all active clients"""
    statement = select(Client).where(Client.is_active == True)
    results = session.exec(statement).all()
    return results


@router.get("/{client_id}")
async def read_clients(
    *, client_id: int = None, session: Session = Depends(get_session)
):
    """Get a client by client_id"""
    statement = select(Client).where(Client.id == client_id)
    try:
        result = session.exec(statement).one()
        return result
    except NoResultFound:
        msg = f"""There is no client with id = {client_id}"""
        return msg


@router.get("/names/{name}")
async def read_clients_by_name(
    *, name: str = None, session: Session = Depends(get_session)
):
    """Get a client by client_name"""
    statement = select(Client).where(Client.name == name)
    result = session.exec(statement).one()
    return result


@router.get("/{client_id}/epics/")
async def read_clients_epics(
    client_id: int = None, session: Session = Depends(get_session)
):
    """Get epics from a client_id"""
    statement = (
        select(Client.id, Client.name, Epic.name)
        .select_from(Client)
        .join(Epic)
        .where(Client.id == client_id)
    )
    results = session.exec(statement).all()
    return results


# @router.put("/{client_id}/deactivate-client")
# async def update_clients(
#     *,
#     client_id: int,
#     session: Session = Depends(get_session),
# ):
#     """Deactivate a client"""
#     statement = select(Client).where(Client.id == client_id)
#     client_to_update = session.exec(statement).one()
#     client_to_update.active = False
#     statement2 = select(Epic).join(Clinet)
#     client_to_update = session.exec(statement).one()
#     client_to_update.active = False

#     session.add(client_to_update)
#     session.commit()
#     session.refresh(client_to_update)
#     return client_to_update


@router.put("/{client_id}/activate")
async def activate_clients(
    *,
    client_id: int,
    session: Session = Depends(get_session),
):
    """Activate a client"""
    statement = select(Client).where(Client.id == client_id)
    client_to_update = session.exec(statement).one()
    client_to_update.is_active = True
    client_to_update.updated_at = datetime.now()
    session.add(client_to_update)
    session.commit()
    session.refresh(client_to_update)
    return client_to_update


@router.put("/{client_id}/deactivate")
async def deactivate_clients(
    *,
    client_id: int,
    session: Session = Depends(get_session),
):
    """Deactivate a client"""
    statement = select(Client).where(Client.id == client_id)
    client_to_update = session.exec(statement).one()
    client_to_update.is_active = False
    client_to_update.updated_at = datetime.now()
    session.add(client_to_update)

    session.commit()
    session.refresh(client_to_update)
    return client_to_update


@router.put("/{client_id}/deactivate-epics")
async def update_clients_and_epics(
    *,
    client_id: int,
    session: Session = Depends(get_session),
):
    """Deactivate a client and its epics"""
    statement1 = select(Client).where(Client.id == client_id)
    client_to_update = session.exec(statement1).one()
    client_to_update.is_active = False
    client_to_update.updated_at = datetime.now()
    session.add(client_to_update)
    statement2 = select(Epic).where(Epic.client_id == client_id)
    epics_to_update = session.exec(statement2).all()
    for epic in epics_to_update:
        epic.is_active = False
        session.add(epic)
    session.commit()
    return True


@router.put("/{client_id}/new-name")
async def update_clients(
    *,
    client_id: int = None,
    new_client_name: str = None,
    session: Session = Depends(get_session),
):
    """Update a client from a client_id"""
    statement = select(Client).where(Client.id == client_id)
    client_to_update = session.exec(statement).one()
    client_to_update.name = new_client_name
    client_to_update.updated_at = datetime.now()
    session.add(client_to_update)
    session.commit()
    session.refresh(client_to_update)
    return client_to_update
