import requests
from config import base_url
from typing import List, Dict, TypedDict
from pages.utils import (
    year_month_list,
    forecast_days_list,
    timelog_days_list,
    hours_list,
    month_start_list,
)
import json
from datetime import datetime


class Select(TypedDict):
    value: str
    dispay_value: str


class Forecast(TypedDict):
    user_id: int
    epic_id: int
    month: int
    year: int
    days: int


class Timelog(TypedDict):
    start_time: str
    end_time: str
    user_id: int
    epic_id: int
    count_hours: float
    count_days: float
    month: int
    year: int


class Rate(TypedDict):
    user_id: int
    client_id: int
    valid_from: str
    valid_to: str
    amount: float
    created_at: datetime
    updated_at: datetime
    is_active: bool


def to_timelog(
    start_time: str,
    end_time: str,
    user_id: int,
    epic_id: int,
    count_hours: float,
    count_days: float,
    month: int,
    year: int,
) -> bool:
    data = Timelog(
        start_time=start_time,
        end_time=end_time,
        user_id=user_id,
        epic_id=epic_id,
        count_hours=0,
        count_days=0,
        month=str(month),
        year=str(year),
    )
    response = requests.post(
        f"{base_url}/api/timelogs",
        data=json.dumps(dict(data)),
        headers={"accept": "application/json", "Content-Type": "application/json"},
    )
    return True


def to_forecast(user_id: int, epic_id: int, month: str, year: str, days: int) -> bool:
    data = Forecast(
        user_id=user_id,
        epic_id=epic_id,
        month=int(month),
        year=int(year),
        days=days,
    )
    print(dict(data))
    response = requests.post(
        f"{base_url}/api/forecasts",
        data=json.dumps(dict(data)),
        headers={"accept": "application/json", "Content-Type": "application/json"},
    )
    return True

    # user_id=user_id,
    # client_id=client_id,
    # valid_from=str(selected_date),
    # valid_to=str(far_date),
    # amount=amount,
    # created_at=str(datetime.now()),
    # updated_at=str(datetime.now()),
    # is_active=True,


def to_rate(
    user_id: int,
    client_id: int,
    valid_from: str,
    valid_to: str,
    amount: float,
    created_at: str,
    updated_at: str,
    is_active: bool,
) -> bool:
    data = Rate(
        user_id=user_id,
        client_id=client_id,
        valid_from=valid_from,
        valid_to=valid_to,
        amount=amount,
        created_at=created_at,
        updated_at=updated_at,
        is_active=True,
    )
    print(data)
    response = requests.post(
        f"{base_url}/api/rates",
        data=json.dumps(dict(data)),
        headers={"accept": "application/json", "Content-Type": "application/json"},
    )
    return True


def username() -> List[Select]:
    api_username = f"{base_url}/api/users"
    response_username = requests.get(api_username)
    username_rows = [Select(value="", display_value="select username")]
    for item in response_username.json():
        d = Select(value=item["id"], display_value=item["username"])
        username_rows.append(d)
    return username_rows


def epics_names() -> List[Select]:
    api_epic_name = f"{base_url}/api/epics/active"
    response_epic_name = requests.get(api_epic_name)
    epic_name_rows = [Select(value="", display_value="select epic")]
    for item in response_epic_name.json():
        d = Select(value=item["id"], display_value=item["name"])
        epic_name_rows.append(d)
    return epic_name_rows


def clients_names() -> List[Select]:
    api_client_name = f"{base_url}/api/clients/active"
    response_client_name = requests.get(api_client_name)
    client_name_rows = [Select(value="", display_value="select client")]
    for item in response_client_name.json():
        d = Select(value=item["id"], display_value=item["name"])
        client_name_rows.append(d)
    return client_name_rows


def client_name_by_epic_id(epic_id) -> Select:
    api_client_name_id = f"{base_url}/api/epics/{epic_id}/client-name"
    response_client_name_id = requests.get(api_client_name_id)
    r = response_client_name_id.json()
    client_name = r.get("name")
    client_id = r.get("id_1")
    d = Select(value=client_id, display_value=client_name)
    return d


def year_month_dict_list() -> List[Dict]:
    ym_dict_list = [Select(value="", display_value="select month")]
    for item in year_month_list:
        d = Select(value=item, display_value=item)
        ym_dict_list.append(d)
    return ym_dict_list


def forecast_days() -> List[Dict]:
    days = [Select(value="", display_value="select days")]
    for item in forecast_days_list:
        d = Select(value=item, display_value=item)
        days.append(d)
    return days


def forecast_by_user_epic_year_month(user_id, epic_id, year, month) -> List[Dict]:
    if user_id != "" and epic_id != "" and year != "" and month != "":
        api = f"{base_url}/api/forecasts/users/{user_id}/epics/{epic_id}/year/{year}/month/{month}"
        response = requests.get(api)
        rows = []
        for item in response.json():
            d = {
                "forecast id": item["id"],
                "year": item["year"],
                "month": item["month"],
                "days": item["days"],
            }
            rows.append(d)
        print(rows)
        return rows


def forecast_deletion(forecast_to_delete) -> bool:
    api = f"{base_url}/api/forecasts/?forecast_id={forecast_to_delete}"
    response = requests.delete(api)
    return True


def timelog_days() -> List[Dict]:
    days = [Select(value="", display_value="select days")]
    for item in timelog_days_list:
        d = Select(value=item, display_value=item)
        days.append(d)
    return days


def hours() -> List[Dict]:
    hours = [Select(value="", display_value="select hour")]
    for item in hours_list:
        d = Select(value=item, display_value=item)
        hours.append(d)
    return hours


def months_start() -> List[Dict]:
    months = [Select(value="", display_value="select start date")]
    for item in month_start_list:
        d = Select(value=item, display_value=item)
        months.append(d)
    return months
