import requests
from config import base_url
from typing import List
from data.common import Select


def clients_names() -> List[Select]:
    api_client_name = f"{base_url}/api/clients/active"
    response_client_name = requests.get(api_client_name)
    client_name_rows = [Select(value="", display_value="select client")]
    for item in response_client_name.json():
        d = Select(value=item["id"], display_value=item["name"])
        client_name_rows.append(d)
    return client_name_rows
