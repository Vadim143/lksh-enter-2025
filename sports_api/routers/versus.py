from fastapi import FastAPI, Request, APIRouter, UploadFile, File, HTTPException

versus_router = APIRouter()


@versus_router.get("/versus")
def versus(request: Request, player1_id: int, player2_id: int):
    pass
