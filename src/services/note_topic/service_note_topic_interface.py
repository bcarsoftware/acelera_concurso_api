from abc import ABC, abstractmethod
from decimal import Decimal
from typing import List, Optional

from src.models_dtos.note_topic_dto import NoteTopicDTO
from src.models_responses.note_topic_response import NoteTopicResponse


class ServiceNoteTopicInterface(ABC):
    @abstractmethod
    async def create_note_topic(self, note_topic: NoteTopicDTO) -> NoteTopicResponse:
        pass

    @abstractmethod
    async def update_note_topic(self, note_topic: NoteTopicDTO, note_topic_id: int) -> NoteTopicResponse:
        pass

    @abstractmethod
    async def update_note_topic_rate_success(self, rate_success: Optional[Decimal], note_topic_id: int) -> NoteTopicResponse:
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
