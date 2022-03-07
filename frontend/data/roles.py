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
            "short_name": item["short_name"],
            "full name": item["name"],
        }
        rows.append(d)
    return rows
