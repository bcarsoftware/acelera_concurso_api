from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from src.core.constraints import Constraints
from src.exceptions.database_exception import DatabaseException

load_dotenv()


def get_engine() -> Generator[AsyncEngine, None, None]:
    url = Constraints.DB_URL

    if url is None:
        raise DatabaseException("database url cannot be null")

    yield create_async_engine(url, echo=False)
