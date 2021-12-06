from sqlite3.dbapi2 import Timestamp, adapt
from typing import Optional
from sqlmodel import Field, SQLModel, Field
from pydantic import validator
from datetime import datetime


class TimeLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(foreign_key="user.id")
    start_time: str
    end_time: str
    client_id: str = Field(foreign_key="client.id")
    epic_id: str = Field(foreign_key="epic.id")
    work_hours: float
    month: int
    year: int
