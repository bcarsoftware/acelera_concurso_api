from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.constraints import HttpStatus
from src.db.model.models import NoteTopic
from src.exceptions.database_exception import DatabaseException
from src.models_dtos.note_topic_dto import NoteTopicDTO
from src.models_responses.note_topic_response import NoteTopicResponse
from src.repositories.note_topic.repository_note_topic_interface import NoteTopicRepositoryInterface


class NoteTopicRepository(NoteTopicRepositoryInterface):
    async def create_note_topic(self, note_topic: NoteTopicDTO) -> NoteTopicResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                note_topic_orm = NoteTopic(**note_topic.model_dump())
                session.add(note_topic_orm)
                await session.commit()
                await session.refresh(note_topic_orm)
            return NoteTopicResponse.model_validate(note_topic_orm)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def update_note_topic(self, note_topic: NoteTopicDTO, note_topic_id: int) -> NoteTopicResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(NoteTopic).filter(
                        and_(
                            NoteTopic.note_topic_id == note_topic_id,
                            not NoteTopic.deleted
                        )
                    )
                )

                note_topic_orm = response.scalar_one_or_none()

                if not note_topic_orm:
                    raise DatabaseException("note topic not found", HttpStatus.NOT_FOUND)

                note_topic.finish = False
                note_topic.deleted = False

                for key, value in note_topic.model_dump().items():
                    setattr(note_topic_orm, key, value)

                await session.commit()
                await session.refresh(note_topic_orm)
            return await NoteTopicResponse.model_validate(note_topic_orm)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def find_note_topic_by_topic_id(self, topic_id: int) -> List[NoteTopicResponse]:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(NoteTopic).filter(
                        and_(
                            NoteTopic.topic_id == topic_id,
                            not NoteTopic.deleted
                        )
                    )
                )

                note_topics = response.scalars().all()

                if not note_topics:
                    raise DatabaseException("note topic not found", HttpStatus.NOT_FOUND)

            return [
                await NoteTopicResponse.model_validate(note_topic)
                for note_topic in note_topics
            ]
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def finish_note_topic(self, note_topic: NoteTopicDTO, note_topic_id: int) -> NoteTopicResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(NoteTopic).filter(
                        and_(
                            NoteTopic.note_topic_id == note_topic_id,
                            not NoteTopic.deleted
                        )
                    )
                )

                note_topic_data = response.scalar_one_or_none()

                if not note_topic_data:
                    raise DatabaseException("note topic not found", HttpStatus.NOT_FOUND)

                for key, value in note_topic.model_dump().items():
                    setattr(note_topic_data, key, value)

                note_topic_data.topic.subject.public_tender.user.points += 5

                await session.commit()
                await session.refresh(note_topic_data)
            return await NoteTopicResponse.model_validate(note_topic_data)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def delete_note_topic(self, note_topic_id: int) -> NoteTopicResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(NoteTopic).filter(
                        and_(
                            NoteTopic.note_topic_id == note_topic_id,
                            not NoteTopic.deleted
                        )
                    )
                )

                note_topic = response.scalar_one_or_none()

                if not note_topic:
                    raise DatabaseException("note subject not found", HttpStatus.NOT_FOUND)

                note_topic.deleted = True

                await session.commit()
                await session.refresh(note_topic)
            return await NoteTopicResponse.model_validate(note_topic)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)
