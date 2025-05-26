from fastapi import FastAPI, Request, APIRouter, UploadFile, File, HTTPException

players_router = APIRouter()


@players_router.get("/players")
def players(request: Request):
    pass


@players_router.get("/players/{id}")
def player(request: Request, id: int):
    pass


@players_router.get("/goals")
def goals(request: Request, player_id: int):
    pass

