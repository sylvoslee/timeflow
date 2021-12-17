from fastapi import *
from sqlmodel import Session, select, SQLModel
from sqlalchemy.exc import OperationalError
from utils import engine, create_db
from models.user import User
from models.timelog import TimeLog
from models.epic import Epic
from models.client import Client
from utils import *
import datetime
from api import user, timelog, forecast, epic, client, rate

app = FastAPI()
session = Session(engine)
app.include_router(timelog.router)
app.include_router(forecast.router)
app.include_router(user.router)
app.include_router(epic.router)
app.include_router(client.router)
app.include_router(rate.router)


@app.on_event("startup")
def on_startup():
    try:
        statement = select(TimeLog)
        results = session.exec(statement)
    except OperationalError:
        create_db()
