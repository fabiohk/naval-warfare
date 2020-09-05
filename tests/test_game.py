import pytest

from naval_warfare.exceptions import CannotOccupyPositions
from naval_warfare.exceptions import InputWithError
from naval_warfare.exceptions import UnavailableShip
from naval_warfare.game import DEFAULT_GAME_OPTION
from naval_warfare.game import AvailableShip
from naval_warfare.game import Game
from naval_warfare.game import GameOption
from naval_warfare.game import Player
from naval_warfare.game import has_all_ships_destroyed
from naval_warfare.game import parse_line_input
from naval_warfare.game import place_ship
from naval_warfare.game import retrieve_available_ships
from naval_warfare.models import BoardPosition
from naval_warfare.models import Position
from naval_warfare.models import PositionStatus
from naval_warfare.models import Ship
from naval_warfare.models import ShipDirection


def test_should_return_game_has_ended_when_all_board_players_has_all_ships_destroyed():
    player_1, player_2 = Player("player_1", game_option=DEFAULT_GAME_OPTION), Player(
        "player_2", game_option=DEFAULT_GAME_OPTION
    )
    game = Game(player_1, player_2)

    assert has_all_ships_destroyed(player_1.board)
    assert has_all_ships_destroyed(player_2.board)
    assert game.has_ended


def test_should_return_game_has_ended_when_one_board_player_has_all_ships_destroyed():
    player_1, player_2 = Player("player_1", game_option=DEFAULT_GAME_OPTION), Player(
        "player_2", game_option=DEFAULT_GAME_OPTION
    )
    game = Game(player_1, player_2)
    player_1.board.ships.append(Ship("destroyer", 3))

    assert not has_all_ships_destroyed(player_1.board)
    assert has_all_ships_destroyed(player_2.board)
    assert game.has_ended


def test_should_return_game_hasnt_ended_when_board_players_has_ships_not_destroyed_yet():
    player_1, player_2 = Player("player_1", game_option=DEFAULT_GAME_OPTION), Player(
        "player_2", game_option=DEFAULT_GAME_OPTION
    )
    game = Game(player_1, player_2)

    player_1.board.ships.append(Ship("destroyer", 3))
    player_2.board.ships.append(Ship("destroyer", 3))

    assert not has_all_ships_destroyed(player_1.board)
    assert not has_all_ships_destroyed(player_2.board)
    assert not game.has_ended


def test_should_retrieve_only_the_available_ships_slugs():
    game_option: GameOption = {
        "ABC": AvailableShip(kind="abc", length=3, quantity=0),
        "DEF": AvailableShip(kind="def", length=4, quantity=99),
        "GHI": AvailableShip(kind="ghi", length=4, quantity=1),
    }

    available_ships = retrieve_available_ships(game_option)
    expected_available_ships = ["DEF", "GHI"]

    assert sorted(available_ships) == expected_available_ships


def test_should_succesfully_parse_a_valid_line_input():
    game_option: GameOption = {
        "ABC": AvailableShip(kind="abc", length=3, quantity=0),
        "DEF": AvailableShip(kind="def", length=4, quantity=99),
        "GHI": AvailableShip(kind="ghi", length=10, quantity=1),
    }
    line_horizontal_direction = "DEF 0 0 H"

    available_ship, position, ship_direction = parse_line_input(line_horizontal_direction, game_option)

    assert id(available_ship) == id(game_option["DEF"])  # Same reference!
    assert position == Position(0, 0)
    assert ship_direction == ShipDirection.H

    line_vertical_direction = "GHI 1 0 V"

    available_ship, position, ship_direction = parse_line_input(line_vertical_direction, game_option)
    assert id(available_ship) == id(game_option["GHI"])  # Same reference
    assert position == Position(1, 0)
    assert ship_direction == ShipDirection.V


def test_should_raise_exception_when_couldnt_parse_position():
    game_option: GameOption = {
        "ABC": AvailableShip(kind="abc", length=3, quantity=0),
        "DEF": AvailableShip(kind="def", length=4, quantity=99),
        "GHI": AvailableShip(kind="ghi", length=10, quantity=1),
    }
    invalid_line = "DEF 0 def H"

    with pytest.raises(InputWithError):
        parse_line_input(invalid_line, game_option)


def test_should_raise_exception_when_ship_isnt_a_ship_option():
    game_option: GameOption = {
        "ABC": AvailableShip(kind="abc", length=3, quantity=0),
        "DEF": AvailableShip(kind="def", length=4, quantity=99),
        "GHI": AvailableShip(kind="ghi", length=10, quantity=1),
    }
    invalid_line = "JKL 0 0 H"

    with pytest.raises(InputWithError):
        parse_line_input(invalid_line, game_option)


def test_should_raise_exception_when_direction_isnt_valid():
    game_option: GameOption = {
        "ABC": AvailableShip(kind="abc", length=3, quantity=0),
        "DEF": AvailableShip(kind="def", length=4, quantity=99),
        "GHI": AvailableShip(kind="ghi", length=10, quantity=1),
    }
    invalid_line = "ABC 0 0 L"

    with pytest.raises(InputWithError):
        parse_line_input(invalid_line, game_option)


def test_should_successfully_place_ship():
    game_option: GameOption = {
        "ABC": AvailableShip(kind="abc", length=3, quantity=0),
        "DEF": AvailableShip(kind="def", length=4, quantity=99),
        "GHI": AvailableShip(kind="ghi", length=10, quantity=1),
    }
    player = Player("player_1", game_option=game_option)

    place_ship(player, game_option["DEF"], Position(0, 0), ShipDirection.H)

    assert game_option["DEF"]["quantity"] == 98  # 99 - 1!
    assert len(player.board.ships) == 1
    assert player.board.ships[0] == Ship("def", 4)


def test_should_raise_exception_when_ship_isnt_available():
    game_option: GameOption = {
        "ABC": AvailableShip(kind="abc", length=3, quantity=0),
        "DEF": AvailableShip(kind="def", length=4, quantity=99),
        "GHI": AvailableShip(kind="ghi", length=10, quantity=1),
    }
    player = Player("player_1", game_option=game_option)

    with pytest.raises(UnavailableShip):
        place_ship(player, game_option["ABC"], Position(0, 0), ShipDirection.H)


def test_should_raise_exception_when_cannot_occupy_all_positions_from_board():
    game_option: GameOption = {
        "ABC": AvailableShip(kind="abc", length=3, quantity=0),
        "DEF": AvailableShip(kind="def", length=4, quantity=99),
        "GHI": AvailableShip(kind="ghi", length=10, quantity=1),
    }
    player = Player("player_1", game_option=game_option)
    player.board.chart[0][1] = BoardPosition(PositionStatus.BOMBED)

    with pytest.raises(CannotOccupyPositions):
        place_ship(player, game_option["DEF"], Position(0, 0), ShipDirection.H)
