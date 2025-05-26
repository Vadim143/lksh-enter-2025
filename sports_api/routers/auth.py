from fastapi import FastAPI, Request, APIRouter, UploadFile, File, HTTPException

auth_router = APIRouter()


@auth_router.post("/login")
def login(request: Request):
    pass
