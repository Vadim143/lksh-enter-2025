from sports_api.config import get_settings
import requests
from console_sol.models import *
from console_sol.cache import *
import logging
from dotenv import dotenv_values

logger = logging.getLogger(__name__)

config = dotenv_values("../.env")
base_url = "https://lksh-enter.ru"
token = config.get('TOKEN')
if not token:
    logger.critical("Переменная TOKEN не найдена в .env!")
    raise RuntimeError("Нет токена авторизации.")
headers = {"Authorization": token}


def get_json(url):
    full_url = base_url + url
    logger.info(f"GET запрос к {full_url}")
    response = requests.get(full_url, headers=headers)
    response.raise_for_status()
    logger.info(f"Ответ успешно получен от {full_url}")
    return response.json()


def fetch_matches():
    try:
        logger.info("Загрузка данных о матчах с API")
        tmp = get_json("/matches")
        save_data("matches", tmp)
    except Exception as e:
        logger.warning(f"Не удалось загрузить данные о матчах: {e}. Загрузка из кэша.")
        tmp = get_data("matches")

    matches = [
        Match(
            id=match.get("id"),
            team1_id=match.get("team1"),
            team2_id=match.get("team2"),
            team1_score=match.get("team1_score"),
            team2_score=match.get("team2_score")
        )
        for match in tmp
    ]
    logger.info(f"Загружено {len(matches)} матчей")
    return matches


def fetch_teams():
    try:
        logger.info("Загрузка данных о командах с API")
        tmp = get_json("/teams")
        save_data("teams", tmp)
    except Exception as e:
        logger.warning(f"Не удалось загрузить команды: {e}. Загрузка из кэша.")
        tmp = get_data("teams")

    teams = [
        Team(
            id=team.get("id"),
            name=team.get("name"),
            players=team.get("players")
        )
        for team in tmp
    ]
    logger.info(f"Загружено {len(teams)} команд")
    return teams


def fetch_team(id):
    try:
        logger.info(f"Загрузка команды с id={id} с API")
        team = get_json(f"/teams/{id}")
    except Exception as e:
        logger.warning(f"Не удалось загрузить команду id={id}: {e}. Поиск в кэше.")
        teams = get_data("teams")
        team = {}
        for t in teams:
            if t.id == id:
                team = t
                break
        if not team:
            logger.error(f"Команда с id={id} не найдена в кэше")
            return None

    return Team(id=team.get("id"), name=team.get("name"), players=team.get("players"))


def fetch_player(id):
    try:
        logger.info(f"Загрузка игрока с id={id} с API")
        player = get_json(f"/players/{id}")
        add_player(player)
    except Exception as e:
        logger.warning(f"Не удалось загрузить игрока id={id}: {e}. Загрузка из кэша.")
        player = get_players().get(f"{id}")
        if not player:
            logger.error(f"Игрок с id={id} не найден в кэше")
            return None

    return Player(
        id=player["id"],
        name=player["name"],
        surname=player.get("surname"),
        number=player["number"]
    )


def fetch_goals(id):
    logger.info("Загрузка голов")
    goals_json = get_data("goals")
    goals = []
    try:
        logger.info(f"Загрузка голов для матча id={id}")
        tmp = get_json(f"/goals?match_id={id}")
        goals_json.extend(tmp)
    except Exception as e:
        logger.warning(f"Ошибка при загрузке голов для матча id={match.id}: {e}")

    save_data("goals", goals_json)
    for goal in goals_json:
        if goal['match'] == id:
            goals.append(Goal(
                id=goal.get("id"),
                player=goal.get("player"),
                match=goal.get("match"),
                minute=goal.get("minute")
            ))
    logger.info(f"Загружено {len(goals)} голов")
    return goals
