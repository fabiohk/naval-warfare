import logging

from naval_warfare.board import bomb_board_position
from naval_warfare.board import can_bomb_board_position
from naval_warfare.board import occupy_board_positions_with_ship
from naval_warfare.board import retrieve_affected_positions
from naval_warfare.exceptions import CannotBombPosition
from naval_warfare.models import Board2D
from naval_warfare.models import Position
from naval_warfare.models import Ship

logger = logging.getLogger(__name__)


def place_ship_on_board(ship: Ship, board: Board2D, front_position: Position, direction: str):
    logger.info(
        "Ship %s (length: %s) will be placed in %s direction starting at %s",
        ship.kind,
        ship.length,
        direction,
        front_position,
    )

    possible_affected_positions = retrieve_affected_positions(ship.length, front_position, direction)
    occupy_board_positions_with_ship(board, possible_affected_positions, ship)
    logger.info("Succesfully placed ship!")


def bomb_position(board: Board2D, position: Position) -> bool:
    """Attempt to bomb a position. Returns True if it hit something, otherwise False."""
    logger.info("Trying to bomb board on position: %s", position)
    if not can_bomb_board_position(board, position):
        raise CannotBombPosition

    has_hit_something = bomb_board_position(board, position)
    logger.info("Succesfully bombed given position! Outcome: hit %s", "something" if has_hit_something else "nothing")
    return has_hit_something
