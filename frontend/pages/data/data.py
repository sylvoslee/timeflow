import requests
from config import base_url
from typing import List, Dict, TypedDict
from pages.utils import (
    year_month_list,
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


def rates_by_user_client_date(user_id: int, client_id: int, date: str) -> List[Dict]:
    if user_id != "" and client_id != "" and date != "":
        api = f"{base_url}/api/rates/users/{user_id}/clients/{client_id}/months/?date={date}"
        response = requests.get(api)
        rows = []
        for item in response.json():
            d = {
                "valid from": item["valid_from"],
                "valid_to": item["valid_to"],
                "amount": item["amount"],
            }
            rows.append(d)
        return rows


def rate_active_by_user_client(user_id: int, client_id: int) -> List[Dict]:
    api = f"{base_url}/api/rates/users/{user_id}/clients/{client_id}/active"
    print(api)
    response = requests.get(api)
    print(response)
    rows = []
    for item in response.json():
        d = {
            "valid from": item["valid_from"],
            "valid_to": item["valid_to"],
            "amount": item["amount"],
        }
        rows.append(d)
    return rows


def rate_update(user_id: int, client_id: int, new_amount: float):
    api = f"{base_url}/api/rates/?user_id={user_id}&client_id={client_id}&new_amount={new_amount}"
    response = requests.put(api)
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
