from typing import List

from src.models_dtos.note_topic_dto import NoteTopicDTO
from src.models_responses.note_topic_response import NoteTopicResponse
from src.services.note_topic.service_note_topic_interface import ServiceNoteTopicInterface
from src.utils.managers.note_topic_manager import NoteTopicManager


class ServiceNoteTopic(ServiceNoteTopicInterface):
    async def create_note_topic(self, note_topic: NoteTopicDTO) -> NoteTopicResponse:
        await NoteTopicManager.make_validation(note_topic)
        pass

    async def update_note_topic(self, note_topic: NoteTopicDTO, note_topic_id: int) -> NoteTopicResponse:
        await NoteTopicManager.make_validation(note_topic)
        pass

    async def find_note_topic_by_topic_id(self, topic_id: int) -> List[NoteTopicResponse]:
        pass

    async def finish_note_topic(self, note_topic: NoteTopicDTO, note_topic_id: int) -> NoteTopicResponse:
        await NoteTopicManager.make_validation(note_topic)
        await NoteTopicManager.rate_success_seventh_percent(note_topic)
        pass

    async def delete_note_topic(self, note_topic_id: int) -> NoteTopicResponse:
        pass
