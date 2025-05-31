import json
from sports_api.schemas import Player
from dataclasses import asdict
import logging
import re
import os

logger = logging.getLogger(__name__)


def sanitize_filename(filename: str) -> str:
    return re.sub(r'[<>:"/\\|?*]', '_', filename)


def get_players():
    try:
        with open("../data/players.json", encoding="utf-8") as f:
            tmp = json.load(f)
    except Exception as e:
        logger.warning(f"Ошибка при чтении players.json: {e}")
        tmp = dict()

    players = dict()
    for player in tmp.values():
        players[int(player.get("id", 0))] = Player(
            id=int(player.get("id", 0)),
            name=player.get("name"),
            surname=player.get("surname"),
            number=player.get("number")
        )
    logger.info(f"Загружено игроков: {len(players)}")
    return players


def add_player(p: Player):
    try:
        with open("../data/players.json", "r", encoding="utf-8") as f:
            players = json.load(f)
    except Exception as e:
        logger.warning(f"Ошибка при чтении players.json для обновления: {e}")
        players = dict()

    players[p.id] = asdict(p)

    try:
        with open("../data/players.json", "w", encoding="utf-8") as f:
            json.dump(players, f, indent=4)
        logger.info(f"Игрок id={p.id} успешно добавлен/обновлён")
    except Exception as e:
        logger.error(f"Ошибка при записи players.json: {e}")


def save_data(fname, data):
    fname = sanitize_filename(fname)
    path = f"../data/{fname}.json"
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        logger.info(f"Данные сохранены в {path}")
    except Exception as e:
        logger.error(f"Ошибка при сохранении {path}: {e}")


def get_data(fname):
    fname = sanitize_filename(fname)
    path = f"../data/{fname}.json"
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        logger.info(f"Данные успешно загружены из {path}")
        return data
    except Exception as e:
        logger.error(f"Ошибка при загрузке {path}: {e}")
        return {}
