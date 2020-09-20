from typing import Dict
from typing import Union

import pytest
from fastapi.testclient import TestClient

from naval_warfare import api
from naval_warfare.game import DEFAULT_GAME_OPTION
from naval_warfare.game import Game
from naval_warfare.game import Player
from naval_warfare.models import BoardPosition
from naval_warfare.models import Position
from naval_warfare.models import PositionStatus
from naval_warfare.models import Ship


@pytest.fixture
def app_client() -> TestClient:
    return TestClient(api.app)


@pytest.fixture
def game() -> Dict[str, Union[int, Player]]:
    game_id = 1
    player_1, player_2 = Player("Player 1", game_option=DEFAULT_GAME_OPTION), Player(
        "Player 2", game_option=DEFAULT_GAME_OPTION
    )
    setattr(api.app, f"game_{game_id}", Game(player_1, player_2))
    return {"id": game_id, "player_1": player_1, "player_2": player_2}


def test_should_succesfully_create_a_new_game(app_client: TestClient):
    response = app_client.post("/new-game/", json={"player_1": "Player 1", "player_2": "Player 2"})

    assert response.status_code == 201
    assert response.json() == {"id": 1}

    assert hasattr(api.app, "game_1")


def test_should_successfully_retrieve_the_available_ships_from_a_player(
    app_client: TestClient, game: Dict[str, Union[int, Player]]
):
    expected_available_ships = [ship for ship, parameters in DEFAULT_GAME_OPTION.items() if parameters["quantity"] > 0]

    response = app_client.get("/available-ships/", params={"game": game["id"], "player": game["player_1"].name})

    assert response.status_code == 200
    assert "available_ships" in response.json()

    available_ships = response.json()["available_ships"]
    assert sorted(available_ships) == sorted(expected_available_ships)


@pytest.mark.parametrize("field", ["game", "player"])
def test_shouldnt_retrieve_the_available_ships_when_a_required_field_isnt_given(app_client: TestClient, field: str):
    params = {"game": 1, "player": "Player 1"}
    params.pop(field)

    response = app_client.get("/available-ships/", params=params)

    assert response.status_code == 422
    assert response.json() == {
        "detail": [{"loc": ["query", field], "msg": "field required", "type": "value_error.missing"}]
    }


def test_shouldnt_retrieve_the_available_ships_when_an_unknown_game_is_given(app_client: TestClient):
    response = app_client.get("/available-ships/", params={"game": 42, "player": "Player 1"})

    assert response.status_code == 400
    assert response.json() == {"detail": "Unknown game!"}


def test_shouldnt_retrieve_the_available_ships_when_an_unkown_player_is_given(
    app_client: TestClient, game: Dict[str, Union[int, str]]
):
    response = app_client.get("/available-ships/", params={"game": game["id"], "player": "Unknown Player"})

    assert response.status_code == 400
    assert response.json() == {"detail": "Unknown player!"}


def test_should_successfully_place_ship_on_board(app_client: TestClient, game: Dict[str, Union[int, Player]]):
    json = {
        "game": game["id"],
        "ship": "AIR",  # Length 5
        "player": game["player_1"].name,
        "front_position": {"x": 0, "y": 0},
        "direction": "horizontally",
    }

    expected_positions, expected_ship = [
        Position(0, 0),
        Position(0, 1),
        Position(0, 2),
        Position(0, 3),
        Position(0, 4),
    ], Ship("aircraft-carrier", 5)

    ship_quantity_before_call = game["player_1"].game_option["AIR"]["quantity"]

    response = app_client.put("/ship-on-board/", json=json)

    ship_quantity_after_call = game["player_1"].game_option["AIR"]["quantity"]

    assert ship_quantity_after_call == ship_quantity_before_call - 1
    assert response.status_code == 204
    assert all(game["player_1"].board.ship_at(position) == expected_ship for position in expected_positions)


def test_shouldnt_place_an_unknown_ship_on_board(app_client: TestClient, game: Dict[str, Union[int, Player]]):
    json = {
        "game": game["id"],
        "ship": "unknown-ship",  # Length 5
        "player": game["player_1"].name,
        "front_position": {"x": 0, "y": 0},
        "direction": "horizontally",
    }

    response = app_client.put("/ship-on-board/", json=json)

    assert response.status_code == 400
    assert response.json() == {"detail": "Unknown ship!"}


def test_shouldnt_place_a_ship_into_an_unknown_game(app_client: TestClient, game: Dict[str, Union[int, Player]]):
    json = {
        "game": 42,
        "ship": "AIR",  # Length 5
        "player": game["player_1"].name,
        "front_position": {"x": 0, "y": 0},
        "direction": "horizontally",
    }

    response = app_client.put("/ship-on-board/", json=json)

    assert response.status_code == 400
    assert response.json() == {"detail": "Unknown game!"}


def test_shouldnt_place_a_ship_on_an_already_occupied_position(
    app_client: TestClient, game: Dict[str, Union[int, Player]]
):
    json = {
        "game": game["id"],
        "ship": "AIR",  # Length 5
        "player": game["player_1"].name,
        "front_position": {"x": 0, "y": 0},
        "direction": "horizontally",
    }

    game["player_1"].board.chart[0][0] = BoardPosition(status=PositionStatus.OCCUPIED)

    ship_quantity_before_call = game["player_1"].game_option["AIR"]["quantity"]

    response = app_client.put("/ship-on-board/", json=json)

    ship_quantity_after_call = game["player_1"].game_option["AIR"]["quantity"]

    assert ship_quantity_after_call == ship_quantity_before_call
    assert response.status_code == 400
    assert response.json() == {"detail": "Cannot occupy ship on given position!"}
