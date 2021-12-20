from fastapi import APIRouter
from models.forecast import Forecast
from models.client import Client
from models.user import User
from utils import *
from sqlmodel import Session, select, SQLModel


router = APIRouter(prefix="/api")
session = Session(engine)

@router.post("/forecasts")
async def forecast(forecast: Forecast):

    new_forecast = Forecast(
        id=forecast.id,
        user_id=forecast.user_id,
        epic_id=forecast.epic_id,
        client_id=forecast.client_id,
        days=forecast.days,
        month=forecast.month,
        year=forecast.year
    )

    session.add(new_forecast)
    session.commit()
    return True


@router.get("/forecasts/list")
async def get_forecasts_list(user_id: str = None, epic_id: str = None):
    if user_id != None:
        statement = (
            select(Forecast)
                .where(Forecast.user_id == user_id)
        )
    if epic_id != None:
        statement = (
            select(Forecast)
                .where(Forecast.epic_id == epic_id)
        )
    else:
        statement = select(Forecast)

    results = session.exec(statement).all()
    return results


@router.put("/forecasts/update")
async def update_forecasts(
    user_id: str = None,
    epic_id: str = None,
    month: int = None,
    year: int = None,
    days: float = None
):
    statement = (
        select(Forecast)
        .where(Forecast.user_id == user_id)
        .where(Forecast.epic_id == epic_id)
        .where(Forecast.month == month)
        .where(Forecast.year == year)
    )
    forecast_to_update = session.exec(statement).one()
    forecast_to_update.days = days
    session.add(forecast_to_update)
    session.commit()
    session.refresh(forecast_to_update)
    return True


@router.delete("/forecasts/delete")
async def delete_forecasts(
    user_id: str = None,
    epic_id: str = None,
    month: int = None,
    year: int = None
):
    statement = (
        select(Forecast)
        .where(Forecast.user_id == user_id)
        .where(Forecast.epic_id == epic_id)
        .where(Forecast.month == month)
        .where(Forecast.year == year)
    )
    results = session.exec(statement)
    forecast_to_delete = results.one()
    session.delete(forecast_to_delete)
    session.commit()
