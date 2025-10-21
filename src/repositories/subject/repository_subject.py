from typing import List

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.model.models import Subject
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
            return await SubjectResponse.model_validate(subject)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", 500)

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
                    raise DatabaseException("subject not found", 404)

                for key, value in subject_dto.model_dump().items():
                    setattr(subject, key, value)

                await session.commit()
                await session.refresh(subject)
            return await SubjectResponse.model_validate(subject)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", 500)

    async def get_subjects(self, tender_id: int) -> List[SubjectResponse]:
        try:
            async with AsyncSession(self._engine_) as session:
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
                        raise DatabaseException("any subject found by name and tender id", 404)

                return [
                    await SubjectResponse.model_validate(subject)
                    for subject in subjects
                ]
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", 500)

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
                    raise DatabaseException("any subject found by name and tender id", 404)

            return [
                await SubjectResponse.model_validate(subject)
                for subject in subjects
            ]
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", 500)

    async def delete_subject(self, subject_id: int) -> SubjectResponse:
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
                    raise DatabaseException("subject not found", 404)

                subject.deleted = True
                await session.commit()
                await session.refresh(subject)
            return await SubjectResponse.model_validate(subject)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", 500)
