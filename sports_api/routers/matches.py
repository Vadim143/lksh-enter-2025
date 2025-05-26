from fastapi import FastAPI, Request, APIRouter, UploadFile, File, HTTPException

matches_router = APIRouter()


@matches_router.get("/matches")
def matches(request: Request):
    pass