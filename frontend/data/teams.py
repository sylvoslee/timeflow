import requests
from config import base_url


def team_deactivation(name_to_deact) -> bool:
    api = f"{base_url}/api/teams/{name_to_deact}/deactivate"
    response = requests.put(api)
    return True
