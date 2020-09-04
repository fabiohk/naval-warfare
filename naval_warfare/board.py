import logging
from typing import List
from typing import Sequence

from naval_warfare.exceptions import CannotOccupyPositions
from naval_warfare.exceptions import UnknownDirection
from naval_warfare.models import Board2D
from naval_warfare.models import Position
from naval_warfare.models import PositionStatus

logger = logging.getLogger(__name__)


def is_position_inside_the_board(board: Board2D, position: Position) -> bool:
    return 0 <= position.x < board.length and 0 <= position.y < board.width


def cannot_occupy_board_in_the_positions(board: Board2D, positions: Sequence[Position]) -> bool:
    return any(
        not is_position_inside_the_board(board, position)
        or board.chart[position.x][position.y] != PositionStatus.FREE.value
        for position in positions
    )


def retrieve_affected_positions(ship_length: int, front_position: Position, direction: str) -> List[Position]:
    if direction == "horizontal":
        return [Position(front_position.x, j) for j in range(front_position.y, front_position.y + ship_length)]

    if direction == "vertical":
        return [Position(i, front_position.y) for i in range(front_position.x, front_position.x + ship_length)]

    raise UnknownDirection


def occupy_board_positions(board: Board2D, positions: Sequence[Position]):
    logger.info("Possible positions that will be occupied: %s", positions)
    if cannot_occupy_board_in_the_positions(board, positions):
        raise CannotOccupyPositions

    for position in positions:
        board.chart[position.x][position.y] = PositionStatus.OCCUPIED.value
    logger.info("Board positions occupied!")
