from decimal import Decimal
from typing import List

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from src.core.constraints import HttpStatus, Points
from src.db.model.models import Subject, PublicTender
from src.enums.enum_status import EnumStatus
from src.exceptions.database_exception import DatabaseException
from src.models_dtos.subject_dto import SubjectDTO
from src.models_responses.subject_response import SubjectResponse
from src.repositories.subject.repository_subject_interface import SubjectRepositoryInterface


class SubjectRepository(SubjectRepositoryInterface):
    async def create_subject(self, subject_dto: SubjectDTO) -> SubjectResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                subject = Subject(**subject_dto.model_dump())
                session.add(subject)
                await session.commit()
                await session.refresh(subject)
            return SubjectResponse.model_validate(subject)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def update_subject(self, subject_dto: SubjectDTO, subject_id: int) -> SubjectResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(Subject).filter(
                        and_(
                            Subject.subject_id == subject_id,
                            not Subject.deleted
                        )
                    )
                )

                subject = response.scalar_one_or_none()

                if not subject:
                    raise DatabaseException("subject not found", HttpStatus.NOT_FOUND)

                subject_dto.deleted = False
                subject_dto.status = EnumStatus.INCOMPLETE

                for key, value in subject_dto.model_dump().items():
                    setattr(subject, key, value)

                await session.commit()
                await session.refresh(subject)
            return SubjectResponse.model_validate(subject)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def get_subjects(self, tender_id: int) -> List[SubjectResponse]:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(Subject).filter(
                        and_(
                            Subject.public_tender_id == tender_id,
                            not Subject.deleted
                        )
                    )
                )

                subjects = response.scalars().all()

                if not subjects:
                    raise DatabaseException("any subject found by name and tender id", HttpStatus.NOT_FOUND)

            return [
                SubjectResponse.model_validate(subject)
                for subject in subjects
            ]
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def get_subject_by_name(self, tender_id: int, name: str) -> List[SubjectResponse]:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(Subject).filter(
                        and_(
                            Subject.name == name,
                            Subject.public_tender_id == tender_id,
                            not Subject.deleted
                        )
                    )
                )

                subjects = response.scalars().all()

                if not subjects:
                    raise DatabaseException("any subject found by name and tender id", HttpStatus.NOT_FOUND)

            return [
                SubjectResponse.model_validate(subject)
                for subject in subjects
            ]
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def finish_subject(self, subject_id: int) -> SubjectResponse:
        try:
            seventh_five_percent = Decimal("75.0")
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(Subject).options(
                        selectinload(Subject.topics),
                        joinedload(Subject.public_tender).joinedload(PublicTender.user)
                    ).filter(
                        and_(
                            Subject.subject_id == subject_id,
                            not Subject.deleted
                        )
                    )
                )

                subject = response.scalar_one_or_none()

                if not subject:
                    raise DatabaseException("subject not found", HttpStatus.NOT_FOUND)

                topics = subject.topics

                if not topics:
                    raise DatabaseException("subject topics not found", HttpStatus.NOT_FOUND)

                topics = tuple(rate for rate in subject.topics if rate is not None)

                average = (
                    sum(map(lambda topic: topic.fulfillment, topics)) / len(topics)
                ) if len(topics) > 0 else Decimal("0.0")

                can_finish = average >= seventh_five_percent and subject.public_tender and subject.public_tender.user

                if can_finish:
                    subject.status = EnumStatus.COMPLETE
                    subject.public_tender.user.points += Points.SUBJECT_POINTS
                else:
                    raise DatabaseException("subject is not complete - less than 75%", HttpStatus.BAD_REQUEST)

                await session.commit()
                await session.refresh(subject)
            return SubjectResponse.model_validate(subject)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def delete_subject(self, subject_id: int, points: int) -> SubjectResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(Subject).options(
                        joinedload(Subject.public_tender).
                        joinedload(PublicTender.user)
                    ).filter(
                        and_(
                            Subject.subject_id == subject_id,
                            not Subject.deleted
                        )
                    )
                )

                subject = response.scalar_one_or_none()

                if not subject:
                    raise DatabaseException("subject not found", HttpStatus.NOT_FOUND)

                if not subject.public_tender or not subject.public_tender.user:
                    raise DatabaseException("subject is broken", HttpStatus.UNPROCESSABLE_ENTITY)

                subject.deleted = True
                subject.public_tender.user.points -= points
                await session.commit()
                await session.refresh(subject)
            return SubjectResponse.model_validate(subject)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)
