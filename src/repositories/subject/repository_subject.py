from decimal import Decimal
from typing import List

from sqlalchemy import select, and_, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from src.core.constraints import HttpStatus, Points
from src.db.model.models import Subject, PublicTender, RateLog, User
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
        except DatabaseException as e:
            raise e
        except Exception as e:
            print(f"Unexcepted Erro Found: {type(e).__name__} - {str(e)}")
            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def update_subject(self, subject_dto: SubjectDTO, subject_id: int) -> SubjectResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(Subject).filter(
                        and_(
                            Subject.subject_id == subject_id,
                            Subject.deleted == False
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
        except DatabaseException as e:
            raise e
        except Exception as e:
            print(f"Unexcepted Erro Found: {type(e).__name__} - {str(e)}")
            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def update_subject_fulfillment(self, fulfillment: Decimal, subject_id: int, user_id: int) -> SubjectResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(Subject).filter(
                        and_(
                            Subject.subject_id == subject_id,
                            Subject.deleted == False
                        )
                    )
                )

                subject = response.scalar_one_or_none()

                if not subject:
                    raise DatabaseException("subject not found", HttpStatus.NOT_FOUND)

                subject.fulfillment = fulfillment
                rate_log = RateLog(user_id=user_id, rate=fulfillment, subject=True)

                session.add(rate_log)
                await session.commit()
                await session.refresh(subject)
            return SubjectResponse.model_validate(subject)
        except DatabaseException as e:
            raise e
        except Exception as e:
            print(f"Unexcepted Erro Found: {type(e).__name__} - {str(e)}")
            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def get_subjects(self, tender_id: int) -> List[SubjectResponse]:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(Subject).filter(
                        and_(
                            Subject.public_tender_id == tender_id,
                            Subject.deleted == False
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
        except DatabaseException as e:
            raise e
        except Exception as e:
            print(f"Unexcepted Erro Found: {type(e).__name__} - {str(e)}")
            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def finish_subject(self, subject_id: int) -> SubjectResponse:
        try:
            seventh_five_percent = Decimal("75.0")
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(Subject).options(
                        selectinload(Subject.note_subjects),
                        selectinload(Subject.topics.note_topics),
                        joinedload(Subject.public_tender).joinedload(PublicTender.user)
                    ).filter(
                        and_(
                            Subject.subject_id == subject_id,
                            Subject.deleted == False,
                            Subject.status == EnumStatus.INCOMPLETE
                        )
                    )
                )

                subject = response.scalar_one_or_none()

                if not subject:
                    raise DatabaseException("subject not found", HttpStatus.NOT_FOUND)

                if subject.fulfillment < seventh_five_percent:
                    raise DatabaseException("subject fulfillment must be at least 75", HttpStatus.BAD_REQUEST)

                note_subjects = subject.note_subjects

                finished_all_note_subjects = all(note_subject.finish for note_subject in note_subjects)

                if not finished_all_note_subjects:
                    raise DatabaseException("there's at least one note subject not finished", HttpStatus.BAD_REQUEST)

                topics = subject.topics or []

                topics_and_notes_finished = all(
                    topic.status == EnumStatus.COMPLETE and
                    all(note.finish for note in (topic.note_topics or []))
                    for topic in topics
                )

                if not topics_and_notes_finished:
                    raise DatabaseException("there's at least one topic or note topic that has not finished", HttpStatus.BAD_REQUEST)

                user_id = subject.public_tender.user.user_id
                subject.status = EnumStatus.COMPLETE

                await session.execute(
                    update(User).where(User.user_id == user_id).values(points=User.points + Points.SUBJECT_POINTS)
                )

                await session.commit()
                await session.refresh(subject)
            return SubjectResponse.model_validate(subject)
        except DatabaseException as e:
            raise e
        except Exception as e:
            print(f"Unexcepted Erro Found: {type(e).__name__} - {str(e)}")
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
                            Subject.deleted == False
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
        except DatabaseException as e:
            raise e
        except Exception as e:
            print(f"Unexcepted Erro Found: {type(e).__name__} - {str(e)}")
            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)
