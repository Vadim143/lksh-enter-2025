import logging
from fastapi import APIRouter, Request

from console_sol.api import fetch_goals
from sports_api.data_store import teams as main_teams, matches as main_matches

goals_router = APIRouter()
logger = logging.getLogger(__name__)


@goals_router.get('/goals')
def goals(request: Request, player_id: int):
    logger.info(f"Запрос голов для игрока с id={player_id}")
    player_goals = []
    team_id = 0
    for team in main_teams:
        if player_id in team.players:
            team_id = team.id
    for match in main_matches:
        if match.team1_id == team_id or match.team2_id == team_id:
            for goal in fetch_goals(match.id):
                if goal.player == player_id:
                    player_goals.append({"match": goal.match, "time": goal.minute})
    logger.info(f"Найдено голов: {len(player_goals)} для игрока id={player_id}")
    return player_goals
