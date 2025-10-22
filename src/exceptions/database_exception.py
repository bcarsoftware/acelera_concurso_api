from src.core.constraints import HttpStatus


class DatabaseException(Exception):
    code: int
    name: str

    def __init__(self, message: str, code: int = HttpStatus.INTERNAL_SERVER_ERROR) -> None:
        super().__init__(message)
        self.message = message
        self.name = "DatabaseException"
        self.code = code
