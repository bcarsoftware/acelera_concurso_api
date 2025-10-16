from os import environ
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine, Engine

load_dotenv()


def engine() -> Generator[Engine, None, None]:
    url = environ.get("DB_URL")
    yield create_engine(url, echo=False)

