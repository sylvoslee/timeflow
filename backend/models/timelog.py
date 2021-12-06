from sqlite3.dbapi2 import Timestamp, adapt
from typing import Optional
from sqlmodel import Field, SQLModel, Field
from pydantic import validator
from datetime import datetime


class TimeLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    start_time: str
    end_time: str
    client_name: str
    epic_name: str
    work_hours: Optional[float]
    month: Optional[int]
    year: Optional[int]
