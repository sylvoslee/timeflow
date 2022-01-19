from sqlite3.dbapi2 import Timestamp, adapt
from typing import Optional
from sqlmodel import Field, SQLModel, Field
from pydantic import validator, root_validator, ValidationError
from datetime import datetime, timedelta
from ..utils import string_to_datetime

# """
# {
#   "user_id": 1,
#   "start_time": "2022-01-19T08:30:00.000Z",
#   "end_time": "2022-01-19T09:30:00.000Z",
#   "client_id": 1,
#   "epic_id": 1,
#   "count_hours": 0,
#   "count_days": 0,
#   "daily_value": 0,
#   "month": 0,
#   "year": 0
# }
# """


class TimeLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    start_time: str
    end_time: str
    client_id: int = Field(foreign_key="client.id")
    epic_id: int = Field(foreign_key="epic.id")
    count_hours: float
    count_days: float
    daily_value: float
    month: int
    year: int

    # actually computed "month" field
    @validator("month", always=True, pre=True)
    def set_month(cls, month_value, values):
        start_time_dt = string_to_datetime(values["start_time"])
        month_value = start_time_dt.month
        return month_value

    # actually computed "year" field
    @validator("year", always=True, pre=True)
    def set_year(cls, year_value, values):
        start_time_dt = string_to_datetime(values["start_time"])
        year_value = start_time_dt.year
        return year_value

    @validator("end_time", always=True, pre=True)
    def check_time_delta(cls, v, values):
        if v <= values["start_time"]:
            raise ValueError("start_time is bigger or same as end_time")
        return v

    @root_validator
    def count_hours_change(cls, values):
        delta = string_to_datetime(values["end_time"]) - string_to_datetime(
            values["start_time"]
        )
        work_delta_hours = delta.total_seconds() / 3600
        work_hours = "{:.2f}".format(work_delta_hours)
        values["count_hours"] = work_hours
        return values

    @validator("year", always=True)
    def valid_year(cls, year_input):
        assert year_input >= datetime.now().year
        return year_input
