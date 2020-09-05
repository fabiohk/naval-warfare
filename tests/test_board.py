import itertools

import pytest

from naval_warfare.board import cannot_occupy_board_in_the_positions
from naval_warfare.board import has_all_ships_destroyed
from naval_warfare.board import occupy_board_positions_with_ship
from naval_warfare.board import retrieve_affected_positions
from naval_warfare.exceptions import CannotOccupyPositions
from naval_warfare.exceptions import UnknownDirection
from naval_warfare.models import Board2D
from naval_warfare.models import BoardPosition
from naval_warfare.models import Position
from naval_warfare.models import PositionStatus
from naval_warfare.models import Ship
from naval_warfare.models import ShipDirection


def test_should_return_false_when_board_has_all_positions_free():
    board = Board2D(4, 4)  # A new board completely free

    assert not cannot_occupy_board_in_the_positions(
        board, [Position(i, j) for i, j in itertools.product(range(4), range(4))]
    )


def test_should_return_true_when_position_is_occupied_on_board():
    board = Board2D(4, 4)

    board.chart[0][0] = BoardPosition(PositionStatus.OCCUPIED)

    assert cannot_occupy_board_in_the_positions(
        board, [Position(i, j) for i, j in itertools.product(range(4), range(4))]
    )


def test_should_return_true_when_position_is_bombed_on_board():
    board = Board2D(4, 4)

    board.chart[0][0] = BoardPosition(PositionStatus.BOMBED)

    assert cannot_occupy_board_in_the_positions(
        board, [Position(i, j) for i, j in itertools.product(range(4), range(4))]
    )


def test_should_return_true_when_given_position_isnt_inside_the_board():
    board = Board2D(4, 4)

    assert cannot_occupy_board_in_the_positions(board, [Position(10, 2)])


def test_should_return_horizontal_positions():
    front_position = Position(1, 1)

    affected_positions = retrieve_affected_positions(2, front_position, ShipDirection.H)

    expected_positions = [Position(1, j) for j in range(1, 3)]

    assert sorted(affected_positions) == sorted(expected_positions)


def test_should_return_vertical_positions():
    front_position = Position(1, 1)

    affected_positions = retrieve_affected_positions(2, front_position, ShipDirection.V)

    expected_positions = [Position(i, 1) for i in range(1, 3)]

    assert sorted(affected_positions) == sorted(expected_positions)


def test_should_raise_exception_for_unknown_direction():
    with pytest.raises(UnknownDirection):
        retrieve_affected_positions(2, Position(1, 1), "unknown_direction")


def test_should_occupy_free_positions_from_board_with_ship():
    board = Board2D(4, 4)  # A new board completely free
    ship = Ship("destroyer", 3)

    occupy_board_positions_with_ship(board, [Position(1, 1)], ship)

    assert board.chart[1][1].status == PositionStatus.OCCUPIED
    assert board.chart[1][1].ship == ship

    assert len(board.ships) == 1


def test_should_raise_exception_that_cannot_occupy_board_position():
    board = Board2D(4, 4)  # A new board completely free

    board.chart[1][1] = BoardPosition(PositionStatus.BOMBED)  # Occupy position (1,1)

    with pytest.raises(CannotOccupyPositions):
        occupy_board_positions_with_ship(board, [Position(1, 1)], Ship("destroyer", 3))


def test_should_return_true_when_all_ships_from_a_board_was_destroyed():
    board, ship = Board2D(4, 4), Ship("destroyer", 3)

    ship.hits_taken = 3  # Ship destroyed
    board.ships.append(ship)  # Append ship to the board

    assert has_all_ships_destroyed(board)


def test_should_return_false_when_theres_a_not_destroyed_ship_on_board():
    board, ship = Board2D(4, 4), Ship("destroyer", 3)

    ship.hits_taken = 2  # Ship almost destroyed
    board.ships.append(ship)  # Append ship to the board

    assert not has_all_ships_destroyed(board)
