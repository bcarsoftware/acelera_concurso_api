from typing import List

from src.models_dtos.topic_dto import TopicDTO
from src.models_responses.topic_response import TopicResponse
from src.services.topic.service_topic_interface import ServiceTopicInterface
from src.utils.managers.topic_manager import TopicManager


class ServiceTopic(ServiceTopicInterface):
    async def create_topic(self, topic_dto: TopicDTO) -> TopicResponse:
        await TopicManager.make_validation(topic_dto)
        pass

    async def update_topic(self, topic_dto: TopicDTO, topic_id: int) -> TopicResponse:
        await TopicManager.make_validation(topic_dto)
        pass

    async def get_topics(self, subject_id: int) -> List[TopicResponse]:
        pass

    async def get_topic_by_name(self, subject_id: int, name: str) -> List[TopicResponse]:
        pass

    async def get_topic_by_status(self, subject_id: int, status: str) -> List[TopicResponse]:
        pass

    async def delete_topic(self, request: Request, topic_id: int) -> TopicResponse:
        pass
