import requests
from config import base_url
from typing import List
from data.common import Select
from components.input import Selector, SelectorDropdownKeyValue


def client_dropdown(set_client_id):
    # Connect to clients list endpoint
    api_client_name = f"{base_url}/api/clients"
    response_client_name = requests.get(api_client_name)

    # Create a dropdown of clients which can then be selected
    client_name_rows = [
        {item["name"]: item["id"]} for item in response_client_name.json()
    ]
    client_name_dropdown_list = SelectorDropdownKeyValue(rows=client_name_rows)
    selector_client_name = Selector(
        set_value=set_client_id,
        placeholder="Select Client",
        dropdown_list=client_name_dropdown_list,
    )
    return selector_client_name


def clients_names() -> List[Select]:
    api_client_name = f"{base_url}/api/clients/active"
    response_client_name = requests.get(api_client_name)
    client_name_rows = [Select(value="", display_value="select client")]
    for item in response_client_name.json():
        d = Select(value=item["id"], display_value=item["name"])
        client_name_rows.append(d)
    return client_name_rows
