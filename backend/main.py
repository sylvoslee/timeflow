from fastapi import *
from sqlmodel import Session, select, SQLModel
from sqlalchemy.exc import OperationalError
from models import Epic, TimeLog, User, engine, create_db, Client
from utils import *
import datetime
from api import user, timelog

app = FastAPI()
session = Session(engine)
app.include_router(user.router)
app.include_router(timelog.router)


@app.on_event("startup")
def on_startup():
    try:
        statement = select(TimeLog)
        results = session.exec(statement)
    except OperationalError:
        create_db()


# Get full client list
@app.get("/api/clients")
async def clients():
    statement = select(Client.client_name)
    results = session.exec(statement).all()
    return results


# Get full epic_name list
@app.get("/api/epics")
async def epics():
    statement = select(Epic.epic_name)
    results = session.exec(statement).all()
    return results


# Post client
@app.post("/api/client/")
async def client(client: Client):
    session.add(client)
    session.commit()


# Post epic
@app.post("/api/epic/")
async def epic(epic: Epic):
    session.add(epic)
    session.commit()


@app.post("/api/forecast/")
async def forecast(forecast: Forecast):
    statement = select(User.id).where(User.id == forecast.user_id)
    results = session.exec(statement).first()

    startt_to_dt = string_to_datetime(timelog.start_time)

    new_forecast = Forecast(
        id=forecast.id,
        user_id=forecast.user_id,
        epic_id=forecast.epic_id,
        work_days=forecast.work_days,
        month=startt_to_dt.month,
        year=startt_to_dt.year,
    )

    session.add(new_forecast)
    session.commit()
    return "Hallo"
