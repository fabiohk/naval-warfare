from naval_warfare.models import Ship


def increase_ship_hits_taken(ship: Ship, hits_taken: int = 1):
    ship.hits_taken += hits_taken


def is_ship_destroyed(ship: Ship) -> bool:
    return ship.hits_taken >= ship.length
