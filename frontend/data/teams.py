import requests
from config import base_url


def team_deactivation(name_to_deact) -> bool:
    api = f"{base_url}/api/teams/{name_to_deact}/deactivate"
    response = requests.put(api)
    return True


def team_activation(name_to_activ) -> bool:
    api = f"{base_url}/api/teams/{name_to_activ}/activate"
    response = requests.put(api)
    return True
