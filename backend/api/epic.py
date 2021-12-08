from fastapi import APIRouter
from utils import engine
from sqlmodel import Session, select, SQLModel, or_
from models.epic import Epic
from models.client import Client

from sqlalchemy.exc import NoResultFound

router = APIRouter()
session = Session(engine)

# Post new epic
@router.post("/api/epics/create")
async def post_epic(epic: Epic):
    statement = select(Epic).where(Epic.name == epic.name)
    try:
        result = session.exec(statement).one()
        return False
    except NoResultFound:
        session.add(epic)
        session.commit()
        return True


# Get epic by name
@router.get("/api/epics/read")
async def read_epics(epic_name: str = None):
    statement = select(Epic).where(Epic.name == epic_name)
    try:
        result = session.exec(statement).one()
        return result
    except NoResultFound:
        msg = f"""There is no epic named {epic_name}"""
        return msg


# Get epics list
@router.get("/api/epics/list")
async def get_epic_list(list_name: str = None):
    if list_name == "epics":
        statement = select(Epic.name)
        result = session.exec(statement).all()
        return result
    else:
        return f"""This list doesn't exist. Please select existing list"""


# Update epics
@router.put("/api/epics/update")
async def update_epic(
    epic_id: str = None,
    epic_name: str = None,
    work_area: str = None,
    client_new_id: int = None,
):
    statement = select(Epic).where(or_(Epic.name == epic_name, Epic.id == epic_id))
    epic_to_update = session.exec(statement).one()
    epic_to_update.work_area = work_area
    epic_to_update.client_id = client_new_id
    session.add(epic_to_update)
    session.commit()
    session.refresh(epic_to_update)
    return True


# Delete epics
@router.delete("/api/epics/delete")
async def delete_epics(epic_name: str = None):
    statement = select(Epic).where(Epic.name == epic_name)
    results = session.exec(statement)
    epic_to_delete = results.one()
    session.delete(epic_to_delete)
    session.commit()
    return True
