from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncEngine

from src.db.core.db_base import get_engine


class TopicRepositoryInterface(ABC):
    @abstractmethod
    async def create_topic(self, topic_dto: TopicDTO) -> TopicResponse:
        pass

    @abstractmethod
    async def update_topic(self, topic_dto: TopicDTO, topic_id: int) -> TopicResponse:
        pass

    @abstractmethod
    async def get_topics(self, subject_id: int) -> List[TopicResponse]:
        pass

    @abstractmethod
    async def get_topic_by_name(self, subject_id: int, name: str) -> List[TopicResponse]:
        pass

    @abstractmethod
    async def get_topic_by_status(self, subject_id: int, status: str) -> List[TopicResponse]:
        pass

    @abstractmethod
    async def delete_topic(self, topic_id: int) -> TopicResponse:
        pass

    @property
    def _engine_(self) -> AsyncEngine:
        eng = get_engine()
        return next(eng)
