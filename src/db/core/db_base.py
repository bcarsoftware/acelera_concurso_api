from typing import Generator

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from src.core.constraints import Constraints, HttpStatus
from src.exceptions.database_exception import DatabaseException

load_dotenv()


def get_engine() -> Generator[AsyncEngine, None, None]:
    url = Constraints.DB_URL

    if url is None:
        raise DatabaseException("database url cannot be null", HttpStatus.NOT_FOUND)

    yield create_async_engine(url, echo=False)
