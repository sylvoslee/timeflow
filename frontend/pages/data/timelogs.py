import requests
import json
from typing import List, Dict, TypedDict
from pages.utils import timelog_days_list
from pages.data.common import Select
from config import base_url


class Timelog(TypedDict):
    start_time: str
    end_time: str
    user_id: int
    epic_id: int
    count_hours: float
    count_days: float
    month: int
    year: int


def timelog_days() -> List[Dict]:
    days = [Select(value="", display_value="select days")]
    for item in timelog_days_list:
        d = Select(value=item, display_value=item)
        days.append(d)
    return days


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
