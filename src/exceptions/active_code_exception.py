from src.exceptions.default_exception import DefaultException


class ActiveCodeException(DefaultException):
    def __init__(self, message: str, code: int = 400) -> None:
        super().__init__(message)
        self.code = code
        self.name = "ActiveCodeException"
