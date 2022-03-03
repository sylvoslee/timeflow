from fastapi import APIRouter, Depends
from ..utils import engine, get_session
from sqlmodel import Session, select, or_
from ..models.team import Team
from ..models.user import User
from sqlalchemy import NoResultFound
from datetime import datetime

router = APIRouter(prefix="/api/teams", tags=["team"])
session = Session(engine)

# Post new team
@router.post("/")
async def post_team(*, team: Team, session: Session = Depends(get_session)):
    statement = select(Team).where(or_(Team.name == team.name, team.id == team.id))
    try:
        result = session.exec(statement).one()
        return False
    except NoResultFound:
        session.add(team)
        session.commit()
        session.refresh(team)
        return team
