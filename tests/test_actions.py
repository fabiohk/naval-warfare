from naval_warfare.actions import place_ship_on_board
from naval_warfare.models import Board2D
from naval_warfare.models import Position
from naval_warfare.models import PositionStatus
from naval_warfare.models import Ship


def test_should_place_ship_horizontally():
    board, ship, front_position = Board2D(4, 4), Ship("destroyer", 3), Position(0, 0)

    place_ship_on_board(ship, board, front_position, "horizontal")

    assert board.chart[0][0] == PositionStatus.OCCUPIED.value
    assert board.chart[0][1] == PositionStatus.OCCUPIED.value
    assert board.chart[0][2] == PositionStatus.OCCUPIED.value


def test_should_place_ship_vertically():
    board, ship, front_position = Board2D(4, 4), Ship("destroyer", 3), Position(0, 0)

    place_ship_on_board(ship, board, front_position, "vertical")

    assert board.chart[0][0] == PositionStatus.OCCUPIED.value
    assert board.chart[1][0] == PositionStatus.OCCUPIED.value
    assert board.chart[2][0] == PositionStatus.OCCUPIED.value
