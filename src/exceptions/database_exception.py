class DatabaseException(Exception):
    code: int
    name: str

    def __init__(self, message: str, code: int = 500) -> None:
        super().__init__(message)
        self.message = message
        self.name = "DatabaseException"
        self.code = code
