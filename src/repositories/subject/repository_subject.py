from decimal import Decimal
from typing import List

from sqlalchemy import select, and_, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from src.core.constraints import HttpStatus, Points
from src.db.model.models import Subject, PublicTender, RateLog, User
from src.enums.enum_status import EnumStatus
from src.exceptions.database_exception import DatabaseException
from src.exceptions.subject_exception import SubjectException
from src.models_dtos.subject_dto import SubjectDTO
from src.models_responses.subject_response import SubjectResponse
from src.repositories.subject.repository_subject_interface import SubjectRepositoryInterface
from src.utils.managers.subject_manager import SubjectManager


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
            print(f"Unexcepted Erro Found: {str(e)}")
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
            print(f"Unexcepted Erro Found: {str(e)}")
            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def update_subject_fulfillment(self, fulfillment: Decimal, subject_id: int, user_id: int) -> SubjectResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(Subject)
                    .options(
                        joinedload(Subject.public_tender)
                    )
                    .filter(
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
                public_tender_id = subject.public_tender.public_tender_id

                rate_log = RateLog(user_id=user_id, rate=fulfillment, public_tender_id=public_tender_id, subject=True)

                session.add(rate_log)
                await session.commit()
                await session.refresh(subject)
            return SubjectResponse.model_validate(subject)
        except DatabaseException as e:
            raise e
        except Exception as e:
            print(f"Unexcepted Erro Found: {str(e)}")
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
            print(f"Unexcepted Erro Found: {str(e)}")
            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def finish_subject(self, subject_id: int) -> SubjectResponse:
        try:
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

                await SubjectManager.verify_fulfillment(subject.fulfillment, Decimal("75.0"))

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
        except SubjectException as e:
            raise e
        except DatabaseException as e:
            raise e
        except Exception as e:
            print(f"Unexcepted Erro Found: {str(e)}")
            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def delete_subject(self, subject_id: int) -> SubjectResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(Subject).options(
                        selectinload(Subject.note_subjects),
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

                note_subjects = subject.note_subjects or []

                finished_all_note_subjects = all(note_subject.finish for note_subject in note_subjects)

                if not finished_all_note_subjects:
                    raise DatabaseException("there is at least one note subject not finished", HttpStatus.BAD_REQUEST)

                user_id = subject.public_tender.user.user_id
                len_subjects = len(note_subjects)
                points_decrease = len_subjects * Points.NOTE_POINTS + Points.SUBJECT_POINTS

                await session.execute(
                    update(User).where(User.user_id == user_id).values(points=User.points - points_decrease)
                )

                await session.commit()
                await session.refresh(subject)
            return SubjectResponse.model_validate(subject)
        except DatabaseException as e:
            raise e
        except Exception as e:
            print(f"Unexcepted Erro Found: {str(e)}")
            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)
