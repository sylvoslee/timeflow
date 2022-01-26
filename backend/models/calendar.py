from sqlite3.dbapi2 import Timestamp, adapt
from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import validator
from datetime import datetime


class Calendar(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime
    year_number: int
    year_name: str
    quarter_number: int
    quarter_name: str
    month_number: int
    month_name: str
    week_number: int
    week_name: str
    week_day_number: int
    week_day_name: str
