from collections import namedtuple
from dataclasses import dataclass
from dataclasses import field
from enum import Enum
from typing import List
from typing import NewType


class PositionStatus(Enum):
    FREE = "O"
    OCCUPIED = "X"
    BOMBED = "B"


Chart2D = NewType("Chart2D", List[List[PositionStatus]])


@dataclass
class Board2D:
    length: int  # horizontal - x
    width: int  # vertical - y
    chart: Chart2D = field(init=False)

    def __post_init__(self):
        self.chart = [[PositionStatus.FREE.value for _ in range(self.width)] for _ in range(self.length)]


@dataclass
class Ship:
    kind: str
    length: int


Position = namedtuple("Position", ["x", "y"])
