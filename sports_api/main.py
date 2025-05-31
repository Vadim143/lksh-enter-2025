from fastapi import FastAPI, Request, APIRouter, UploadFile, File, HTTPException
from console_sol.api import *
from sports_api.routers import *
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import logging
from datetime import datetime, timedelta
from apscheduler.triggers.date import DateTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sports_api.data_store import teams, matches, team_by_id, team_by_name

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] MAIN1 %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("main1.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI()

app.mount("/templates", StaticFiles(directory="templates"), name="templates")

app.include_router(front_router)
app.include_router(stats_router)
app.include_router(versus_router)
app.include_router(goals_router)

scheduler = AsyncIOScheduler()


def update_data():
    logger.debug("Начинаем обновление данных")

    teams.clear()
    teams.extend(fetch_teams())
    logger.debug(f"Обновлены teams: {len(teams)} записей")

    matches.clear()
    matches.extend(fetch_matches())
    logger.debug(f"Обновлены matches: {len(matches)} записей")


    team_by_id.clear()
    team_by_name.clear()
    for team in teams:
        team_by_name[team.name] = team
        team_by_id[team.id] = team
    logger.debug(f"Обновлены словари team_by_name ({len(team_by_name)}) и team_by_id ({len(team_by_id)})")

    scheduler.add_job(update_data, trigger=DateTrigger(datetime.now() + timedelta(seconds=300)))
    logger.info("Данные обновлены и запланировано следующее обновление")


if __name__ == "__main__":
    logger.info("Запуск планировщика и сервера")
    scheduler.start()
    update_data()
    uvicorn.run(app, host="127.0.0.1", port=80)
