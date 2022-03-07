import requests
import json
from config import base_url
from datetime import datetime


def team_deactivation(name_to_deact) -> bool:
    api = f"{base_url}/api/teams/{name_to_deact}/deactivate"
    response = requests.put(api)
    return True


def team_activation(name_to_activ) -> bool:
    api = f"{base_url}/api/teams/{name_to_activ}/activate"
    response = requests.put(api)
    return True


def to_team(name: str, short_name: str, user_id: int):
    data = {
        "name": name,
        "short_name": short_name,
        "user_id": user_id,
        "is_active": True,
        "created_at": str(datetime.now()),
        "updated_at": str(datetime.now()),
    }
    print("here", data)
    response = requests.post(
        f"{base_url}/api/teams",
        data=json.dumps(data),
        headers={"accept": "application/json", "Content-Type": "application/json"},
    )
