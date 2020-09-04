import logging
from typing import List
from typing import Sequence

from naval_warfare.exceptions import CannotOccupyPositions
from naval_warfare.exceptions import UnknownDirection
from naval_warfare.models import Board2D
from naval_warfare.models import Position
from naval_warfare.models import PositionStatus
from naval_warfare.models import Ship
from naval_warfare.ship import increase_ship_hits_taken
from naval_warfare.ship import is_ship_destroyed

logger = logging.getLogger(__name__)


def is_position_inside_the_board(board: Board2D, position: Position) -> bool:
    return 0 <= position.x < board.length and 0 <= position.y < board.width


def is_position_bombed(board: Board2D, position: Position) -> bool:
    return board.status_at(position) == PositionStatus.BOMBED.value


def can_bomb_board_position(board: Board2D, position: Position) -> bool:
    return is_position_inside_the_board(board, position) and not is_position_bombed(board, position)


def is_position_occuppied(board: Board2D, position: Position) -> bool:
    return board.status_at(position) == PositionStatus.OCCUPIED.value


def cannot_occupy_board_in_the_positions(board: Board2D, positions: Sequence[Position]) -> bool:
    return any(
        not is_position_inside_the_board(board, position) or board.status_at(position) != PositionStatus.FREE.value
        for position in positions
    )


def retrieve_affected_positions(ship_length: int, front_position: Position, direction: str) -> List[Position]:
    if direction == "horizontal":
        return [Position(front_position.x, j) for j in range(front_position.y, front_position.y + ship_length)]

    if direction == "vertical":
        return [Position(i, front_position.y) for i in range(front_position.x, front_position.x + ship_length)]

    raise UnknownDirection


def occupy_board_positions_with_ship(board: Board2D, positions: Sequence[Position], ship: Ship):
    logger.info("Possible positions that will be occupied: %s", positions)
    if cannot_occupy_board_in_the_positions(board, positions):
        raise CannotOccupyPositions

    for position in positions:
        board.chart[position.x][position.y].status = PositionStatus.OCCUPIED.value
        board.chart[position.x][position.y].ship = ship

    logger.info("Board positions occupied!")


def bomb_board_position(board: Board2D, position: Position) -> bool:
    has_hit_something = is_position_occuppied(board, position)
    board.chart[position.x][position.y].status = PositionStatus.BOMBED.value
    return has_hit_something


def has_destroyed_ship_on_position(board: Board2D, position: Position) -> bool:
    affected_ship = board.ship_at(position)
    increase_ship_hits_taken(affected_ship)
    return is_ship_destroyed(affected_ship)
