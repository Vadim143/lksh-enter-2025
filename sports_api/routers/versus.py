import logging
from fastapi import APIRouter, Request, HTTPException
from misc.methods import versus
from sports_api.data_store import teams as main_teams, matches as main_matches

logger = logging.getLogger(__name__)
versus_router = APIRouter()

@versus_router.get('/versus')
def versus_stats(request: Request, player1_id: int, player2_id: int):
    logger.info(f"Запрос сравнения игроков: player1_id={player1_id}, player2_id={player2_id}")

    count = versus(player1_id, player2_id,
                   matches=main_matches,
                   team_by_id={team.id: team for team in main_teams})

    logger.info(f"Количество встреч между игроками {player1_id} и {player2_id}: {count}")

    return {"count": count}
