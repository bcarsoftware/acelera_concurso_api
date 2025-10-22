from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncEngine

from src.db.core.db_base import get_engine


class NoteTopicRepositoryInterface(ABC):
    @abstractmethod
    async def create_note_topic(self, note_topic: NoteTopicDTO) -> NoteTopicResponse:
        pass

    @abstractmethod
    async def update_note_topic(self, note_topic: NoteTopicDTO, note_topic_id: int) -> NoteTopicResponse:
        pass

    @abstractmethod
    async def find_note_topic_by_topic_id(self, topic_id: int) -> List[NoteTopicResponse]:
        pass

    @abstractmethod
    async def finish_note_topic(self, note_topic: NoteTopicDTO, note_topic_id: int) -> NoteTopicResponse:
        pass

    @abstractmethod
    async def delete_note_topic(self, note_topic_id: int) -> NoteTopicResponse:
        pass

    @property
    def _engine_(self) -> AsyncEngine:
        eng = get_engine()
        return next(eng)
