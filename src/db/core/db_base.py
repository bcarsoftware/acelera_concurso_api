from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine, Engine

from src.core.constraints import Constraints
from src.exceptions.database_exception import DatabaseException

load_dotenv()


def engine() -> Generator[Engine, None, None]:
    url = Constraints.DB_URL

    if url is None:
        raise DatabaseException("database url cannot be null")

    yield create_engine(url, echo=False)

