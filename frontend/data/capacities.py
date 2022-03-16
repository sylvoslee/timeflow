import requests
import json
from config import base_url
from typing import List, TypedDict, Dict
from data.common import Select
from pages.utils import capacity_days_list
from datetime import datetime


class Capacity(TypedDict):
    user_id: int
    team_id: int
    year: int
    month: int
    days: int
    created_at: datetime
    updated_at: datetime
    is_locked: bool


def to_capacity(user_id: int, team_id: int, year_month: str, days: int) -> bool:
    data = Capacity(
        user_id=user_id,
        team_id=team_id,
        year=int(year_month[:4]),
        month=int(year_month[5:7]),
        days=days,
        created_at=str(datetime.now()),
        updated_at=str(datetime.now()),
        is_locked=False,
    )

    response = requests.post(
        f"{base_url}/api/capacities",
        data=json.dumps(dict(data)),
        headers={"accept": "application/json", "Content-Type": "application/json"},
    )
    return True


def capacities_by_user_team_year_month(user_id, team_id, year_month) -> List[Dict]:
    if user_id != "" and team_id != "" and year_month != "":
        api = f"{base_url}/api/capacities/"
        params = {
            "user_id": user_id,
            "team_id": team_id,
            "year": int(year_month[:4]),
            "month": int(year_month[5:7]),
        }

        response = requests.get(api, params=params)
        rows = []
        for item in response.json():
            d = {
                "capacity id": item["capacity_id"],
                "user": item["user_short_name"],
                "team": item["team_short_name"],
                "year": item["year"],
                "month": item["month"],
                "capacity days": item["days"],
            }
            rows.append(d)
        print(rows)
        return rows


def capacity_days() -> List[Dict]:
    days = [Select(value="", display_value="select capacity days")]
    for item in capacity_days_list:
        d = Select(value=item, display_value=item)
        days.append(d)
    return days


def capacity_deletion(capacity_to_delete) -> bool:
    api = f"{base_url}/api/capacities/?capacity_id={capacity_to_delete}"
    response = requests.delete(api)
    return True
