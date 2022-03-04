from fastapi import APIRouter, Depends
from ..utils import engine, get_session, far_date, date_str_to_date
from sqlmodel import Session, select, SQLModel
from sqlalchemy.exc import NoResultFound
from ..models.rate import Rate
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/rates", tags=["rate"])
session = Session(engine)


# Post new rate
@router.post("/")
async def rate(
    rate: Rate,
    session: Session = Depends(get_session),
):
    statement1 = (
        select(Rate)
        .where(Rate.user_id == rate.user_id)
        .where(Rate.client_id == rate.client_id)
        .where(Rate.valid_from >= rate.valid_from)
    )

    one_day_delta = timedelta(days=1)
    close_date = rate.valid_from - one_day_delta
    statement2 = (
        select(Rate)
        .where(Rate.user_id == rate.user_id)
        .where(Rate.client_id == rate.client_id)
        .where(Rate.valid_to == far_date)
    )
    try:
        result = session.exec(statement1).one()
        return False
    except NoResultFound:
        try:
            rate_to_close = session.exec(statement2).one()
            rate_to_close.valid_to = close_date
            rate_to_close.updated_at = datetime.now()
            rate_to_close.is_active = False
            session.add(rate_to_close)
            session.add(rate)
            session.commit()
            return True
        except NoResultFound:
            session.add(rate)
            session.commit()
            return True


# Get rate
@router.get("/")
async def read_rates(
    session: Session = Depends(get_session),
):
    statement = select(Rate)
    result = session.exec(statement).all()
    return result


@router.get("/users/{user_id}/clients/{client_id}/months/")
async def rates_by_user_client_date(
    user_id: int,
    client_id: int,
    date: str,
    session: Session = Depends(get_session),
):
    month_start_date = date_str_to_date(date)
    statement = (
        select(Rate)
        .where(Rate.user_id == user_id)
        .where(Rate.client_id == client_id)
        .where(Rate.valid_from <= month_start_date)
        .where(Rate.valid_to > month_start_date)
    )
    result = session.exec(statement).all()
    return result


# Activate rate
@router.put("/{rate_id}/activate")
async def activate_rate(
    rate_id: str,
    session: Session = Depends(get_session),
):
    statement = select(Rate).where(Rate.id == rate_id)
    rate_to_activate = session.exec(statement).one()
    rate_to_activate.is_active = True
    rate_to_activate.updated_at = datetime.now()
    session.add(rate_to_activate)
    session.commit()
    session.refresh(rate_to_activate)
    return rate_to_activate


# Deactivate rate
@router.put("/{rate_id}/deactivate")
async def deactivate_rate_id(
    rate_id: str = None,
    session: Session = Depends(get_session),
):
    statement = select(Rate).where(Rate.id == rate_id)
    rate_id_to_deactivate = session.exec(statement).one()
    rate_id_to_deactivate.is_active = False
    rate_id_to_deactivate.updated_at = datetime.now()
    session.add(rate_id_to_deactivate)
    session.commit()
    session.refresh(rate_id_to_deactivate)
    return rate_id_to_deactivate


# Update rates
@router.put("/")
async def update_rates(
    user_id: str = None,
    client_id: str = None,
    new_amount: str = None,
    session: Session = Depends(get_session),
):
    statement = (
        select(Rate)
        .where(Rate.user_id == user_id)
        .where(Rate.client_id == client_id)
        .where(Rate.is_active == True)
    )
    rate_to_update = session.exec(statement).one()
    rate_to_update.amount = new_amount
    session.add(rate_to_update)
    session.commit()
    session.refresh(rate_to_update)
    return True
