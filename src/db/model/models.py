from datetime import date, datetime
from typing import List

from sqlalchemy import String, Date, Column, Integer, DateTime, Enum, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, relationship

from sqlalchemy.ext.declarative import declarative_base

from src.enum.enum_gender import EnumGender

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = Column(Integer, autoincrement=True, primary_key=True)

    first_name: Mapped[str] = Column(String(64), nullable=False)
    last_name: Mapped[str] = Column(String(255), nullable=False)
    date_born: Mapped[date] = Column(Date, nullable=False)
    gender: Mapped[EnumGender] = Column(Enum("FEMALE", "MALE", "NOT_BINARY", "NOT_SAY", name="EnumGender"), nullable=False)

    username: Mapped[str] = Column(String(128), nullable=False, unique=True)
    email: Mapped[str] = Column(String(255), nullable=False, unique=True)
    password: Mapped[str] = Column(String(255), nullable=False)

    points: Mapped[int] = Column(Integer, nullable=False, default=0)
    deleted: Mapped[bool] = Column(Boolean, nullable=False, default=False)

    # TODO: Relationships
    public_tenders: Mapped[List["PublicTender"]] = relationship(back_populates="user")

    create_at: Mapped[datetime] = Column(DateTime, nullable=False, default=datetime.now)
    update_at: Mapped[datetime] = Column(DateTime, nullable=False, onupdate=datetime.now)


class PublicTender(Base):
    __tablename__ = "public_tenders"

    public_tender_id: Mapped[int] = Column(Integer, autoincrement=True, primary_key=True)

    user_id: Mapped[int] = Column(Integer, ForeignKey(User.user_id, ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="public_tenders")

    tender_name: Mapped[str] = Column(String(255), nullable=False)
    tender_board: Mapped[str] = Column(String(255), nullable=False)
    notice_link: Mapped[str] = Column(String(1024), nullable=True)
    tender_date: Mapped[date] = Column(Date, nullable=True)
    deleted: Mapped[bool] = Column(Boolean, nullable=False, default=False)

    create_at: Mapped[datetime] = Column(DateTime, nullable=False, default=datetime.now)
    update_at: Mapped[datetime] = Column(DateTime, nullable=False, onupdate=datetime.now)

