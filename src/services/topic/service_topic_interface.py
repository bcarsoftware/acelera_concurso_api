from abc import ABC, abstractmethod
from typing import List

from src.models_dtos.topic_dto import TopicDTO
from src.models_responses.topic_response import TopicResponse


class ServiceTopicInterface(ABC):
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
    async def delete_topic(self, request: Request, topic_id: int) -> TopicResponse:
        pass
