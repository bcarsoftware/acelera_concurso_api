from functools import wraps
from typing import Callable, Any

from src.exceptions.database_exception import DatabaseException
from src.exceptions.default_exception import DefaultException

# TODO: Request Success and Error Factory | after implements here
def exception_handler(function: Callable) -> Callable:
    @wraps(function)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return function(*args, **kwargs)
        except DefaultException as e:
            raise e
        except DatabaseException as d:
            raise d

    return wrapper
