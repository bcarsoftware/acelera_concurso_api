from src.exceptions.default_exception import DefaultException


class JWTException(DefaultException):
    def __init__(self, message: str, code: int = 401) -> None:
        super().__init__(message, code)
        self.name = "JWTException"
