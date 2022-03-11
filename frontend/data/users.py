import requests
from config import base_url
from data.common import Select
from typing import List


def users_names() -> List[Select]:
    # Connect to users list endpoint
    api_user_name = f"{base_url}/api/users"
    response_user_name = requests.get(api_user_name)
    user_name_rows = [Select(value="", display_value="select user")]
    for item in response_user_name.json():
        d = Select(value=item["id"], display_value=item["name"])
        user_name_rows.append(d)
    return user_name_rows
