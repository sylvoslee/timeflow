from os import name
from fastapi import APIRouter
from ..models.forecast import Forecast
from ..models.client import Client
from ..models.user import User
from ..utils import engine
from sqlmodel import Session, select, SQLModel


router = APIRouter(prefix="/api/forecasts")
session = Session(engine)


@router.post("/")
async def forecast(forecast: Forecast):
    new_forecast = Forecast(
        id=forecast.id,
        user_id=forecast.user_id,
        epic_id=forecast.epic_id,
        client_id=forecast.client_id,
        days=forecast.days,
        month=forecast.month,
        year=forecast.year,
    )
    session.add(new_forecast)
    session.commit()
    return True


@router.get("/lists/{client_id}")
async def get_clients_list(client_id: str = None):
    if client_id != None:
        statement = select(Client.id
                            ,Client.name
                            ,Forecast.user_id
                            ,Forecast.month
                            ,Forecast.year
                            ,Forecast.days
                            ).join(Client).where(Client.id == client_id)
        results = session.exec(statement).all()
        return results
    else:
        raise ValueError


@router.get("/lists/{user_id}")
async def get_forecasts_list(user_id: str = None):
    if user_id != None:
        statement = select(Client.id
                            ,Client.name
                            ,Forecast.user_id
                            ,Forecast.month
                            ,Forecast.year
                            ,Forecast.days
                            ).join(Client).where(Forecast.user_id == user_id)
        results = session.exec(statement).all()
        return results
    else:
        raise ValueError


@router.put("/")
async def update_forecasts(
    user_id: str = None,
    epic_id: str = None,
    month: int = None,
    year: int = None,
    days: float = None,
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


@router.delete("/")
async def delete_forecasts(
    user_id: str = None, epic_id: str = None, month: int = None, year: int = None
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
