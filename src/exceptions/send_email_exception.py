from src.exceptions.default_exception import DefaultException


class SendEmailException(DefaultException):
    def __init__(self, message: str, code: int = 400) -> None:
        super().__init__(message, code)
        self.name = "SendEmailException"
