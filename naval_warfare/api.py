import logging
from typing import Dict
from typing import List

from fastapi import FastAPI
from fastapi import Query

from naval_warfare.actions import place_ship_on_board
from naval_warfare.api_models import Players
from naval_warfare.api_models import ShipOnBoard
from naval_warfare.exceptions import UnknownGame
from naval_warfare.exceptions import UnknownPlayer
from naval_warfare.exceptions import UnknownShip
from naval_warfare.game import DEFAULT_GAME_OPTION
from naval_warfare.game import Game
from naval_warfare.game import Player
from naval_warfare.game import retrieve_available_ships
from naval_warfare.game import start
from naval_warfare.models import Position
from naval_warfare.models import Ship

logger = logging.getLogger(__name__)

app = FastAPI()

games_count = 0


@app.post("/new-game/", status_code=201)
def start_game(players: Players) -> Dict[str, int]:
    logger.info("Starting a new game!")

    global games_count
    games_count += 1
    player_1, player_2 = Player(players.player_1, game_option=DEFAULT_GAME_OPTION), Player(
        players.player_2, game_option=DEFAULT_GAME_OPTION
    )
    setattr(app, f"game_{games_count}", Game(player_1, player_2))

    logger.info("Game %s started!", games_count)
    return {"id": games_count}


@app.get("/available-ships/")
def get_available_ships(
    game_id: int = Query(..., alias="game", description="The player game ID", title="Game ID"),
    player_name: str = Query(
        ..., alias="player", description="The player name to retrieve available ships", title="Player Name"
    ),
) -> Dict[str, List[str]]:
    logger.info("Retrieving the available ships for player %s from game %s", player_name, game_id)

    game: Game = getattr(app, f"game_{game_id}", None)
    if not game:
        raise UnknownGame

    player = game.get_player(player_name)

    return {"available_ships": retrieve_available_ships(player.game_option)}


@app.put("/ship-on-board/", status_code=204)
def put_ship_on_board(ship_on_board: ShipOnBoard):
    game_id, player_name, ship, direction, front_position = (
        ship_on_board.game,
        ship_on_board.player,
        ship_on_board.ship,
        ship_on_board.direction,
        ship_on_board.front_position,
    )
    logger.info(
        "%s from game %s is trying to place the ship %s at (%s,%s) in a %s direction",
        player_name,
        game_id,
        ship,
        front_position.x,
        front_position.y,
        direction.value,
    )

    game: Game = getattr(app, f"game_{game_id}", None)
    if not game:
        raise UnknownGame

    player = game.get_player(player_name)

    try:
        chosen_ship = player.game_option[ship]
    except KeyError:
        raise UnknownShip

    place_ship_on_board(
        Ship(chosen_ship["kind"], chosen_ship["length"]),
        player.board,
        Position(front_position.x, front_position.y),
        direction,
    )
    chosen_ship["quantity"] -= 1


@app.post("/play-game/")
def play_game():
    pass


@app.get("/game-result/")
def get_game_result():
    pass
