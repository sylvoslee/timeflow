
from sqlite3.dbapi2 import Timestamp, adapt
from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import validator
from datetime import datetime

class Forecast(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    epic_id: int = Field(foreign_key="epic.id")
    client_id: int = Field(foreign_key="client.id")
    days: float
    month: int
    year: int

    # __table_args__ = {'extend_existing': True}

    @validator("days")
    def valid_days(cls, days_input):
        assert days_input in range(0, 24), "Work days cannot be greater than 24"
        return days_input
