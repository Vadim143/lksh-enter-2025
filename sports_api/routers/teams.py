from fastapi import FastAPI, Request, APIRouter, UploadFile, File, HTTPException

teams_router = APIRouter()


@teams_router.get("/teams")
def teams(request: Request):
    pass


@teams_router.get("/teams/{id}")
def team(request: Request, id: int):
    pass
