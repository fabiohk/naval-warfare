from collections import namedtuple
from dataclasses import dataclass
from dataclasses import field
from enum import Enum
from typing import List
from typing import NewType
from typing import Optional


class PositionStatus(Enum):
    FREE = "O"
    OCCUPIED = "X"
    BOMBED = "B"


class ShipDirection(str, Enum):
    H = "horizontally"
    V = "vertically"


@dataclass
class Ship:
    kind: str
    length: int
    hits_taken: int = field(default=0, init=False)


@dataclass
class BoardPosition:
    status: PositionStatus = PositionStatus.FREE
    ship: Optional[Ship] = None


Chart2D = NewType("Chart2D", List[List[BoardPosition]])

Position = namedtuple("Position", ["x", "y"])


@dataclass
class Board2D:
    length: int  # horizontal - x
    width: int  # vertical - y
    chart: Chart2D = field(init=False)
    ships: List[Ship] = field(default_factory=list, init=False)

    def __post_init__(self):
        self.chart = [[BoardPosition() for _ in range(self.width)] for _ in range(self.length)]

    def __str__(self) -> str:
        return "\n".join([" ".join(position.status.value for position in self.chart[i]) for i in range(self.length)])

    def status_at(self, position: Position) -> str:
        return self.chart[position.x][position.y].status

    def ship_at(self, position: Position) -> Ship:
        return self.chart[position.x][position.y].ship
