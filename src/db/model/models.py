from datetime import date, datetime

from sqlalchemy import String, Date, Column, Integer, DateTime
from sqlalchemy.orm import Mapped

from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = Column(Integer, autoincrement=True, primary_key=True)

    first_name: Mapped[str] = Column(String(64), nullable=False)
    last_name: Mapped[str] = Column(String(255), nullable=False)
    date_born: Mapped[date] = Column(Date, nullable=False)
    gender: Mapped[str] = Column(String(64), nullable=False) # TODO: crate EnumGender

    username: Mapped[str] = Column(String(128), nullable=False, unique=True)
    email: Mapped[str] = Column(String(255), nullable=False, unique=True)
    password: Mapped[str] = Column(String(255), nullable=False)

    points: Mapped[int] = Column(Integer, nullable=False, default=0)

    # TODO: Relationships

    create_at: Mapped[datetime] = Column(DateTime, nullable=False, default=datetime.now)
    update_at: Mapped[datetime] = Column(DateTime, nullable=False, onupdate=datetime.now)
