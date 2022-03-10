import requests
import json
from typing import TypedDict
from datetime import datetime
from config import base_url
from components.input import Selector2, SelectorDropdownKeyValue
from data.common import Select


class User(TypedDict):
    short_name: str
    first_name: str
    last_name: str
    email: str
    role_id: int
    team_id: int
    start_date: str
    created_at: datetime
    updated_at: datetime
    is_active: bool


def to_user(
    short_name: str,
    first_name: str,
    last_name: str,
    email: str,
    role_id: str,
    team_id: str,
    year_month: str,
    day: int,
    created_at: datetime,
    updated_at: datetime,
):
    ym = year_month
    year = ym[:4]
    month = ym[5:7]
    start_date = year + "-" + month + "-" + day

    data = User(
        short_name=short_name,
        first_name=first_name,
        last_name=last_name,
        email=email,
        role_id=role_id,
        team_id=team_id,
        start_date=start_date,
        created_at=str(created_at),
        updated_at=str(updated_at),
        is_active=True,
    )
    response = requests.post(
        f"{base_url}/api/users",
        data=json.dumps(dict(data)),
        headers={"accept": "application/json", "Content-Type": "application/json"},
    )


def user_dropdown(set_user_id):
    """Return a dropdown list that allows for the selection of a single user"""

    # Connect to active users list endpoint
    api = f"{base_url}/api/users"
    response_user_name = requests.get(api)

    # Create a dropdown of users which can then be selected
    rows = [Select(display_value=" Select owner (user)", value="")]
    for item in response_user_name.json():
        d = Select(display_value=item["short_name"], value=item["id"])
        rows.append(d)
    selector_user_name = Selector2(set_value=set_user_id, data=rows)
    return selector_user_name
