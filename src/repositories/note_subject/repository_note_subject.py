from typing import List

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.constraints import HttpStatus
from src.db.model.models import NoteSubject, PublicTender, Subject, User
from src.exceptions.database_exception import DatabaseException
from src.models_dtos.note_subject_dto import NoteSubjectDTO
from src.models_responses.note_subject_response import NoteSubjectResponse
from src.repositories.note_subject.repository_note_subject_interface import NoteSubjectRepositoryInterface


class NoteSubjectRepository(NoteSubjectRepositoryInterface):
    async def create_note_subject(self, note_subject: NoteSubjectDTO) -> NoteSubjectResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                note_subject_orm = NoteSubject(**note_subject.model_dump())
                session.add(note_subject_orm)
                await session.commit()
                await session.refresh(note_subject_orm)
            return await NoteSubjectResponse.model_validate(note_subject_orm)
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
                            not NoteSubject.deleted
                        )
                    )
                )

                note_subject_orm = response.scalar_one_or_none()

                if not note_subject_orm:
                    raise DatabaseException("note subject not found", 404)

                note_subject.finish = False
                note_subject.deleted = False

                for key, value in note_subject.model_dump().items():
                    setattr(note_subject_orm, key, value)

                await session.commit()
                await session.refresh(note_subject_orm)
            return await NoteSubjectResponse.model_validate(note_subject_orm)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def find_note_subject_by_subject_id(self, subject_id: int) -> List[NoteSubjectResponse]:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(NoteSubject).filter(
                        and_(
                            NoteSubject.subject_id == subject_id,
                            not NoteSubject.deleted
                        )
                    )
                )

                note_subjects = response.scalars().all()

                if not note_subjects:
                    raise DatabaseException("note subject not found", 404)

            return [
                await NoteSubjectResponse.model_validate(n_subject)
                for n_subject in note_subjects
            ]
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def finish_note_subject(self, note_subject: NoteSubjectDTO, note_subject_id: int) -> NoteSubjectResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(NoteSubject).filter(
                        and_(
                            NoteSubject.note_subject_id == note_subject_id,
                            not NoteSubject.deleted
                        )
                    )
                )

                note_subject_data = response.scalar_one_or_none()

                if not note_subject_data:
                    raise DatabaseException("note subject not found", 404)

                for key, value in note_subject.model_dump().items():
                    setattr(note_subject_data, key, value)

                note_subject_data.subject.public_tender.user.points += 5

                await session.commit()
                await session.refresh(note_subject_data)
            return await NoteSubjectResponse.model_validate(note_subject_data)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def delete_note_subject(self, note_subject_id: int) -> NoteSubjectResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(NoteSubject).filter(
                        and_(
                            NoteSubject.note_subject_id == note_subject_id,
                            not NoteSubject.deleted
                        )
                    )
                )

                note_subject = response.scalar_one_or_none()

                if not note_subject:
                    raise DatabaseException("note subject not found", 404)

                note_subject.deleted = True

                await session.commit()
                await session.refresh(note_subject)
            return await NoteSubjectResponse.model_validate(note_subject)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)
