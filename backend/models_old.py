from sqlite3.dbapi2 import Timestamp, adapt
from typing import Optional
from sqlmodel import Field, SQLModel, Field
from pydantic import validator
from datetime import datetime


class Forecast(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    epic_id: int = Field(foreign_key="epic.id")
    work_days: float
    month: int
    year: int

    @validator("year")
    def valid_year(cls, year_input):
        assert year_input >= datetime.now().years
        return year_input

    @validator("month")
    def valid_month(cls, month_input):
        if month_input not in range(1, 13):
            # or  (month_input < datetime.now().month
            # or (month_input < datetime.now().month and Forecast.year == datetime.now().year + 1)):
            raise TypeError("Month is not valid")
        return month_input

    @validator("work_days")
    def valid_work_days(cls, work_days_input):
        assert work_days_input in range(0, 24), "Work days cannot be greater than 24"
        return work_days_input
