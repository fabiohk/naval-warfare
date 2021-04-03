import logging
from typing import Dict
from typing import List

import sqlalchemy
from fastapi import BackgroundTasks
from fastapi import Body
from fastapi import FastAPI
from fastapi import Query
from sqlalchemy.future import select

from naval_warfare.actions import place_ship_on_board
from naval_warfare.api_models import Players
from naval_warfare.api_models import ShipOnBoard
from naval_warfare.db_models import Board
from naval_warfare.db_models import Game
from naval_warfare.db_models import GameSettings
from naval_warfare.db_models import Player
from naval_warfare.db_models import SessionLocal
from naval_warfare.exceptions import GameAlreadyStarted
from naval_warfare.exceptions import GameHasntStarted
from naval_warfare.exceptions import GameStillInProgress
from naval_warfare.exceptions import UnknownGame
from naval_warfare.exceptions import UnknownShip
from naval_warfare.game import DEFAULT_GAME_OPTION
from naval_warfare.game import GameStatus
from naval_warfare.game import retrieve_available_ships
from naval_warfare.game import start
from naval_warfare.models import Position
from naval_warfare.models import Ship

logger = logging.getLogger(__name__)

app = FastAPI()


@app.post("/new-game/", status_code=201)
async def start_new_game(players: Players) -> Dict[str, int]:
    logger.info("Starting a new game!")

    player_1, player_2 = (Player(name=players.player_1), Player(name=players.player_2))

    async with SessionLocal() as session:
        result = await session.execute(select(GameSettings).filter(GameSettings.slug == "default"))
        game_settings = result.first()
        if game_settings is None:
            game_settings = GameSettings(slug="default", configuration=DEFAULT_GAME_OPTION)
            session.add(game_settings)
        game = Game(settings=game_settings)
        player_1_board, player_2_board = Board(length=10, width=10, game=game, player=player_1), Board(
            length=10, width=10, game=game, player=player_2
        )
        session.add_all([player_1, player_2, game, player_1_board, player_2_board])
        await session.commit()
        await session.refresh(game)

    return {"id": game.id}


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
def play_game(
    background_tasks: BackgroundTasks,
    game_id: int = Body(..., alias="game", description="The game ID to start the game", title="Game ID", embed=True),
):
    logger.info("Receive a request to start the game %s", game_id)
    game: Game = getattr(app, f"game_{game_id}", None)
    if not game:
        raise UnknownGame

    if game.status != GameStatus.INITIALIZED:
        raise GameAlreadyStarted

    background_tasks.add_task(start, game)
    return {"detail": f"Started game {game_id}!"}


@app.get("/game-result/")
def retrieve_game_result(game_id: int = Query(..., alias="game", description="The player game ID", title="Game ID")):
    logger.info("Retrieving game result from %s", game_id)
    game: Game = getattr(app, f"game_{game_id}", None)
    if not game:
        raise UnknownGame

    if game.status != GameStatus.ENDED:
        logger.debug("Game status: %s", game.status)
        exception = GameHasntStarted if game.status == GameStatus.INITIALIZED else GameStillInProgress
        raise exception

    return {
        "winner": str(game.winner),
        "turns": [
            {
                "attacking_player": str(turn.attacking_player),
                "outcome": {
                    "has_hit_something": turn.outcome.has_hit_something,
                    "has_destroyed_a_ship": turn.outcome.has_destroyed_a_ship,
                },
                "position": {"x": turn.position.x, "y": turn.position.y},
            }
            for turn in game.turns
        ],
    }
