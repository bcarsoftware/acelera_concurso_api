from src.exceptions.default_exception import DefaultException


class SubjectException(DefaultException):
    def __init__(self, message: str, code: int = 400):
        super().__init__(message, code)
        self.name = "SubjectException"
