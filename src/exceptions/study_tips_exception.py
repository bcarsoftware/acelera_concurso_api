from src.core.constraints import HttpStatus
from src.exceptions.default_exception import DefaultException


class StudyTipsException(DefaultException):
    def __init__(self, message: str, code: int = HttpStatus.BAD_REQUEST) -> None:
        super().__init__(message, code)
        self.name = "StudyTipsException"
