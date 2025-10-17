from src.exceptions.default_exception import DefaultException


class TopicException(DefaultException):
    def __init__(self, message: str, code: int = 400):
        super().__init__(message, code)
        self.name = "TopicException"
