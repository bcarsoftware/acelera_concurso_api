from decimal import Decimal
from typing import List

from sqlalchemy import select, and_, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from src.core.constraints import HttpStatus, Points
from src.db.model.models import NoteSubject, Subject, PublicTender, RateLog, User
from src.exceptions.database_exception import DatabaseException
from src.exceptions.note_exception import NoteException
from src.models_dtos.note_subject_dto import NoteSubjectDTO
from src.models_responses.note_subject_response import NoteSubjectResponse
from src.repositories.note_subject.repository_note_subject_interface import NoteSubjectRepositoryInterface
from src.utils.managers.note_subject_manager import NoteSubjectManager


class NoteSubjectRepository(NoteSubjectRepositoryInterface):
    async def create_note_subject(self, note_subject: NoteSubjectDTO) -> NoteSubjectResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                note_subject_orm = NoteSubject(**note_subject.model_dump())
                session.add(note_subject_orm)
                await session.commit()
                await session.refresh(note_subject_orm)
            return NoteSubjectResponse.model_validate(note_subject_orm)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def update_note_subject(self, note_subject: NoteSubjectDTO, note_subject_id: int) -> NoteSubjectResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(NoteSubject).filter(
                        and_(
                            NoteSubject.note_subject_id == note_subject_id,
                            NoteSubject.deleted == False
                        )
                    )
                )

                note_subject_orm = response.scalar_one_or_none()

                if not note_subject_orm:
                    raise DatabaseException("note subject not found", HttpStatus.NOT_FOUND)

                note_subject.finish = False
                note_subject.deleted = False

                for key, value in note_subject.model_dump().items():
                    setattr(note_subject_orm, key, value)

                await session.commit()
                await session.refresh(note_subject_orm)
            return NoteSubjectResponse.model_validate(note_subject_orm)
        except DatabaseException as e:
            raise e
        except Exception as e:
            print(f"Unexcepted Erro Found: {str(e)}")
            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def update_note_subject_rate_success(self, rate_success: Decimal, note_subject_id: int, user_id: int) -> NoteSubjectResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(NoteSubject)
                    .options(
                        joinedload(NoteSubject.subject)
                        .joinedload(Subject.public_tender)
                    )
                    .filter(
                        and_(
                            NoteSubject.note_subject_id == note_subject_id,
                            NoteSubject.deleted == False
                        )
                    )
                )

                note_subject = response.scalar_one_or_none()

                if not note_subject:
                    raise DatabaseException("note subject not found", HttpStatus.NOT_FOUND)

                public_tender_id = note_subject.subject.public_tender.public_tender_id

                note_subject.rate_success = rate_success
                rate_log = RateLog(user_id=user_id, rate=rate_success, public_tender_id=public_tender_id, note_subject=True)

                session.add(rate_log)
                await session.commit()
                await session.refresh(note_subject)
            return NoteSubjectResponse.model_validate(note_subject)
        except DatabaseException as e:
            raise e
        except Exception as e:
            print(f"Unexcepted Erro Found: {str(e)}")
            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def find_note_subject_by_subject_id(self, subject_id: int) -> List[NoteSubjectResponse]:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(NoteSubject).filter(
                        and_(
                            NoteSubject.subject_id == subject_id,
                            NoteSubject.deleted == False
                        )
                    )
                )

                note_subjects = response.scalars().all()

                if not note_subjects:
                    raise DatabaseException("note subject not found", HttpStatus.NOT_FOUND)

            return [
                NoteSubjectResponse.model_validate(n_subject)
                for n_subject in note_subjects
            ]
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def finish_note_subject(self, note_subject_id: int) -> NoteSubjectResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(NoteSubject)
                    .options(
                        selectinload(NoteSubject.subject)
                        .selectinload(Subject.public_tender)
                        .selectinload(PublicTender.user)
                    )
                    .filter(
                        and_(
                            NoteSubject.note_subject_id == note_subject_id,
                            NoteSubject.deleted == False,
                            NoteSubject.finish == False
                        )
                    )
                )

                note_subject = response.scalar_one_or_none()

                if not note_subject:
                    raise DatabaseException("note subject not found", HttpStatus.NOT_FOUND)

                await NoteSubjectManager.verify_rate_success(note_subject.rate_success, Decimal("75.0"))
                user_id = note_subject.subject.public_tender.user.user_id

                await session.execute(
                    update(User).where(User.user_id == user_id).values(points=User.points + Points.NOTE_POINTS)
                )

                await session.commit()
                await session.refresh(note_subject)
            return NoteSubjectResponse.model_validate(note_subject)
        except NoteException as e:
            raise e
        except DatabaseException as e:
            raise e
        except Exception as e:
            print(f"Unexcepted Erro Found: {str(e)}")
            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def delete_note_subject(self, note_subject_id: int) -> NoteSubjectResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(NoteSubject).filter(
                        and_(
                            NoteSubject.note_subject_id == note_subject_id,
                            NoteSubject.deleted == False
                        )
                    )
                )

                note_subject = response.scalar_one_or_none()

                if not note_subject:
                    raise DatabaseException("note subject not found", HttpStatus.NOT_FOUND)

                note_subject.deleted = True

                await session.commit()
                await session.refresh(note_subject)
            return NoteSubjectResponse.model_validate(note_subject)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)
