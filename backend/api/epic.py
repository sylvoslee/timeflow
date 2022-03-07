from fastapi import APIRouter, Depends
from ..utils import engine, get_session
from sqlmodel import Session, select, SQLModel, or_
from ..models.epic import Epic
from ..models.client import Client
from sqlalchemy.exc import NoResultFound
from datetime import datetime

router = APIRouter(prefix="/api/epics", tags=["epic"])
session = Session(engine)


@router.post("/")
async def post_epic(
    *,
    epic: Epic,
    session: Session = Depends(get_session),
):
    """Post new epic"""
    statement1 = select(Epic).where(or_(Epic.name == epic.name, Epic.id == epic.id))
    statement2 = select(Client.name).where(Client.id == epic.client_id)
    try:
        result = session.exec(statement1).one()
        return False
    except NoResultFound:
        session.add(epic)
        session.commit()
        session.refresh(epic)
        return epic


@router.get("/")
async def get_epic_list(session: Session = Depends(get_session)):
    """Get list of epics"""
    statement = select(Epic)
    results = session.exec(statement).all()
    return results


@router.get("/active")
async def get_active_epic_list(session: Session = Depends(get_session)):
    """Get list of active epics"""
    statement = select(Epic).where(Epic.active == True)
    results = session.exec(statement).all()
    return results


@router.get("/{epic_name}")
async def read_epics(epic_name: str = None, session: Session = Depends(get_session)):
    """Read a single epic from an epic_name"""
    statement = select(Epic).where(Epic.name == epic_name)
    try:
        result = session.exec(statement).one()
        return result
    except NoResultFound:
        msg = f"""There is no epic named {epic_name}"""
        return msg


@router.get("/{epic_id}/client-name")
async def get_client_name_by_epic_id(
    epic_id: int, session: Session = Depends(get_session)
):
    """Get client name from epic_id"""
    statement = (
        select(Epic.id, Client.id, Client.name)
        .join(Client)
        .where(Epic.id == epic_id)
        .where(Client.active == True)
    )
    result = session.exec(statement).one()
    return result


@router.put("/{epic_id}/activate")
async def activate_epic(
    epic_id: str = None,
    session: Session = Depends(get_session),
):
    """Activate an epic"""
    statement = select(Epic).where(Epic.id == epic_id)
    epic_to_activate = session.exec(statement).one()
    epic_to_activate.active = True
    epic_to_activate.updated_at = datetime.now()
    session.add(epic_to_activate)
    session.commit()
    session.refresh(epic_to_activate)
    return epic_to_activate


@router.put("/{epic_id}/deactivate")
async def deactivate_epic(
    epic_id: str = None,
    session: Session = Depends(get_session),
):
    """Deactivate an epic"""
    statement = select(Epic).where(Epic.id == epic_id)
    epic_to_deactivate = session.exec(statement).one()
    epic_to_deactivate.active = False
    epic_to_deactivate.updated_at = datetime.now()
    session.add(epic_to_deactivate)
    session.commit()
    session.refresh(epic_to_deactivate)
    return epic_to_deactivate


@router.put("/")
async def update_epic(
    epic_id: str = None,
    epic_name: str = None,
    work_area: str = None,
    client_new_id: int = None,
    session: Session = Depends(get_session),
):
    """Update an epic"""
    statement = select(Epic).where(or_(Epic.name == epic_name, Epic.id == epic_id))
    epic_to_update = session.exec(statement).one()
    epic_to_update.work_area = work_area
    epic_to_update.client_id = client_new_id
    session.add(epic_to_update)
    epic_to_update.updated_at = datetime.now()
    session.commit()
    session.refresh(epic_to_update)
    return epic_to_update
