from fastapi import APIRouter, Depends
from ..utils import engine, get_session
from sqlmodel import Session, select, SQLModel, or_
from ..models.epic_area import EpicArea
from ..models.client import Client
from sqlalchemy.exc import NoResultFound
from datetime import datetime

router = APIRouter(prefix="/api/epic_areas", tags=["epic_area"])
session = Session(engine)

# Post new epic area
@router.post("/")
async def post_epic_area(
    *,
    epic_area: EpicArea,
    session: Session = Depends(get_session),
):
    statement1 = select(EpicArea).where(
        or_(EpicArea.name == epic_area.name, EpicArea.id == epic_area.id)
    )
    statement2 = select(Client.name).where(Client.id == epic_area.client_id)
    try:
        result = session.exec(statement1).one()
        return False
    except NoResultFound:
        session.add(epic_area)
        session.commit()
        session.refresh(epic_area)
        return epic_area
