from functools import wraps
from typing import Callable, Any

from src.core.error_factory import error_factory
from src.exceptions.database_exception import DatabaseException
from src.exceptions.default_exception import DefaultException


def exception_handler(function: Callable) -> Callable:
    @wraps(function)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return await function(*args, **kwargs)
        except DefaultException as e:
            exception = await error_factory(e)

            raise exception
        except DatabaseException as d:
            exception = await error_factory(d)

            raise exception

    return wrapper
