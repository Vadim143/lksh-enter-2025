from fastapi import FastAPI, Request, APIRouter, UploadFile, File, HTTPException
from sports_api.routers import *
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.mount("/templates", StaticFiles(directory="sports_api/templates"), name="templates")
app.include_router(auth_router)
app.include_router(front_router)
app.include_router(matches_router)
app.include_router(players_router)
app.include_router(stats_router)
app.include_router(teams_router)
app.include_router(versus_router)




