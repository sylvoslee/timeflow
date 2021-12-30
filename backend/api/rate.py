from fastapi import APIRouter
from ..utils import engine
from sqlmodel import Session, select, SQLModel
from sqlalchemy.exc import NoResultFound
from ..models.rate import Rate

router = APIRouter(prefix="/api/rates")
session = Session(engine)


# Post new rate
@router.post("/")
async def rate(rate: Rate):
    statement = select(Rate).where(Rate.id == rate.id)
    try:
        result = session.exec(statement).one()
        return False
    except NoResultFound:
        session.add(rate)
        session.commit()
        return True


# Get rate
@router.get("/{user_id},{client_id}")
async def read_rates(user_id: str = None, client_id: str = None):
    if user_id != None and client_id != None:
        statement = (
            select(Rate)
            .where(Rate.user_id == user_id)
            .where(Rate.client_id == client_id)
        )
    result = session.exec(statement).one()
    return result


# Get list of rates
@router.get("/list")
async def list_rates():
    statement = select(Rate)
    results = session.exec(statement).all()
    return results


# Update rates
@router.put("/")
async def update_rates(
    user_id: str = None, client_id: str = None, new_daily_value: str = None
):
    statement = (
        select(Rate).where(Rate.user_id == user_id).where(Rate.client_id == client_id)
    )
    rate_to_update = session.exec(statement).one()
    print(rate_to_update)
    rate_to_update.daily_value = new_daily_value
    session.add(rate_to_update)
    session.commit()
    session.refresh(rate_to_update)
    return True


# Delete rates
@router.delete("/")
async def delete_rates(user_id: str = None, client_id: str = None):
    statement = select(Rate).where(Rate.user_id == user_id)
    results = session.exec(statement)
    rate_to_delete = results.one()
    session.delete(rate_to_delete)
    session.commit()
    return True
