from datetime import date, datetime
from decimal import Decimal
from typing import List

from sqlalchemy import String, Date, Column, Integer, DateTime, Enum, ForeignKey, Boolean, DECIMAL, CheckConstraint
from sqlalchemy.orm import Mapped, relationship

from sqlalchemy.ext.declarative import declarative_base

from src.enums.enum_category import EnumCategory
from src.enums.enum_gender import EnumGender
from src.enums.enum_status import EnumStatus

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = Column(Integer, autoincrement=True, primary_key=True)

    first_name: Mapped[str] = Column(String(64), nullable=False)
    last_name: Mapped[str] = Column(String(255), nullable=False)
    date_born: Mapped[date] = Column(Date, nullable=False)
    gender: Mapped[EnumGender] = Column(Enum(EnumGender, name="EnumGender"), nullable=False)

    username: Mapped[str] = Column(String(128), nullable=False, unique=True)
    email: Mapped[str] = Column(String(282), nullable=False, unique=True)
    password: Mapped[str] = Column(String(255), nullable=False)

    points: Mapped[int] = Column(Integer, nullable=False, default=0)
    deleted: Mapped[bool] = Column(Boolean, nullable=False, default=False)

    study_tips: Mapped[List["StudyTips"]] = relationship(back_populates="user")
    pomodoros: Mapped[List["Pomodoro"]] = relationship(back_populates="user")
    public_tenders: Mapped[List["PublicTender"]] = relationship(back_populates="user")

    create_at: Mapped[datetime] = Column(DateTime, nullable=False, default=datetime.now)
    update_at: Mapped[datetime] = Column(DateTime, nullable=True, onupdate=datetime.now)


class Pomodoro(Base):
    __tablename__ = "pomodoros"

    pomodoro_id: Mapped[int] = Column(Integer, autoincrement=True, primary_key=True)

    user_id: Mapped[int] = Column(
        Integer, ForeignKey(User.user_id, ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="pomodoros")

    pomodoro_name: Mapped[str] = Column(String(128), nullable=False)
    focus_minutes: Mapped[int] = Column(Integer, nullable=False)
    focus_seconds: Mapped[int] = Column(Integer, nullable=False)
    break_short: Mapped[int] = Column(Integer, nullable=False)
    break_long: Mapped[int] = Column(Integer, nullable=False)
    rounds: Mapped[int] = Column(Integer, nullable=False)

    create_at: Mapped[datetime] = Column(DateTime, nullable=False, default=datetime.now)
    update_at: Mapped[datetime] = Column(DateTime, nullable=True, onupdate=datetime.now)


class StudyTips(Base):
    __tablename__ = "study_tips"

    study_tip_id: Mapped[int] = Column(Integer, autoincrement=True, primary_key=True)

    user_id: Mapped[int] = Column(
        Integer, ForeignKey(User.user_id, ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="study_tips")

    name: Mapped[str] = Column(String(255), nullable=False)
    description: Mapped[str] = Column(String(1024), nullable=True)
    ai_generate: Mapped[bool] = Column(Boolean, nullable=False)
    deleted: Mapped[bool] = Column(Boolean, nullable=False, default=False)

    create_at: Mapped[datetime] = Column(DateTime, nullable=False, default=datetime.now)
    update_at: Mapped[datetime] = Column(DateTime, nullable=True, onupdate=datetime.now)


class PublicTender(Base):
    __tablename__ = "public_tenders"

    public_tender_id: Mapped[int] = Column(Integer, autoincrement=True, primary_key=True)

    user_id: Mapped[int] = Column(
        Integer, ForeignKey(User.user_id, ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="public_tenders")

    tender_name: Mapped[str] = Column(String(255), nullable=False)
    tender_board: Mapped[str] = Column(String(255), nullable=False)
    institute: Mapped[str] = Column(String(128), nullable=False)
    work_title: Mapped[str] = Column(String(128), nullable=False)
    notice_link: Mapped[str] = Column(String(1024), nullable=True)
    tender_date: Mapped[date] = Column(Date, nullable=True)
    deleted: Mapped[bool] = Column(Boolean, nullable=False, default=False)

    subjects: Mapped[List["Subject"]] = relationship(back_populates="public_tender")

    create_at: Mapped[datetime] = Column(DateTime, nullable=False, default=datetime.now)
    update_at: Mapped[datetime] = Column(DateTime, nullable=True, onupdate=datetime.now)


class Subject(Base):
    __tablename__ = "subjects"

    subject_id: Mapped[int] = Column(Integer, autoincrement=True, primary_key=True)

    public_tender_id: Mapped[int] = Column(
        Integer, ForeignKey(PublicTender.public_tender_id, ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    public_tender: Mapped["PublicTender"] = relationship(back_populates="subjects")

    name: Mapped[str] = Column(String(255), nullable=False)
    category: Mapped[EnumCategory] = Column(Enum(EnumCategory, name="EnumCategory"), nullable=False)
    status: Mapped[EnumStatus] = Column(Enum(EnumStatus, name="EnumStatus"), nullable=False, default="INCOMPLETE")
    deleted: Mapped[bool] = Column(Boolean, nullable=False, default=False)

    topics: Mapped[List["Topic"]] = relationship(back_populates="subject")
    note_subjects: Mapped[List["NoteSubject"]] = relationship(back_populates="subject")

    create_at: Mapped[datetime] = Column(DateTime, nullable=False, default=datetime.now)
    update_at: Mapped[datetime] = Column(DateTime, nullable=True, onupdate=datetime.now)


class Topic(Base):
    __tablename__ = "topics"

    topic_id: Mapped[int] = Column(Integer, autoincrement=True, primary_key=True)

    subject_id: Mapped[int] = Column(
        Integer, ForeignKey(Subject.subject_id, ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    subject: Mapped["Subject"] = relationship(back_populates="topics")

    name: Mapped[str] = Column(String(255), nullable=False)
    description: Mapped[str] = Column(String(1024), nullable=True)
    fulfillment: Mapped[Decimal] = Column(DECIMAL(10,2), nullable=True)
    status: Mapped[EnumStatus] = Column(Enum(EnumStatus, name="EnumStatus"), nullable=False, default="INCOMPLETE")
    deleted: Mapped[bool] = Column(Boolean, nullable=False, default=False)

    note_topics: Mapped[List["NoteTopic"]] = relationship(back_populates="topic")

    create_at: Mapped[datetime] = Column(DateTime, nullable=False, default=datetime.now)
    update_at: Mapped[datetime] = Column(DateTime, nullable=True, onupdate=datetime.now)


class NoteSubject(Base):
    __tablename__ = "note_subjects"

    note_subject_id: Mapped[int] = Column(Integer, autoincrement=True, primary_key=True)

    subject_id: Mapped[int] = Column(
        Integer, ForeignKey(Subject.subject_id, ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    subject: Mapped["Subject"] = relationship(back_populates="note_subjects")

    name: Mapped[str] = Column(String(255), nullable=False)
    description: Mapped[str] = Column(String(1024), nullable=False)
    finish: Mapped[bool] = Column(Boolean, nullable=False, default=False)
    rate_success: Mapped[Decimal] = Column(DECIMAL(10,2), nullable=True)
    deleted: Mapped[bool] = Column(Boolean, nullable=False, default=False)

    create_at: Mapped[datetime] = Column(DateTime, nullable=False, default=datetime.now)
    update_at: Mapped[datetime] = Column(DateTime, nullable=True, onupdate=datetime.now)


class NoteTopic(Base):
    __tablename__ = "note_topics"

    note_topic_id: Mapped[int] = Column(Integer, autoincrement=True, primary_key=True)

    topic_id: Mapped[int] = Column(
        Integer, ForeignKey(Topic.topic_id, ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    topic: Mapped["Topic"] = relationship(back_populates="note_topics")

    name: Mapped[str] = Column(String(255), nullable=False)
    description: Mapped[str] = Column(String(1024), nullable=False)
    finish: Mapped[bool] = Column(Boolean, nullable=False, default=False)
    rate_success: Mapped[Decimal] = Column(DECIMAL(10,2), nullable=True)
    deleted: Mapped[bool] = Column(Boolean, nullable=False, default=False)

    create_at: Mapped[datetime] = Column(DateTime, nullable=False, default=datetime.now)
    update_at: Mapped[datetime] = Column(DateTime, nullable=True, onupdate=datetime.now)


class UserAdmin(Base):
    __tablename__ = "user_admin"

    user_admin_id: Mapped[int] = Column(Integer, default=1, nullable=False, primary_key=True)

    __table_args__ = (
        CheckConstraint("user_admin_id=1", name="user_admin_check"),
    )

    full_name: Mapped[str] = Column(String(255), nullable=False)
    username: Mapped[str] = Column(String(255), nullable=False, unique=True)
    password: Mapped[str] = Column(String(255), nullable=False)

    public_tender_boards: Mapped[List["PublicTenderBoard"]] = relationship(back_populates="user_admin")

    create_at: Mapped[datetime] = Column(DateTime, nullable=False, default=datetime.now)
    update_at: Mapped[datetime] = Column(DateTime, nullable=True, onupdate=datetime.now)


class PublicTenderBoard(Base):
    __tablename__ = "public_tender_boards"

    public_tender_board_id: Mapped[int] = Column(Integer, autoincrement=True, primary_key=True)

    user_admin_id: Mapped[int] = Column(
        Integer, ForeignKey(UserAdmin.user_admin_id, ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    user_admin: Mapped["UserAdmin"] = relationship(back_populates="public_tender_boards")

    sail: Mapped[str] = Column(String(32), unique=True, nullable=False)
    name: Mapped[str] = Column(String(128), unique=True, nullable=False)

    create_at: Mapped[datetime] = Column(DateTime, nullable=False, default=datetime.now)
    update_at: Mapped[datetime] = Column(DateTime, nullable=True, onupdate=datetime.now)
