from fastapi import FastAPI, Request, APIRouter
from fastapi.templating import Jinja2Templates
from console_sol.api import fetch_teams, fetch_matches
from dataclasses import asdict
import logging
from sports_api.data_store import teams as main_teams, matches as main_matches


logger = logging.getLogger(__name__)


templates = Jinja2Templates(directory="templates")
front_router = APIRouter()


@front_router.get("/front/stats")
def stats(request: Request):
    logger.info("Обработка запроса /front/stats")
    team_by_id = dict()
    team_by_name = dict()
    for team in main_teams:
        team_by_name[team.name] = asdict(team)
        team_by_id[team.id] = asdict(team)
    matches = list(map(asdict, main_matches))

    logger.info(f"Загружено матчей: {len(matches)}")

    return templates.TemplateResponse("stats.html",
                                      {"request": request, "matches": matches})


@front_router.get("/front/versus")
def versus(request: Request):
    logger.info("Обработка запроса /front/versus")
    team_by_id = dict()
    team_by_name = dict()
    for team in main_teams:
        team_by_name[team.name] = asdict(team)
        team_by_id[team.id] = asdict(team)
    matches = list(map(asdict, main_matches))

    logger.info(f"Загружено команд: {len(team_by_id)}, матчей: {len(matches)}")

    return templates.TemplateResponse("versus.html",
                                      {"request": request, "matches": matches, "ti": team_by_id, "tn": team_by_name})
