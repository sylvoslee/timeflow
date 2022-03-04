# pages shared logic goes here

import requests
from config import base_url
from typing import TypedDict
from datetime import datetime


class Select(TypedDict):
    value: str
    dispay_value: str


# fmt: off
year_month_list = ["2022_01","2022_02","2022_03","2022_04","2022_05",
"2022_06","2022_07","2022_08","2022_09","2022_10","2022_11", "2022_12"
]
month_start_list = []
for date in year_month_list:
    month_start = date + "_01"
    month_start_list.append(month_start)

hours = ["07", "08", "09", "10", "11", "12", "13", "14", "15", "16", 
    "17", "18", "19", "20", "21", "22"]
quarters = ["00", "15", "30", "45"]
# fmt: on

forecast_days_list = []
forecast_days_nr = range(1, 30)
for n in forecast_days_nr:
    forecast_days_list.append(n)

timelog_days_list = []
timelog_days_nr = range(1, 32)
for n in timelog_days_nr:
    timelog_days_list.append(n)


hours_list = []
for h in hours:
    for q in quarters:
        hours = f"{h}:{q}"
        hours_list.append(hours)


def month_start_to_str(month_start):
    ms = month_start
    year = ms[:4]
    month = ms[5:7]
    day = ms[8:10]
    ms_str = year + "-" + month + "-" + day
    return ms_str


def date_str_to_date(date: str):
    date_date = datetime.strptime(date, "%Y-%m-%d").date()
    return date_date


far_date = date_str_to_date("9999-12-31")
