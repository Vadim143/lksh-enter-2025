import logging
from fastapi import APIRouter, Request, HTTPException
from misc.methods import get_stat
from sports_api.data_store import teams as main_teams, matches as main_matches

logger = logging.getLogger(__name__)
stats_router = APIRouter()


@stats_router.get('/stats')
def stats(request: Request, team_name: str):
    logger.info(f"Запрос статистики для команды: {team_name}")

    # Используем кэшированные данные из data_store, чтобы не дергать fetch_matches() каждый раз,
    # так как fetch_matches() может быть тяжелым сетевым вызовом.
    team_by_name = {team.name: team for team in main_teams}

    if team_name not in team_by_name:
        logger.warning(f"Команда '{team_name}' не найдена")
        raise HTTPException(status_code=404, detail=f"Команда '{team_name}' не найдена")

    wins, loses, dif = get_stat(team_name, matches=main_matches, team_by_name=team_by_name)

    logger.info(f"Статистика для '{team_name}': wins={wins}, loses={loses}, dif={dif}")
    return {"wins": wins, "loses": loses, "dif": dif}
