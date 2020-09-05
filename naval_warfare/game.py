import logging
from contextlib import suppress
from copy import deepcopy
from dataclasses import dataclass
from random import randint
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import TypedDict

from naval_warfare.actions import BombOutcome
from naval_warfare.actions import bomb_position
from naval_warfare.actions import place_ship_on_board
from naval_warfare.board import has_all_ships_destroyed
from naval_warfare.exceptions import CannotBombPosition
from naval_warfare.exceptions import CannotOccupyPositions
from naval_warfare.exceptions import InputWithError
from naval_warfare.exceptions import UnavailableShip
from naval_warfare.helpers import convert_boolean_to_yes_no
from naval_warfare.models import Board2D
from naval_warfare.models import Position
from naval_warfare.models import Ship
from naval_warfare.models import ShipDirection
from naval_warfare.ship import is_ship_destroyed

logger = logging.getLogger(__name__)

AvailableShip = TypedDict("AvailableShip", {"kind": str, "length": int, "quantity": int})
GameOption = Dict[str, AvailableShip]


class Player:
    def __init__(self, name: str, *, game_option: GameOption, length: int = 10, width: int = 10):
        self.name = name
        self.board = Board2D(length, width)
        self.game_option = deepcopy(game_option)

    @property
    def remaining_ships(self) -> List[str]:
        return [ship.kind for ship in self.board.ships if not is_ship_destroyed(ship)]


@dataclass
class Game:
    player_1: Player
    player_2: Player

    @property
    def has_ended(self) -> bool:
        return any(has_all_ships_destroyed(player.board) for player in self.players)

    @property
    def players(self) -> List[Player]:
        return [self.player_1, self.player_2]


DEFAULT_GAME_OPTION: GameOption = {
    "AIR": AvailableShip(kind="aircraft-carrier", length=5, quantity=1),
    "BTL": AvailableShip(kind="battleship", length=4, quantity=1),
    "SUB": AvailableShip(kind="submarine", length=3, quantity=1),
    "DES": AvailableShip(kind="destroyer", length=3, quantity=1),
    "PTL": AvailableShip(kind="patrol-ship", length=2, quantity=1),
}


def retrieve_available_ships(game_option: GameOption) -> List[str]:
    return [ship_slug for ship_slug, ship_option in game_option.items() if ship_option["quantity"] > 0]


def parse_line_input(line: str, game_option: GameOption) -> Tuple[AvailableShip, Position, ShipDirection]:
    try:
        ship_slug, x, y, direction_slug = line.split(maxsplit=3)
        return (
            game_option[ship_slug],
            Position(int(x), int(y)),
            ShipDirection[direction_slug],
        )
    except (ValueError, KeyError):
        print(
            """
            Couldn't understand the given input, please input in the following format:
                - if horizontally: SLG X Y H
                - if vertically: SLG X Y V      
                
            For example, if you have a destroyer (DES) and you want to put at position (0, 0) horizontally, write:
                DES 0 0 H          
            """
        )
        raise InputWithError


def place_ship(player: Player, chosen_ship: AvailableShip, position: Position, direction: ShipDirection):
    if chosen_ship["quantity"] < 1:
        print("Ship is unavailable!")
        raise UnavailableShip

    try:
        place_ship_on_board(Ship(chosen_ship["kind"], chosen_ship["length"]), player.board, position, direction)
        chosen_ship["quantity"] -= 1
    except CannotOccupyPositions:
        print("Couldn't place ship on given position!")
        raise


def prepare_player_game(player: Player):
    print(
        """
        To place a ship, input in the following format:
            - if horizontally: SLG X Y H
            - if vertically: SLG X Y V

        For example, if you have a destroyer (DES) and you want to put at position (0, 0) horizontally, write:
            DES 0 0 H

        Input them until there's no available ships!
        """
    )
    available_ships = retrieve_available_ships(player.game_option)

    while available_ships:
        print(f"Available ships: {available_ships}")

        with suppress(InputWithError, CannotOccupyPositions, UnavailableShip):
            line = input()
            chosen_ship, position, direction = parse_line_input(line, player.game_option)
            place_ship(player, chosen_ship, position, direction)
            logger.debug(
                """Updated %s board:
                %s
                """,
                player.name,
                player.board,
            )
            available_ships = retrieve_available_ships(player.game_option)


def prepare_game(game_option: Optional[GameOption] = None) -> Game:
    player_1, player_2 = Player("Player 1", game_option=game_option or DEFAULT_GAME_OPTION), Player(
        "Player 2", game_option=game_option or DEFAULT_GAME_OPTION
    )

    print("Player 1, please place your Ships on the board!")
    prepare_player_game(player_1)

    print("Player 2, please place your Ships on the board!")
    prepare_player_game(player_2)

    return Game(player_1, player_2)


def get_random_position(length: int, width: int) -> Position:
    return Position(randint(0, length), randint(0, width))


def print_outcome(player: Player, outcome: BombOutcome, position: Position):
    hit_something, destroyed_ship = (
        convert_boolean_to_yes_no(outcome.has_hit_something),
        convert_boolean_to_yes_no(outcome.has_destroyed_a_ship),
    )
    print(
        f"""
        {player.name} attacked position ({position.x}, {position.y})...
        Outcome:
            - hit something: {hit_something}
            - destroyed ship: {destroyed_ship}
        """
    )


def start(game: Game):
    print("Time to battle!")
    attacking_player, attacked_player = game.player_1, game.player_2

    while not game.has_ended:
        with suppress(CannotBombPosition):
            position = get_random_position(attacked_player.board.length, attacked_player.board.width)
            bomb_outcome = bomb_position(attacked_player.board, position)
            print_outcome(attacking_player, bomb_outcome, position)
            attacking_player, attacked_player = attacked_player, attacking_player

    print(f"Battle result: {attacked_player.name} won!")
    print(f"Remaining ships: {attacked_player.remaining_ships}", end="\n\n")


def show_final_boards(game: Game):
    for player in game.players:
        print(f"Final board from {player.name}")
        print(str(player.board), end="\n\n")
