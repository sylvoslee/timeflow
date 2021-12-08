from sqlite3.dbapi2 import Timestamp, adapt
from typing import Optional
from sqlmodel import Field, SQLModel, Field
from pydantic import validator
from datetime import datetime


class TimeLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    username: str
    start_time: str
    end_time: str
    client_id: int = Field(foreign_key="client.id")
    epic_id: int = Field(foreign_key="epic.id")
    epic_name: str
    work_hours: float
    daily_value: float
    month: int
    year: int
