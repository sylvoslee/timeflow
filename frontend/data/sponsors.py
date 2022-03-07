import requests
import json

from config import base_url
from datetime import datetime


def post_sponsor(name: str, short_name: str, client_id: int):
    data = {
        "name": name,
        "short_name": short_name,
        "client_id": client_id,
        "is_active": True,
        "created_at": str(datetime.now()),
        "updated_at": str(datetime.now()),
    }
    response = requests.post(
        f"{base_url}/api/sponsors",
        data=json.dumps(data),
        headers={"accept": "application/json", "Content-Type": "application/json"},
    )
