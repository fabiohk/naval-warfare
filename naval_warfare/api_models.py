from pydantic import BaseModel

from naval_warfare.models import ShipDirection


class Players(BaseModel):
    player_1: str
    player_2: str


class Position(BaseModel):
    x: int
    y: int


class ShipOnBoard(BaseModel):
    game: int
    ship: str
    player: str
    front_position: Position
    direction: ShipDirection
