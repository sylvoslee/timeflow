import json
import requests

from config import base_url
from datetime import datetime


def epic_area_activation(name_to_activ) -> bool:
    api = f"{base_url}/api/epic_areas/{name_to_activ}/activate"
    response = requests.put(api)
    return True


def epic_area_deactivation(name_to_deact) -> bool:
    api = f"{base_url}/api/epic_areas/{name_to_deact}/deactivate"
    response = requests.put(api)
    return True


def get_active_epic_area_rows():
    """Get all active epic areas and store them in a list."""
    api = f"{base_url}/api/epic_areas/active"
    response = requests.get(api)

    rows = []
    for item in response.json():
        d = {
            "Epic": item["epic_name"],
            "Epic Area": item["epic_area_name"],
            "ID": item["id"],
        }
        rows.append(d)
    return rows


def post_epic_area(epic_id: int, name: str):
    data = {
        "epic_id": epic_id,
        "name": name,
        "is_active": True,
        "created_at": str(datetime.now()),
        "updated_at": str(datetime.now()),
    }
    print("here", data)
    response = requests.post(
        f"{base_url}/api/epic_areas",
        data=json.dumps(data),
        headers={"accept": "application/json", "Content-Type": "application/json"},
    )
    return True
