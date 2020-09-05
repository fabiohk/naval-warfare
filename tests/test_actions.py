import pytest

from naval_warfare.actions import bomb_position
from naval_warfare.actions import place_ship_on_board
from naval_warfare.exceptions import CannotBombPosition
from naval_warfare.models import Board2D
from naval_warfare.models import BoardPosition
from naval_warfare.models import Position
from naval_warfare.models import PositionStatus
from naval_warfare.models import Ship
from naval_warfare.models import ShipDirection


def test_should_place_ship_horizontally():
    board, ship, front_position = Board2D(4, 4), Ship("destroyer", 3), Position(0, 0)

    place_ship_on_board(ship, board, front_position, ShipDirection.H)

    expected_board_position = BoardPosition(PositionStatus.OCCUPIED, ship)

    assert board.chart[0][0] == expected_board_position
    assert board.chart[0][1] == expected_board_position
    assert board.chart[0][2] == expected_board_position


def test_should_place_ship_vertically():
    board, ship, front_position = Board2D(4, 4), Ship("destroyer", 3), Position(0, 0)

    place_ship_on_board(ship, board, front_position, ShipDirection.V)

    expected_board_position = BoardPosition(PositionStatus.OCCUPIED, ship)

    assert board.chart[0][0] == expected_board_position
    assert board.chart[1][0] == expected_board_position
    assert board.chart[2][0] == expected_board_position


def test_should_bomb_a_free_position():
    board, position = Board2D(4, 4), Position(0, 0)

    outcome = bomb_position(board, position)

    assert board.chart[0][0].status == PositionStatus.BOMBED
    assert not outcome.has_hit_something
    assert not outcome.has_destroyed_a_ship


def test_should_bomb_an_occuppied_position_without_destroying_a_ship():
    board, position, ship = Board2D(4, 4), Position(0, 0), Ship("destroyer", 3)

    board.chart[position.x][position.y] = BoardPosition(PositionStatus.OCCUPIED, ship)

    outcome = bomb_position(board, position)

    assert ship.hits_taken == 1
    assert board.chart[0][0].status == PositionStatus.BOMBED
    assert outcome.has_hit_something
    assert not outcome.has_destroyed_a_ship


def test_should_bomb_and_destroy_an_occupied_position():
    board, position, ship = Board2D(4, 4), Position(0, 0), Ship("destroyer", 1)

    board.chart[position.x][position.y] = BoardPosition(PositionStatus.OCCUPIED, ship)

    outcome = bomb_position(board, position)

    assert ship.hits_taken == 1
    assert board.chart[0][0].status == PositionStatus.BOMBED
    assert outcome.has_hit_something
    assert outcome.has_destroyed_a_ship


def test_shouldnt_bomb_an_already_bombed_position():
    board, position = Board2D(4, 4), Position(0, 0)

    board.chart[position.x][position.y] = BoardPosition(PositionStatus.BOMBED)

    with pytest.raises(CannotBombPosition):
        bomb_position(board, position)


def test_shouldnt_bomb_a_position_outside_the_board():
    board, position = Board2D(4, 4), Position(5, 5)

    with pytest.raises(CannotBombPosition):
        bomb_position(board, position)
