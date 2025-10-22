from src.core.constraints import HttpStatus
from src.exceptions.default_exception import DefaultException


class JWTException(DefaultException):
    def __init__(self, message: str, code: int = HttpStatus.NOT_AUTHORIZED) -> None:
        super().__init__(message, code)
        self.name = "JWTException"
