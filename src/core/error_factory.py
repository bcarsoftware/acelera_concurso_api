from fastapi import HTTPException
from src.exceptions.database_exception import DatabaseException
from src.exceptions.default_exception import DefaultException


async def error_factory(exception: DefaultException | DatabaseException, headers: dict = None) -> HTTPException:
    headers = headers or {
        "Content-Type": "application/json"
    }

    detail = {
        "error": exception.args[0] or "Internal Server Error",
        "status_code": exception.code or 500
    }

    return HTTPException(status_code=exception.code, detail=detail, headers=headers)
