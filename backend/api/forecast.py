from fastapi import APIRouter, Depends
from ..utils import engine, get_session
from ..models.forecast import Forecast
from ..models.client import Client
from ..models.epic import Epic
from sqlmodel import Session, select, SQLModel, or_, and_
from sqlalchemy.exc import NoResultFound

router = APIRouter(prefix="/api/forecasts", tags=["forecast"])
session = Session(engine)


@router.post("/")
async def post_forecast(*, forecast: Forecast, session: Session = Depends(get_session)):
    statement = select(Forecast).where(
        and_(
            Forecast.epic_id == forecast.epic_id,
            Forecast.user_id == forecast.user_id,
            Forecast.year == forecast.year,
            Forecast.month == forecast.month,
            Forecast.days == forecast.days,
        )
    )
    try:
        result = session.exec(statement).one()
        return False
    except NoResultFound:
        session.add(forecast)
        session.commit()
        session.refresh(forecast)
        return forecast


@router.get("/")
async def get_forecasts(session: Session = Depends(get_session)):
    statement = select(Forecast)
    result = session.exec(statement).all()
    return result


@router.get("/{user_id}")
async def get_forecasts_users(
    user_id: str = None, session: Session = Depends(get_session)
):
    if user_id != None:
        statement = (
            select(
                Epic.name,
                Forecast.user_id,
                Forecast.month,
                Forecast.year,
                Forecast.days,
            )
            .join(Epic)
            .where(Forecast.user_id == user_id)
        )
        results = session.exec(statement).all()
        return results
    else:
        raise ValueError


# get forecast by user and epic
@router.get("/users/{user_id}/epics/{epic_id}")
async def get_forecasts_by_user_year_epic(
    user_id, epic_id, session: Session = Depends(get_session)
):
    statement = (
        select(Forecast.month, Forecast.days)
        .where(Forecast.user_id == user_id)
        .where(Forecast.epic_id == epic_id)
    )
    results = session.exec(statement).all()
    return results


# get forecast by user and month_year
@router.get("/users/{user_id}/epics/year/{year}/month/{month}")
async def get_forecasts_by_user_year_epic(
    user_id, year, month, session: Session = Depends(get_session)
):
    statement = (
        select(Epic.name, Forecast.year, Forecast.month, Forecast.days)
        .where(Forecast.user_id == user_id)
        .where(Forecast.year == year)
        .where(Forecast.month == month)
        .join(Epic)
    )
    results = session.exec(statement).all()
    return results


# get forecast by user, epic, year, month
@router.get("/users/{user_id}/epics/{epic_id}/year/{year}/month/{month}")
async def get_forecasts_by_user_year_epic(
    user_id, epic_id, year, month, session: Session = Depends(get_session)
):
    statement = (
        select(Forecast.id, Forecast.month, Forecast.year, Forecast.days)
        .where(Forecast.user_id == user_id)
        .where(Forecast.epic_id == epic_id)
        .where(Forecast.year == year)
        .where(Forecast.month == month)
    )
    results = session.exec(statement).all()
    return results


@router.put("/new-days")
async def update_forecasts(
    user_id: str = None,
    epic_id: str = None,
    month: int = None,
    year: int = None,
    days: float = None,
    session: Session = Depends(get_session),
):
    statement = select(Forecast).where(
        and_(
            Forecast.user_id == user_id,
            Forecast.epic_id == epic_id,
            Forecast.month == month,
            Forecast.year == year,
        )
    )
    forecast_to_update = session.exec(statement).one()
    forecast_to_update.days = days
    session.add(forecast_to_update)
    session.commit()
    session.refresh(forecast_to_update)
    return forecast_to_update


@router.delete("/")
async def delete_forecasts(
    forecast_id: str = None,
    session: Session = Depends(get_session),
):
    statement = select(Forecast).where(
        Forecast.id == forecast_id,
    )

    forecast_to_delete = session.exec(statement).one()
    session.delete(forecast_to_delete)
    session.commit()
    return True
