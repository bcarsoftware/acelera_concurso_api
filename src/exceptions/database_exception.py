class DatabaseException(Exception):
    code: int
    name: str

    def __init__(self, message: str = "Internal Server Error", code: int = 500) -> None:
        super().__init__(message)
        self.name = "DatabaseException"
        self.code = code
