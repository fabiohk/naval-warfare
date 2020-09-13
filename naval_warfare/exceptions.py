from typing import Any
from typing import Dict
from typing import Optional

from fastapi.exceptions import HTTPException


class UnknownDirection(Exception):
    pass


class CannotOccupyPositions(Exception):
    pass


class CannotBombPosition(Exception):
    pass


class InputWithError(Exception):
    pass


class UnavailableShip(Exception):
    pass


class UnknownGame(HTTPException):
    def __init__(
        self,
        status_code: int = 400,
        detail: Any = "Unknown game!",
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class UnknownPlayer(HTTPException):
    def __init__(
        self,
        status_code: int = 400,
        detail: Any = "Unknown player!",
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)
