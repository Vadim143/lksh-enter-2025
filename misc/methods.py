import logging
from console_sol.models import *

logger = logging.getLogger(__name__)

def versus(p1, p2, matches, team_by_id):
    cnt = 0
    logger.debug(f"Начинаем подсчет встреч между игроками {p1} и {p2}")
    for match in matches:
        t1 = team_by_id[match.team1_id]
        t2 = team_by_id[match.team2_id]
        t1ps = t1.players
        t2ps = t2.players
        if (p1 in t1ps and p2 in t2ps) or (p2 in t1ps and p1 in t2ps):
            cnt += 1
            logger.debug(f"Матч ID={match.id}: игроки {p1} и {p2} встретились")
    logger.info(f"Игроки {p1} и {p2} встретились всего {cnt} раз(а)")
    return cnt


def get_stat(name, team_by_name, matches):
    logger.debug(f"Получаем статистику для команды '{name}'")
    if name not in team_by_name:
        logger.warning(f"Команда '{name}' не найдена в team_by_name")
        return 0, 0, 0

    id = team_by_name[name].id
    wins = loses = scored = missed = 0

    for match in matches:
        t1s = match.team1_score
        t2s = match.team2_score

        if match.team1_id == id:
            scored += t1s
            missed += t2s
            if t1s > t2s:
                wins += 1
            else:
                loses += 1
        elif match.team2_id == id:
            scored += t2s
            missed += t1s
            if t1s < t2s:
                wins += 1
            else:
                loses += 1

    goal_diff = scored - missed
    logger.info(f"Статистика для '{name}': выигрыши={wins}, поражения={loses}, разница голов={goal_diff}")
    return wins, loses, goal_diff
