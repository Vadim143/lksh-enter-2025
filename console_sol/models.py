from dataclasses import dataclass
from typing import Optional


@dataclass
class Player:
    id: int
    number: int
    name: Optional[str] = None
    surname: Optional[str] = None


@dataclass
class Match:
    id: int
    team1_id: int
    team2_id: int
    team1_score: int
    team2_score: int


@dataclass
class Team:
    id: int
    name: str
    players: list[int]
