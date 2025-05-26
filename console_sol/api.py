from sports_api.config import get_settings
import requests
from console_sol.models import *


base_url = "https://lksh-enter.ru"
settings = get_settings()
token = settings.token
headers = {"Authorization": token}


def get_json(url):
    response = requests.get(base_url + url, headers=headers)
    response.raise_for_status()
    return response.json()


def fetch_matches():
    matches = get_json("/matches")
    return matches


def fetch_teams():
    matches = get_json("/teams")
    return matches


def fetch_team(id):
    matches = get_json(f"/teams/{id}")
    return matches


def fetch_player(id):
    player = get_json(f"/players/{id}")
    return Player(id=player["id"], name=player["name"], surname=player.get("surname", None), number=player["number"])

