from abc import ABC, abstractmethod
from decimal import Decimal
from typing import List, Optional

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
    async def update_topic_fulfillment(self, fulfillment: Optional[Decimal], topic_id: int) -> TopicResponse:
        pass

    @abstractmethod
    async def get_topics(self, subject_id: int) -> List[TopicResponse]:
        pass

    @abstractmethod
    async def finish_topic(self, topic_id: int) -> TopicResponse:
        pass

    @abstractmethod
    async def delete_topic(self, topic_id: int) -> TopicResponse:
        pass
