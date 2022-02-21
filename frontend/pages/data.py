import requests
from config import base_url
from typing import List, Dict, TypedDict
from pages.utils import year_month_list, forecast_days_list
import json


class Select(TypedDict):
    value: str
    dispay_value: str


class Forecast(TypedDict):
    user_id: int
    epic_id: int
    client_id: int
    month: int
    year: int
    days: int


def to_forecast(
    user_id: int, epic_id: int, client_id: int, month: str, year: str, days: int
) -> bool:
    data = Forecast(
        user_id=user_id,
        epic_id=epic_id,
        client_id=client_id,
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


def username() -> List[Select]:
    api_username = f"{base_url}/api/users"
    response_username = requests.get(api_username)
    username_rows = []
    for item in response_username.json():
        d = Select(value=item["id"], display_value=item["username"])
        username_rows.append(d)
    return username_rows


def epics_names() -> List[Select]:
    api_epic_name = f"{base_url}/api/epics/active"
    response_epic_name = requests.get(api_epic_name)
    epic_name_rows = [Select(value="", display_value="select")]
    for item in response_epic_name.json():
        d = Select(value=item["id"], display_value=item["name"])
        epic_name_rows.append(d)
    return epic_name_rows


def client_name_by_epic_id(epic_id) -> Dict:
    api_client_name_id = f"{base_url}/api/epics/{epic_id}/client-name"
    response_client_name_id = requests.get(api_client_name_id)
    r = response_client_name_id.json()
    client_name = r.get("name")
    client_id = r.get("id_1")
    d = Select(value=client_id, display_value=client_name)
    return d


def year_month_dict_list() -> List[Dict]:
    ym_dict_list = []
    for item in year_month_list:
        d = Select(value=item, display_value=item)
        ym_dict_list.append(d)
    return ym_dict_list


def forecast_days() -> List[Dict]:
    days = []
    for item in forecast_days_list:
        d = Select(value=item, display_value=item)
        days.append(d)
    return days


# option = html.option({"value": f"{client_id}"}, client_name)
