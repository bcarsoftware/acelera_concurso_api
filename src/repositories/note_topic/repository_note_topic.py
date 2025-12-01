from decimal import Decimal
from typing import List

from sqlalchemy import select, and_, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from src.core.constraints import HttpStatus, Points
from src.db.model.models import NoteTopic, Topic, Subject, PublicTender, RateLog, User
from src.exceptions.database_exception import DatabaseException
from src.exceptions.note_exception import NoteException
from src.models_dtos.note_topic_dto import NoteTopicDTO
from src.models_responses.note_topic_response import NoteTopicResponse
from src.repositories.note_topic.repository_note_topic_interface import NoteTopicRepositoryInterface
from src.utils.managers.note_topic_manager import NoteTopicManager


class NoteTopicRepository(NoteTopicRepositoryInterface):
    async def create_note_topic(self, note_topic: NoteTopicDTO) -> NoteTopicResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                note_topic_orm = NoteTopic(**note_topic.model_dump())
                session.add(note_topic_orm)
                await session.commit()
                await session.refresh(note_topic_orm)
            return NoteTopicResponse.model_validate(note_topic_orm)
        except DatabaseException as e:
            raise e
        except Exception as e:
            print(f"Unexcepted Erro Found: {str(e)}")
            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def update_note_topic(self, note_topic: NoteTopicDTO, note_topic_id: int) -> NoteTopicResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(NoteTopic).filter(
                        and_(
                            NoteTopic.note_topic_id == note_topic_id,
                            NoteTopic.deleted == False
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
            return NoteTopicResponse.model_validate(note_topic_orm)
        except DatabaseException as e:
            raise e
        except Exception as e:
            print(f"Unexcepted Erro Found: {str(e)}")
            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def update_note_topic_rate_success(self, rate_success: Decimal, note_topic_id: int, user_id: int) -> NoteTopicResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(NoteTopic)
                    .options(
                        joinedload(NoteTopic.topic)
                        .joinedload(Topic.subject)
                        .joinedload(Subject.public_tender)
                    )
                    .filter(
                        and_(
                            NoteTopic.note_topic_id == note_topic_id,
                            NoteTopic.deleted == False
                        )
                    )
                )

                note_topic = response.scalar_one_or_none()

                if not note_topic:
                    raise DatabaseException("note topic not found", HttpStatus.NOT_FOUND)

                note_topic.rate_success = rate_success
                public_tender_id = note_topic.topic.subject.public_tender.public_tender_id

                rate_log = RateLog(user_id=user_id, rate=rate_success, public_tender_id=public_tender_id, note_topic=True)

                session.add(rate_log)
                await session.commit()
                await session.refresh(note_topic)
            return NoteTopicResponse.model_validate(note_topic)
        except DatabaseException as e:
            raise e
        except Exception as e:
            print(f"Unexcepted Erro Found: {str(e)}")
            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def find_note_topic_by_topic_id(self, topic_id: int) -> List[NoteTopicResponse]:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(NoteTopic).filter(
                        and_(
                            NoteTopic.topic_id == topic_id,
                            NoteTopic.deleted == False
                        )
                    )
                )

                note_topics = response.scalars().all()

                if not note_topics:
                    raise DatabaseException("note topic not found", HttpStatus.NOT_FOUND)

            return [
                NoteTopicResponse.model_validate(note_topic)
                for note_topic in note_topics
            ]
        except DatabaseException as e:
            raise e
        except Exception as e:
            print(f"Unexcepted Erro Found: {str(e)}")
            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def finish_note_topic(self, note_topic_id: int) -> NoteTopicResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(NoteTopic)
                    .options(
                        selectinload(NoteTopic.topic)
                        .selectinload(Topic.subject)
                        .selectinload(Subject.public_tender)
                        .selectinload(PublicTender.user)
                    )
                    .filter(
                        and_(
                            NoteTopic.note_topic_id == note_topic_id,
                            NoteTopic.deleted == False
                        )
                    )
                )

                note_topic = response.scalar_one_or_none()

                if not note_topic:
                    raise DatabaseException("note topic not found", HttpStatus.NOT_FOUND)

                await NoteTopicManager.verify_rate_success(note_topic.rate_success, Decimal("75.0"))

                user_id = note_topic.topic.subject.public_tender.user.user_id

                await session.execute(
                    update(User).where(User.user_id == user_id).values(points=User.points + Points.NOTE_POINTS)
                )

                await session.commit()
                await session.refresh(note_topic)
            return NoteTopicResponse.model_validate(note_topic)
        except NoteException as e:
            raise e
        except DatabaseException as e:
            raise e
        except Exception as e:
            print(f"Unexcepted Erro Found: {str(e)}")
            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def delete_note_topic(self, note_topic_id: int) -> NoteTopicResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(NoteTopic).filter(
                        and_(
                            NoteTopic.note_topic_id == note_topic_id,
                            NoteTopic.deleted == False
                        )
                    )
                )

                note_topic = response.scalar_one_or_none()

                if not note_topic:
                    raise DatabaseException("note subject not found", HttpStatus.NOT_FOUND)

                note_topic.deleted = True

                await session.commit()
                await session.refresh(note_topic)
            return NoteTopicResponse.model_validate(note_topic)
        except DatabaseException as e:
            raise e
        except Exception as e:
            print(f"Unexcepted Erro Found: {str(e)}")
            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)
