from src.core.constraints import HttpStatus
from src.exceptions.default_exception import DefaultException


class NoteException(DefaultException):
    def __init__(self, message: str, code: int = HttpStatus.BAD_REQUEST):
        super().__init__(message, code)
        self.name = "NoteException"
