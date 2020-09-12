from typing import Dict

from fastapi import FastAPI

from naval_warfare.api_models import Players
from naval_warfare.game import DEFAULT_GAME_OPTION
from naval_warfare.game import Game
from naval_warfare.game import Player
from naval_warfare.game import prepare_game
from naval_warfare.game import retrieve_available_ships
from naval_warfare.game import start

app = FastAPI()

games_count = 0


@app.post("/new-game/", status_code=201)
def start_game(players: Players):
    global games_count
    games_count += 1
    player_1, player_2 = Player(players.player_1, game_option=DEFAULT_GAME_OPTION), Player(
        players.player_2, game_option=DEFAULT_GAME_OPTION
    )
    setattr(app, f"game_{games_count}", Game(player_1, player_2))
    return {"id": games_count}


@app.get("/available-ships/")
def get_available_ships():
    pass


@app.put("/ship-on-board/")
def put_ship_on_board():
    pass


@app.post("/play-game/")
def play_game():
    pass


@app.get("/game-result/")
def get_game_result():
    pass
