import requests
import json
from config import base_url
from typing import List, Dict, TypedDict
from datetime import datetime


class Role(TypedDict):
    short_name: str
    name: str
    created_at: datetime
    updated_at: datetime
    is_active: bool


def to_role(
    short_name: str,
    name: str,
    created_at: datetime,
    updated_at: datetime,
    is_active: bool,
) -> bool:
    data = Role(
        short_name=short_name,
        name=name,
        created_at=created_at,
        updated_at=updated_at,
        is_active=True,
    )
    response = requests.post(
        f"{base_url}/api/roles",
        data=json.dumps(dict(data)),
        headers={"accept": "application/json", "Content-Type": "application/json"},
    )
    return True


def roles_active():
    api = f"{base_url}/api/roles/active"
    response = requests.get(api)
    data = response.json()
    rows = []
    for item in data:
        d = {
            "id": item["id"],
            "full name": item["name"],
            "short_name": item["short_name"],
        }
        rows.append(d)
    return rows


def role_update(id: int, new_name: str = None, new_short_name: str = None) -> bool:
    if new_name != "" and new_short_name != "":
        api = f"{base_url}/api/roles/?id={id}&new_name={new_name}&new_short_name={new_short_name}"
    elif new_name != "" and new_short_name == "":
        api = f"{base_url}/api/roles/?id={id}&new_name={new_name}"
    elif new_name == "" and new_short_name != "":
        api = f"{base_url}/api/roles/?id={id}&new_short_name={new_short_name}"
    response = requests.put(api)
    return True
