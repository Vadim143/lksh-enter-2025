from fastapi import FastAPI, Request, APIRouter, UploadFile, File, HTTPException
from fastapi.templating import Jinja2Templates

front_router = APIRouter()

templates = Jinja2Templates(directory="sports_api/templates")



@front_router.get("/front/stats")
def stats():
    pass


@front_router.get("/front/versus")
def versus():
    pass