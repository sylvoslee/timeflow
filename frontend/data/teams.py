import requests
import json
from typing import List

from config import base_url
from datetime import datetime
from data.common import Select


def post_team(name: str, short_name: str, user_id: int):
    data = {
        "name": name,
        "short_name": short_name,
        "user_id": user_id,
        "is_active": True,
        "created_at": str(datetime.now()),
        "updated_at": str(datetime.now()),
    }
    response = requests.post(
        f"{base_url}/api/teams",
        data=json.dumps(data),
        headers={"accept": "application/json", "Content-Type": "application/json"},
    )
    return True


def get_active_team_rows():
    """Get all active teams and store them in a list."""
    api = f"{base_url}/api/teams/active"
    response = requests.get(api)

    rows = []
    for item in response.json():
        d = {
            "Team name": item["team_name"],
            "Team short name": item["team_short_name"],
            "User lead": item["user_name"],
        }
        rows.append(d)
    return rows


def teams_id_name(label="select team") -> List[Select]:
    """Gets list of teams by short_name and id

    get endpoint: /api/teams/active
    Returns:
        List[Select]: list of dictionaries
    """

    api = f"{base_url}/api/teams/active"
    response = requests.get(api)
    rows = [
        Select(value="", display_value=label),
        Select(value="", display_value="no team"),
    ]
    for item in response.json():
        d = Select(value=item["id"], display_value=item["team_short_name"])
        rows.append(d)
    return rows


def team_activation(name_to_activ) -> bool:
    api = f"{base_url}/api/teams/{name_to_activ}/activate"
    response = requests.put(api)
    return True


def team_deactivation(name_to_deact) -> bool:
    api = f"{base_url}/api/teams/{name_to_deact}/deactivate"
    response = requests.put(api)
    return True
