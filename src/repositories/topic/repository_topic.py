from decimal import Decimal
from typing import List

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.core.constraints import HttpStatus, Points
from src.db.model.models import Topic, Subject, PublicTender
from src.enums.enum_status import EnumStatus
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

            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

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
                    raise DatabaseException("topic not found", HttpStatus.NOT_FOUND)

                topic_dto.deleted = False
                topic_dto.status = EnumStatus.INCOMPLETE

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
                    raise DatabaseException("any topic found by subject id", HttpStatus.NOT_FOUND)

            return [
                await TopicResponse.model_validate(topic)
                for topic in topics
            ]
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

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
                    raise DatabaseException("any topic found by name", HttpStatus.NOT_FOUND)

            return [
                await TopicResponse.model_validate(topic)
                for topic in topics
            ]
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

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
                    raise DatabaseException("any topic found by status", HttpStatus.NOT_FOUND)

            return [
                await TopicResponse.model_validate(topic)
                for topic in topics
            ]
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def finish_topic(self, topic_id: int) -> TopicResponse:
        try:
            seventh_five_percent = Decimal("75.0")
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(Topic).options(
                        joinedload(Topic.subject).
                        joinedload(Subject.public_tender).
                        joinedload(PublicTender.user)
                    ).filter(
                        and_(
                            Topic.topic_id == topic_id,
                            not Topic.deleted
                        )
                    )
                )

                topic = response.scalar_one_or_none()

                if not topic:
                    raise DatabaseException("topic not found", HttpStatus.NOT_FOUND)

                can_finish = (
                    topic.fulfillment >= seventh_five_percent and
                    topic.subject and topic.subject.public_tender and
                    topic.subject.public_tender.user
                )

                if can_finish:
                    topic.status = EnumStatus.COMPLETE
                    topic.subject.public_tender.user.points += Points.TOPICS_POINTS
                else:
                    raise DatabaseException("topic is not complete - less than 75%", HttpStatus.BAD_REQUEST)

                await session.commit()
                await session.refresh(topic)
            return await TopicResponse.model_validate(topic)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

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
                    raise DatabaseException("topic not found", HttpStatus.NOT_FOUND)

                topic.deleted = True

                await session.commit()
                await session.refresh(topic)
            return await TopicResponse.model_validate(topic)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

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
