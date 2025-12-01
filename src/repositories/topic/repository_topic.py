from decimal import Decimal
from typing import List

from sqlalchemy import select, and_, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from src.core.constraints import HttpStatus, Points
from src.db.model.models import Topic, Subject, PublicTender, RateLog, User
from src.enums.enum_status import EnumStatus
from src.exceptions.database_exception import DatabaseException
from src.exceptions.topic_exception import TopicException
from src.models_dtos.topic_dto import TopicDTO
from src.models_responses.topic_response import TopicResponse
from src.repositories.topic.repository_topic_interface import TopicRepositoryInterface
from src.utils.managers.topic_manager import TopicManager


class TopicRepository(TopicRepositoryInterface):
    async def create_topic(self, topic_dto: TopicDTO) -> TopicResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                topic = Topic(**topic_dto.model_dump())
                session.add(topic)
                await session.commit()
                await session.refresh(topic)
            return TopicResponse.model_validate(topic)
        except DatabaseException as e:
            raise e
        except Exception as e:
            print(f"Unexcepted Erro Found: {str(e)}")
            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def update_topic(self, topic_dto: TopicDTO, topic_id: int) -> TopicResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(Topic).filter(
                        and_(
                            Topic.topic_id == topic_id,
                            Topic.deleted == False
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
            return TopicResponse.model_validate(topic)
        except DatabaseException as e:
            raise e
        except Exception as e:
            print(f"Unexcepted Erro Found: {str(e)}")
            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def update_topic_fulfillment(self, fulfillment: Decimal, topic_id: int, user_id: int) -> TopicResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(Topic)
                    .options(
                        joinedload(Topic.subject)
                        .joinedload(Subject.public_tender)
                    )
                    .filter(
                        and_(
                            Topic.topic_id == topic_id,
                            Topic.deleted == False
                        )
                    )
                )

                topic = response.scalar_one_or_none()

                if topic is None:
                    raise DatabaseException("topic not found", HttpStatus.NOT_FOUND)

                topic.fulfillment = fulfillment
                public_tender_id = topic.subject.public_tender.public_tender_id

                rate_log = RateLog(user_id=user_id, rate=fulfillment, public_tender_id=public_tender_id, topic=True)

                session.add(rate_log)
                await session.commit()
                await session.refresh(topic)
            return TopicResponse.model_validate(topic)
        except DatabaseException as e:
            raise e
        except Exception as e:
            print(f"Unexcepted Erro Found: {str(e)}")
            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def get_topics(self, subject_id: int) -> List[TopicResponse]:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(Topic).filter(
                        and_(
                            Topic.subject_id == subject_id,
                            Topic.deleted == False
                        )
                    )
                )

                topics = response.scalars().all()

                if not topics:
                    raise DatabaseException("any topic found by subject id", HttpStatus.NOT_FOUND)

            return [
                TopicResponse.model_validate(topic)
                for topic in topics
            ]
        except DatabaseException as e:
            raise e
        except Exception as e:
            print(f"Unexcepted Erro Found: {str(e)}")
            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def finish_topic(self, topic_id: int) -> TopicResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(Topic).options(
                        selectinload(Topic.note_topics),
                        joinedload(Topic.subject).
                        joinedload(Subject.public_tender).
                        joinedload(PublicTender.user)
                    ).filter(
                        and_(
                            Topic.topic_id == topic_id,
                            Topic.deleted == False,
                            Topic.status == EnumStatus.INCOMPLETE,
                        )
                    )
                )

                topic = response.scalar_one_or_none()

                if not topic:
                    raise DatabaseException("topic not found", HttpStatus.NOT_FOUND)

                await TopicManager.verify_fulfillment(topic.fulfillment, Decimal("75.0"))

                note_topics = topic.note_topics or []

                finished_all_note_topics = all(note_topic.finish for note_topic in note_topics)

                if not finished_all_note_topics:
                    raise DatabaseException("there's at least one note topic not finished", HttpStatus.BAD_REQUEST)

                user_id = topic.subject.public_tender.user.user_id

                await session.execute(
                    update(User).where(User.user_id == user_id).values(points=User.points + Points.TOPICS_POINTS)
                )

                await session.commit()
                await session.refresh(topic)
            return TopicResponse.model_validate(topic)
        except TopicException as e:
            raise e
        except DatabaseException as e:
            raise e
        except Exception as e:
            print(f"Unexcepted Erro Found: {str(e)}")
            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def delete_topic(self, topic_id: int) -> TopicResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(Topic).options(
                        selectinload(Topic.note_topics),
                        joinedload(Topic.subject).
                        joinedload(Subject.public_tender).
                        joinedload(PublicTender.user)
                    ).filter(
                        and_(
                            Topic.topic_id == topic_id,
                            Topic.deleted == False,
                        )
                    )
                )

                topic = response.scalar_one_or_none()

                if not topic:
                    raise DatabaseException("topic not found", HttpStatus.NOT_FOUND)

                note_topics = topic.note_topics or []

                finished_all_note_topics = all(note_topic.finish for note_topic in note_topics)

                if not finished_all_note_topics:
                    raise DatabaseException("there's at least one note topic not finished", HttpStatus.BAD_REQUEST)

                topic.deleted = True
                points_decrease = len(note_topics) * Points.NOTE_POINTS + Points.TOPICS_POINTS

                user_id = Topic.subject.public_tender.user.user_id

                await session.execute(
                    update(User).where(User.user_id == user_id).values(points=User.points - points_decrease)
                )

                await session.commit()
                await session.refresh(topic)
            return TopicResponse.model_validate(topic)
        except DatabaseException as e:
            raise e
        except Exception as e:
            print(f"Unexcepted Erro Found: {str(e)}")
            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)
