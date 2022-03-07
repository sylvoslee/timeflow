import requests
from config import base_url
from components.input import Selector, SelectorDropdownKeyValue


def user_dropdown(set_user_id):
    """Return a dropdown list that allows for the selection of a single user"""

    # Connect to active users list endpoint
    api_user_name = f"{base_url}/api/users"
    response_user_name = requests.get(api_user_name)

    # Create a dropdown of users which can then be selected
    user_name_rows = [{item["name"]: item["id"]} for item in response_user_name.json()]
    user_name_dropdown_list = SelectorDropdownKeyValue(rows=user_name_rows)
    selector_user_name = Selector(
        set_value=set_user_id,
        placeholder="Select Leader (User)",
        dropdown_list=user_name_dropdown_list,
    )
