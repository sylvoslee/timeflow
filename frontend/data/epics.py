import requests
import json
from typing import List, TypedDict
from datetime import datetime, date

from config import base_url
from data.common import Select
from components.input import Selector, SelectorDropdownKeyValue


class Epic(TypedDict):
    short_name: str
    name: str
    team_id: int
    sponsor_id: int
    start_date: str
    is_active: bool
    created_at: str
    updated_at: str


def to_epic(
    short_name: str,
    name: str,
    team_id: int,
    sponsor_id: int,
    start_date: str,
    is_active: bool,
    created_at: str,
    updated_at: str,
):
    """Posts data to epics table

    Args:
        short_name (str): new epic's short name
        name (str): new epic's full name
        team_id (int): team id new epic is for
        sponsor_id (int): sponsor id new epic is for
        start_date (str): date of epic's start
        is_active (bool): set to True on post
        created_at (str): datetime string of when the epic was created
        updated_at (str): datetime string of when the epic was updated
    """
    data = Epic(
        short_name=short_name,
        name=name,
        team_id=team_id,
        sponsor_id=sponsor_id,
        start_date=start_date,
        is_active=is_active,
        created_at=created_at,
        updated_at=updated_at,
    )
    respone = requests.post(
        f"{base_url}/api/epics",
        data=json.dumps(dict(data)),
        headers={"accept": "application/json", "Content-Type": "application/json"},
    )
    return True


def epic_dropdown(set_epic_id):
    """Return a dropdown list that allows for the selection of a single epic"""
    # Connect to active epics endpoint
    api_epic_name = f"{base_url}/api/epics/active"
    response_epic_name = requests.get(api_epic_name)

    # Create dropdown of active epics which can then be selected
    epic_name_rows = [{item["name"]: item["id"]} for item in response_epic_name.json()]
    epic_name_dropdown_list = SelectorDropdownKeyValue(rows=epic_name_rows)
    selector_epic_name = Selector(
        set_value=set_epic_id,
        placeholder="Select Epic",
        dropdown_list=epic_name_dropdown_list,
    )
    return selector_epic_name


def epics_names() -> List[Select]:
    """Gets list of active epics by name and id
    Returns a list of dictionaries
    """
    api_epic_name = f"{base_url}/api/epics/active"
    response_epic_name = requests.get(api_epic_name)
    epic_name_rows = [Select(value="", display_value="select epic")]
    for item in response_epic_name.json():
        d = Select(value=item["id"], display_value=item["name"])
        epic_name_rows.append(d)
    return epic_name_rows


def epics_by_team_sponsor(team_id: int, sponsor_id: int) -> List[Select]:
    """gets epics by team and sponsor

    Args:
        team_id (int): id of the team an epic is filtered with
        sponsor_id (int): id of the sponsor an epic is filtered with
    """
    api = f"{base_url}/api/epics/teams/{team_id}/sponsors/{sponsor_id}/"
    response = requests.get(api)
    rows = []
    for item in response.json():
        d = {
            "epic id": item["epic_id"],
            "epic name": item["epic_name"],
            "start date": item["start_date"],
            "team name": item["team_name"],
            "sponsor name": item["sponsor_short_name"],
        }
        rows.append(d)
    return rows


def client_name_by_epic_id(epic_id) -> Select:
    """Gets client name by given id"""
    api_client_name_id = f"{base_url}/api/epics/{epic_id}/client-name"
    response_client_name_id = requests.get(api_client_name_id)
    r = response_client_name_id.json()
    client_name = r.get("client_name")
    client_id = r.get("client_id")
    d = Select(value=client_id, display_value=client_name)
    return d
