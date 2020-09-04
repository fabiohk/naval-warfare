import logging

from naval_warfare.board import occupy_board_positions
from naval_warfare.board import retrieve_affected_positions
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
    occupy_board_positions(board, possible_affected_positions)
