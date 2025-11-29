from decimal import Decimal
from re import match
from typing import Dict, Any, Optional

from src.core.constraints import HttpStatus
from src.exceptions.topic_exception import TopicException
from src.models_dtos.topic_dto import TopicDTO
from src.utils.payload_dto import payload_dto
from src.utils.regex import Regex


class TopicManager:
    @classmethod
    async def convert_payload_to_topic_dto(cls, data_body: Dict[str, Any]) -> TopicDTO:
        topic_exception = TopicException("invalid payload for topic", HttpStatus.UNPROCESSABLE_ENTITY)

        topic_dto = await payload_dto(data_body, TopicDTO, topic_exception)

        return TopicDTO(**topic_dto.model_dump())

    @classmethod
    async def make_validation(cls, topic_dto: TopicDTO) -> None:
        await cls._check_topic_deleted_(topic_dto)
        await cls._check_topics_strings_length_(topic_dto)

    @classmethod
    async def verify_fulfillment_none(cls, fulfillment: Optional[Decimal]) -> None:
        if not fulfillment:
            raise TopicException("topic fulfillment is required", HttpStatus.BAD_REQUEST)

    @classmethod
    async def lock_unfinished_notes_topic(cls, unfinished_notes: bool) -> None:
        if unfinished_notes:
            raise TopicException("there are unfinished notes", HttpStatus.BAD_REQUEST)

    @classmethod
    async def verify_fulfillment(cls, fulfillment: Optional[Decimal], minimal: Decimal) -> None:
        if not fulfillment:
            raise TopicException("topic fulfillment is required", HttpStatus.BAD_REQUEST)
        if fulfillment < minimal:
            raise TopicException(f"topic fulfillment must be at least {minimal}", HttpStatus.BAD_REQUEST)

    @classmethod
    async def _check_topic_deleted_(cls, topic_dto: TopicDTO) -> None:
        if topic_dto.deleted:
            raise TopicException("topic was deleted", HttpStatus.NOT_FOUND)

    @classmethod
    async def _check_topics_strings_length_(cls, topic_dto: TopicDTO) -> None:
        if not match(Regex.STRING_255.value, topic_dto.name):
            raise TopicException(
                "topic name doesn't match between 1 until 255 characters",
                HttpStatus.BAD_REQUEST
            )
        if topic_dto.description and not match(Regex.STRING_1024.value, topic_dto.description):
            raise TopicException(
                "topic description doesn't match between 1 until 1024 characters",
                HttpStatus.BAD_REQUEST
            )
