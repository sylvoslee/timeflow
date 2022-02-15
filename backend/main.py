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
    statement = select(Calendar).where(Calendar.id == 1)
    result = session.exec(statement).first()
    if result == None:
        calendar_from_excel = pd.read_excel("backend/calendar_id.xlsx")
        calendar_change_index = calendar_from_excel.set_index("date")
        calendar_change_index.to_sql("calendar", con=engine, if_exists="append")
