import requests
from config import base_url
from components.input import Selector2, SelectorDropdownKeyValue
from data.common import Select


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
    print("rows are", rows)
    selector_user_name = Selector2(set_value=set_user_id, data=rows)
    return selector_user_name
