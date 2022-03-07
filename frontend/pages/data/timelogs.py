from typing import List, Dict, TypedDict
from pages.utils import timelog_days_list
from pages.data.data import Select


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
