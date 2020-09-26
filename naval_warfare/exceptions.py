from typing import Any
from typing import Dict
from typing import Optional

from fastapi.exceptions import HTTPException


class UnknownDirection(Exception):
    pass


class CannotOccupyPositions(HTTPException):
    def __init__(
        self,
        status_code: int = 400,
        detail: Any = "Cannot occupy ship on given position!",
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)


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


class UnknownShip(HTTPException):
    def __init__(
        self,
        status_code: int = 400,
        detail: Any = "Unknown ship!",
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class GameAlreadyStarted(HTTPException):
    def __init__(
        self,
        status_code: int = 400,
        detail: Any = "Game already started!",
        headers: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class GameStillInProgress(HTTPException):
    def __init__(
        self, status_code: int = 400, detail: Any = "Game still in progress!", headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class GameHasntStarted(HTTPException):
    def __init__(
        self, status_code: int = 400, detail: Any = "Game hasn't started yet!", headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
