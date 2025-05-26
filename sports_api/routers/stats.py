from fastapi import FastAPI, Request, APIRouter, UploadFile, File, HTTPException

stats_router = APIRouter()


@stats_router.get("/stats")
def stats(request: Request, team_name: str):
    pass
