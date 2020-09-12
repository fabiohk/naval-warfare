from pydantic import BaseModel


class Players(BaseModel):
    player_1: str
    player_2: str
