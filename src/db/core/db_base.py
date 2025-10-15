from os import environ

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase


load_dotenv()


class DBBase(DeclarativeBase):
    pass


def engine():
    url = environ.get("DB_URL")
    return create_async_engine(url, echo=False)
