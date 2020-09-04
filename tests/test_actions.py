import pytest

from naval_warfare.actions import bomb_position
from naval_warfare.actions import place_ship_on_board
from naval_warfare.exceptions import CannotBombPosition
from naval_warfare.models import Board2D
from naval_warfare.models import BoardPosition
from naval_warfare.models import Position
from naval_warfare.models import PositionStatus
from naval_warfare.models import Ship


def test_should_place_ship_horizontally():
    board, ship, front_position = Board2D(4, 4), Ship("destroyer", 3), Position(0, 0)

    place_ship_on_board(ship, board, front_position, "horizontal")

    expected_board_position = BoardPosition(PositionStatus.OCCUPIED.value, ship)

    assert board.chart[0][0] == expected_board_position
    assert board.chart[0][1] == expected_board_position
    assert board.chart[0][2] == expected_board_position


def test_should_place_ship_vertically():
    board, ship, front_position = Board2D(4, 4), Ship("destroyer", 3), Position(0, 0)

    place_ship_on_board(ship, board, front_position, "vertical")

    expected_board_position = BoardPosition(PositionStatus.OCCUPIED.value, ship)

    assert board.chart[0][0] == expected_board_position
    assert board.chart[1][0] == expected_board_position
    assert board.chart[2][0] == expected_board_position


def test_should_bomb_a_free_position():
    board, position = Board2D(4, 4), Position(0, 0)

    has_hit_something = bomb_position(board, position)

    assert board.chart[0][0].status == PositionStatus.BOMBED.value
    assert not has_hit_something


def test_should_bomb_an_occuppied_position():
    board, position, ship = Board2D(4, 4), Position(0, 0), Ship("destroyer", 3)

    board.chart[position.x][position.y] = BoardPosition(PositionStatus.OCCUPIED.value, ship)

    has_hit_something = bomb_position(board, position)

    assert board.chart[0][0].status == PositionStatus.BOMBED.value
    assert has_hit_something


def test_shouldnt_bomb_an_already_bombed_position():
    board, position = Board2D(4, 4), Position(0, 0)

    board.chart[position.x][position.y] = BoardPosition(PositionStatus.BOMBED.value)

    with pytest.raises(CannotBombPosition):
        bomb_position(board, position)


def test_shouldnt_bomb_a_position_outside_the_board():
    board, position = Board2D(4, 4), Position(5, 5)

    with pytest.raises(CannotBombPosition):
        bomb_position(board, position)
