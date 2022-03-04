from fastapi import APIRouter, Depends
from ..utils import engine, get_session
from sqlmodel import Session, select, or_
from ..models.client import Client
from ..models.sponsor import Sponsor
from sqlalchemy.exc import NoResultFound
from datetime import datetime

router = APIRouter(prefix="/api/sponsors", tags=["sponsor"])
session = Session(engine)

# Post new sponsor
@router.post("/")
async def post_sponsor(
    *,
    sponsor: Sponsor,
    session: Session = Depends(get_session),
):
    statement = select(Sponsor).where(
        or_(Sponsor.name == sponsor.name, Sponsor.id == sponsor.id)
    )
    try:
        result = session.exec(statement).one()
        return False
    except NoResultFound:
        session.add(sponsor)
        session.commit()
        session.refresh(sponsor)
        return sponsor
