from abc import ABC

from src.core.constraints import HttpStatus


class DefaultException(ABC, Exception):
    code: int
    message: str
    name: str = "DefaultException"

    def __init__(self, message: str, code: int = HttpStatus.BAD_REQUEST):
        self.message = message
        self.code = code
        super().__init__(message)
