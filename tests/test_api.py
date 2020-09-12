import pytest
from fastapi.testclient import TestClient

from naval_warfare import api
from naval_warfare.game import Game


@pytest.fixture
def app_client() -> TestClient:
    return TestClient(api.app)


def test_should_succesfully_create_a_new_game(app_client: TestClient):
    response = app_client.post("/new-game/", json={"player_1": "Player 1", "player_2": "Player 2"})

    assert response.status_code == 201
    assert response.json() == {"id": 1}

    assert hasattr(api.app, "game_1")
