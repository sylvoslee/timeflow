from fastapi import *
from sqlmodel import Session, select, SQLModel
from sqlalchemy.exc import OperationalError
from models_old import Epic, Client, Forecast
from utils import engine, create_db
from models.user import User
from models.timelog import TimeLog

# from models import user
from utils import *
import datetime
from api import user, timelog, forecast

app = FastAPI()
session = Session(engine)
app.include_router(user.router)
app.include_router(timelog.router)
app.include_router(forecast.router)


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
