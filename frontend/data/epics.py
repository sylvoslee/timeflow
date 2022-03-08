import requests
from typing import List
from config import base_url
from data.common import Select
from components.input import Selector, SelectorDropdownKeyValue


def epic_dropdown(set_epic_id):
    """Return a dropdown list that allows for the selection of a single epic"""
    # Connect to active epics endpoint
    api_epic_name = f"{base_url}/api/epics/active"
    response_epic_name = requests.get(api_epic_name)

    # Create dropdown of active epics which can then be selected
    epic_name_rows = [{item["name"]: item["id"]} for item in response_epic_name.json()]
    epic_name_dropdown_list = SelectorDropdownKeyValue(rows=epic_name_rows)
    selector_epic_name = Selector(
        set_value=set_epic_id,
        placeholder="Select Epic",
        dropdown_list=epic_name_dropdown_list,
    )
    return selector_epic_name


def epics_names() -> List[Select]:
    api_epic_name = f"{base_url}/api/epics/active"
    response_epic_name = requests.get(api_epic_name)
    epic_name_rows = [Select(value="", display_value="select epic")]
    for item in response_epic_name.json():
        d = Select(value=item["id"], display_value=item["name"])
        epic_name_rows.append(d)
    return epic_name_rows


def client_name_by_epic_id(epic_id) -> Select:
    api_client_name_id = f"{base_url}/api/epics/{epic_id}/client-name"
    response_client_name_id = requests.get(api_client_name_id)
    r = response_client_name_id.json()
    client_name = r.get("name")
    client_id = r.get("id_1")
    d = Select(value=client_id, display_value=client_name)
    return d
