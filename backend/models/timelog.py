from sqlite3.dbapi2 import Timestamp, adapt
from typing import Optional
from sqlmodel import Field, SQLModel, Field
from pydantic import validator, root_validator, ValidationError
from datetime import datetime, timedelta
from ..utils import string_to_datetime_hm


# {
#   "user_id": 1,
#   "start_time": "2022-01-19T08:30:00.000Z",
#   "end_time": "2022-01-19T09:30:00.000Z",
#   "client_id": 1,
#   "epic_id": 1,
#   "count_hours": 0,
#   "count_days": 0,
#   "month": 0,
#   "year": 0
# }


class TimeLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    start_time: str
    end_time: str
    client_id: int = Field(foreign_key="client.id")
    epic_id: int = Field(foreign_key="epic.id")
    count_hours: float
    count_days: float
    month: int
    year: int

    @root_validator(pre=True)
    def check_time_delta(cls, values):
        assert (
            values["start_time"] < values["end_time"]
        ), "start_time must be smaller then end_time"
        return values

    # actually computed "month" field --> to be changed
    # @validator("month", always=True, pre=True)
    # def set_month(cls, month_value, values):
    #     start_time_dt = string_to_datetime(values["start_time"])
    #     month_value = start_time_dt.month
    #     return month_value

    # actually computed "year" field --> to be changed
    # @validator("year", always=True, pre=True)
    # def set_year(cls, year_value, values):
    #     start_time_dt = string_to_datetime(values["start_time"])
    #     year_value = start_time_dt.year
    #     return year_value

    # actually computed "count_hours" field --> to be changed
    @root_validator(pre=True)
    def count_hours_compute(cls, values):
        delta = string_to_datetime_hm(values["end_time"]) - string_to_datetime_hm(
            values["start_time"]
        )
        work_delta_hours = delta.total_seconds() / 3600
        work_hours = "{:.2f}".format(work_delta_hours)
        values["count_hours"] = work_hours
        return values

    # actually computed "count_days" field --> to be changed
    @root_validator(pre=True)
    def count_days_compute(cls, values):
        delta = string_to_datetime_hm(values["end_time"]) - string_to_datetime_hm(
            values["start_time"]
        )
        work_delta_days = delta.total_seconds() / 3600 / 8
        work_days = "{:.2f}".format(work_delta_days)
        values["count_days"] = work_days
        return values

    @validator("count_hours", always=True)
    def daily_hours(cls, hours_input):
        assert hours_input < 12, "user worked over 12 hours"
        return hours_input

    @validator("year", always=True)
    def valid_year(cls, year_input):
        assert year_input in range(
            2021, datetime.now().year + 1
        ), "year value not in range [2021, current year]"
        return year_input
