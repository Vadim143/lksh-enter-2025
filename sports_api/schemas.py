from pydantic import BaseModel
from typing import Optional


class Player(BaseModel):
    id: int
    name: str
    surname: Optional[str] = None
    number: int


class Match(BaseModel):
    id: int
    team1_id: int
    team2_id: int
    team1_score: int
    team2_score: int


class Team(BaseModel):
    id: int
    name: str
    players: list[int]
