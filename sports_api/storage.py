from typing import TypedDict
from .schemas import *
import json
from pathlib import Path
from config import get_settings


class Db(TypedDict):
    players: dict[int, Player]
    matches: dict[int, Match]
    teams: dict[int, Team]


FILE = Path(get_settings().data_path)
FILE.parent.mkdir(parents=True, exist_ok=True)


def load():
    if FILE.exists():
        with FILE.open() as f:
            data = json.load(f)
            db = Db(players=data["players"], matches=data["matches"], teams=data["teams"])
            return db


def save(db: Db):
    with FILE.open(mode="w") as f:
        json.dump(db, f)
