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
