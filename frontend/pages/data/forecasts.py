import requests
import json

from config import base_url
from typing import List, Dict, TypedDict
from pages.data.data import Select, Forecast
from pages.utils import forecast_days_list


class Forecast(TypedDict):
    user_id: int
    epic_id: int
    month: int
    year: int
    days: int


def forecast_by_user_epic_year_month(user_id, epic_id, year, month) -> List[Dict]:
    if user_id != "" and epic_id != "" and year != "" and month != "":
        api = f"{base_url}/api/forecasts/users/{user_id}/epics/{epic_id}/year/{year}/month/{month}"
        response = requests.get(api)
        rows = []
        for item in response.json():
            d = {
                "forecast id": item["id"],
                "year": item["year"],
                "month": item["month"],
                "days": item["days"],
            }
            rows.append(d)
        print(rows)
        return rows


def forecast_days() -> List[Dict]:
    days = [Select(value="", display_value="select days")]
    for item in forecast_days_list:
        d = Select(value=item, display_value=item)
        days.append(d)
    return days


def forecast_deletion(forecast_to_delete) -> bool:
    api = f"{base_url}/api/forecasts/?forecast_id={forecast_to_delete}"
    response = requests.delete(api)
    return True


def to_forecast(user_id: int, epic_id: int, month: str, year: str, days: int) -> bool:
    data = Forecast(
        user_id=user_id,
        epic_id=epic_id,
        month=int(month),
        year=int(year),
        days=days,
    )
    print(dict(data))
    response = requests.post(
        f"{base_url}/api/forecasts",
        data=json.dumps(dict(data)),
        headers={"accept": "application/json", "Content-Type": "application/json"},
    )
    return True

    # user_id=user_id,
    # client_id=client_id,
    # valid_from=str(selected_date),
    # valid_to=str(far_date),
    # amount=amount,
    # created_at=str(datetime.now()),
    # updated_at=str(datetime.now()),
    # is_active=True,
