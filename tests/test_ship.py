import pytest

from naval_warfare.models import Ship
from naval_warfare.ship import increase_ship_hits_taken
from naval_warfare.ship import is_ship_destroyed


@pytest.mark.parametrize("hits", [0, 1, 100])
def test_should_increase_hits_taken_by_a_ship(hits: int):
    ship = Ship("destroyer", 3)

    previous_hits_taken = ship.hits_taken

    increase_ship_hits_taken(ship, hits)

    assert previous_hits_taken + hits == ship.hits_taken


@pytest.mark.parametrize("hits_taken", [5, 3])
def test_should_return_true_when_a_ship_took_more_hits_than_its_length(hits_taken: int):
    ship = Ship("destroyer", 3)

    ship.hits_taken = hits_taken

    assert is_ship_destroyed(ship)


@pytest.mark.parametrize("hits_taken", [0, 2])
def test_should_return_false_when_a_ship_took_less_hits_than_its_length(hits_taken: int):
    ship = Ship("destroyer", 3)

    ship.hits_taken = hits_taken

    assert not is_ship_destroyed(ship)
