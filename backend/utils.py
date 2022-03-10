from datetime import datetime
from sqlmodel import Session, SQLModel, create_engine, text
import sqlite3

database_loc = "backend/database.sqlite"
con_str = f"sqlite:///{database_loc}"

engine = create_engine(con_str, echo=True)
sqlite3_engine = sqlite3.connect(f"{database_loc}")


def get_session():
    session = Session(engine)
    return session


def create_db():
    SQLModel.metadata.create_all(engine)


def execute_sample_sql(session):
    """Read sample sql database and import it."""
    with open("backend/tests/sample.sql") as f:
        content = f.read()

    queries = filter(None, content.split(";\n"))
    queries = [text(query) for query in queries]

    for query in queries:
        session.exec(query)

    session.commit()
    session.expire_all()


session = Session(engine)

tags_metadata = [
    {
        "name": "user",
        "description": "Operations with users",
    },
    {
        "name": "epic",
        "description": "operations with epics",
    },
    {
        "name": "epic_area",
        "description": "operations with epic areas",
    },
    {
        "name": "team",
        "description": "operations with teams",
    },
    {
        "name": "sponsor",
        "description": "operations with sponsors",
    },
    {
        "name": "client",
        "description": "operations with clients",
    },
    {
        "name": "forecast",
        "description": "operations with forecasts",
    },
    {
        "name": "rate",
        "description": "operations with rates",
    },
    {
        "name": "timelog",
        "description": "operations with timelogs",
    },
]


def string_to_datetime(date_string):
    date = datetime.strptime(date_string, "%Y-%m-%d %H:%M")
    return date


def string_to_datetime_hm(date_string):
    date = datetime.strptime(date_string, "%H:%M")
    return date


def string_to_datetime_GMT(date_string):
    date = datetime.strptime(date_string, "%a %b %d %Y %H:%M:%S %Z%z")
    return date


def string_to_datetime_work(date_string):
    date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    return date


def datetime_to_string(date_date):
    date_string = date_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return date_string


def time_period(time_of_start, time_of_end):
    starting_time = string_to_datetime_work(time_of_start)
    ending_time = string_to_datetime_work(time_of_end)
    working_time = ending_time - starting_time
    return working_time


def date_str_to_date(date: str):
    date_date = datetime.strptime(date, "%Y-%m-%d").date()
    return date_date


far_date = date_str_to_date("9999-12-31")
