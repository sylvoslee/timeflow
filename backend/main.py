from fastapi import *
from sqlmodel import Session, select, SQLModel
from sqlalchemy.exc import OperationalError
from backend.models.timelog import TimeLog
from backend.models.calendar import Calendar
from backend.utils import engine, create_db
from datetime import datetime
from backend.api import user, timelog, forecast, epic, client, rate
from .utils import tags_metadata
import pandas as pd
from pandas import Timestamp

app = FastAPI(title="timesheets app API", openapi_tags=tags_metadata)

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


@app.on_event("startup")
def implement_calendar_table():
    calendar_from_csv = pd.read_csv("backend/calendar.csv")
    calendar_from_csv.to_sql("calendar", con=engine, if_exists="replace")
