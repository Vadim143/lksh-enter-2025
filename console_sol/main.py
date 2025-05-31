import sys
import logging
from datetime import datetime, timedelta
from apscheduler.triggers.date import DateTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from console_sol.api import *
from console_sol.cache import *
from misc.methods import *

# Настройка логгера до любых логов
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] MAIN1 %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("main_console.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("main_console")

# Планировщик
scheduler = AsyncIOScheduler()
scheduler.start()

# Глобальные переменные
teams = []
matches = []
team_by_id = dict()
team_by_name = dict()


def update_data():
    logger.info("Обновление данных...")
    teams.clear()
    teams.extend(fetch_teams())

    matches.clear()
    matches.extend(fetch_matches())

    team_by_id.clear()
    team_by_name.clear()
    for team in teams:
        team_by_name[team.name] = team
        team_by_id[team.id] = team

    scheduler.add_job(update_data, trigger=DateTrigger(datetime.now() + timedelta(seconds=300)))
    logger.info("Данные успешно обновлены")


def convert_id(id):
    if id in cached_players:
        return cached_players[id]
    else:
        logger.info(f"Игрок id={id} не найден в кеше. Получаем из API...")
        player = fetch_player(id)
        add_player(player)
        return player


# Основная инициализация
update_data()

players = set()
for team in teams:
    for id in team.players:
        players.add(id)

cached_players = get_players()
players = sorted(map(convert_id, players), key=lambda x: [x.name, x.surname])

logger.info(f"Всего игроков: {len(players)}")
for player in players:
    print(f"{player.name} {player.surname}")

# Обработка пользовательского ввода
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        request, tmp = line.split("?")
        tmp = tmp.strip()
        request = request.strip()
        if request == 'stats':
            name = tmp[1:-1]
            wins, loses, dif = get_stat(name, team_by_name=team_by_name, matches=matches)
            print(wins, loses, f"{'+' if dif >= 0 else ''}{dif}")
        elif request == 'versus':
            p1, p2 = map(int, tmp.split())
            cnt = versus(p1, p2, team_by_id=team_by_id, matches=matches)
            print(cnt)
    except Exception as e:
        logger.warning(f"Ошибка при обработке ввода: {line} — {e}")
        print("Неверный запрос")
