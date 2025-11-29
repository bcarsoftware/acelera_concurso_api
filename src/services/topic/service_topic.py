from decimal import Decimal
from typing import List, Optional

from src.core.constraints import Points
from src.models_dtos.topic_dto import TopicDTO
from src.models_responses.topic_response import TopicResponse
from src.repositories.note_topic.repository_note_topic import NoteTopicRepository
from src.repositories.note_topic.repository_note_topic_interface import NoteTopicRepositoryInterface
from src.repositories.topic.repository_topic import TopicRepository
from src.repositories.topic.repository_topic_interface import TopicRepositoryInterface
from src.services.topic.service_topic_interface import ServiceTopicInterface
from src.utils.managers.topic_manager import TopicManager


class ServiceTopic(ServiceTopicInterface):
    def __init__(self) -> None:
        self.topic_repository: TopicRepositoryInterface = TopicRepository()
        self.note_topic_repository: NoteTopicRepositoryInterface = NoteTopicRepository()

    async def create_topic(self, topic_dto: TopicDTO) -> TopicResponse:
        await TopicManager.make_validation(topic_dto)

        return await self.topic_repository.create_topic(topic_dto)

    async def update_topic(self, topic_dto: TopicDTO, topic_id: int) -> TopicResponse:
        await TopicManager.make_validation(topic_dto)

        return await self.topic_repository.update_topic(topic_dto, topic_id)

    async def update_topic_fulfillment(self, fulfillment: Optional[Decimal], topic_id: int, user_id: int) -> TopicResponse:
        await TopicManager.verify_fulfillment_none(fulfillment)

        new_fulfillment = fulfillment or Decimal("0")

        return await self.topic_repository.update_topic_fulfillment(new_fulfillment, topic_id, user_id)

    async def get_topics(self, subject_id: int) -> List[TopicResponse]:
        return await self.topic_repository.get_topics(subject_id)

    async def finish_topic(self, topic_id: int) -> TopicResponse:
        return await self.topic_repository.finish_topic(topic_id)

    async def delete_topic(self, topic_id: int) -> TopicResponse:
        note_topics_unfinished = await self.note_topic_repository.exists_note_topics_incomplete(topic_id)

        await TopicManager.lock_unfinished_notes_topic(note_topics_unfinished)

        counted_notes_finished = await self.note_topic_repository.count_finished_note_topics(topic_id)
        points = counted_notes_finished * Points.NOTE_POINTS + Points.TOPICS_POINTS

        return await self.topic_repository.delete_topic(topic_id, points)
