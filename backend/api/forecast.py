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
async def list_clients(list_name: str):
    if list_name == "clients":
        statement = select(Forecast.id, 
                            Forecast.user_id,
                            Forecast.epic_id,
                            Client.id,
                            Forecast.days, 
                            Forecast.month,
                            Forecast.year).select_from(Forecast)
        results = session.exec(statement).all()
        return results
    else:
        return False
