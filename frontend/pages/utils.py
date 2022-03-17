# pages shared logic goes here

import requests
from config import base_url
from typing import TypedDict, Callable, List
from datetime import datetime
from idom import component


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

days_in_month_list = []
days_in_month_nr = range(1, 32)
for n in days_in_month_nr:
    days_in_month_list.append(n)


capacity_days_list = []
capacity_days_nr = range(1, 21)
for n in capacity_days_nr:
    capacity_days_list.append(n)


def days_list(days: int) -> List:
    days_list = []
    days_nr = range(1, (days + 1))
    for n in days_nr:
        days_list.append(n)
    return days_list


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


def switch_state(value: bool, set_value: Callable):
    if value == True:
        set_value(False)
    elif value == False:
        set_value(True)
    return True
