from abc import ABC


class DefaultException(ABC, Exception):
    code: int
    message: str
    name: str = "DefaultException"

    def __init__(self, message: str, code: int = 400):
        self.message = message
        self.code = code
        super().__init__(message)
