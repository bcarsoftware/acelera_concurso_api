from typing import List

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.model.models import Topic
from src.exceptions.database_exception import DatabaseException
from src.models_dtos.topic_dto import TopicDTO
from src.models_responses.topic_response import TopicResponse
from src.repositories.topic.repository_topic_interface import TopicRepositoryInterface


class TopicRepository(TopicRepositoryInterface):
    async def create_topic(self, topic_dto: TopicDTO) -> TopicResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                topic = Topic(**topic_dto.model_dump())
                session.add(topic)
                await session.commit()
                await session.refresh(topic)
            return await TopicResponse.model_validate(topic)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", 500)

    async def update_topic(self, topic_dto: TopicDTO, topic_id: int) -> TopicResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(Topic).filter(
                        and_(
                            Topic.topic_id == topic_id,
                            not Topic.deleted
                        )
                    )
                )

                topic = response.scalar_one_or_none()

                if topic is None:
                    raise DatabaseException("topic not found", 404)

                for key, value in topic_dto.model_dump().items():
                    setattr(topic, key, value)

                await session.commit()
                await session.refresh(topic)
            return await TopicResponse.model_validate(topic)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", 500)

    async def get_topics(self, subject_id: int) -> List[TopicResponse]:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(Topic).filter(
                        and_(
                            Topic.subject_id == subject_id,
                            not Topic.deleted
                        )
                    )
                )

                topics = response.scalars().all()

                if not topics:
                    raise DatabaseException("any topic found by subject id")

            return [
                await TopicResponse.model_validate(topic)
                for topic in topics
            ]
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", 500)

    async def get_topic_by_name(self, subject_id: int, name: str) -> List[TopicResponse]:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(Topic).filter(
                        and_(
                            Topic.subject_id == subject_id,
                            not Topic.deleted
                        )
                    )
                )

                topics = response.scalars().all()

                if not topics:
                    raise DatabaseException("any topic found by name")

            return [
                await TopicResponse.model_validate(topic)
                for topic in topics
            ]
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", 500)

    async def get_topic_by_status(self, subject_id: int, status: str) -> List[TopicResponse]:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(Topic).filter(
                        and_(
                            Topic.subject_id == subject_id,
                            not Topic.deleted
                        )
                    )
                )

                topics = response.scalars().all()

                if not topics:
                    raise DatabaseException("any topic found by status")

            return [
                await TopicResponse.model_validate(topic)
                for topic in topics
            ]
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", 500)

    async def delete_topic(self, topic_id: int) -> TopicResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(Topic).filter(
                        and_(
                            Topic.topic_id == topic_id,
                            not Topic.deleted
                        )
                    )
                )

                topic = response.scalar_one_or_none()

                if not topic:
                    raise DatabaseException("topic not found", 404)

                topic.deleted = True

                await session.commit()
                await session.refresh(topic)
            return await TopicResponse.model_validate(topic)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", 500)

    async def topic_exists(self, topic_id: int) -> bool:
        async with AsyncSession(self._engine_) as session:
            response = await session.execute(
                select(Topic).filter(
                    and_(
                        Topic.topic_id == topic_id,
                        not Topic.deleted
                    )
                )
            )

            result = not response.scalar_one_or_none()
        return not result
