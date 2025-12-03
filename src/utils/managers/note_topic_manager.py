from decimal import Decimal
from typing import Dict, Any, Optional

from src.core.constraints import HttpStatus
from src.exceptions.note_exception import NoteException
from src.models_dtos.note_topic_dto import NoteTopicDTO
from src.utils.payload_dto import payload_dto
from src.utils.regex import Regex


class NoteTopicManager:
    @classmethod
    async def convert_payload_to_note_topic_dto(cls, data_body: Dict[str, Any]) -> NoteTopicDTO:
        note_topic_exception = NoteException(
            "invalid payload for note topic",
            HttpStatus.UNPROCESSABLE_ENTITY
        )

        note_topic = await payload_dto(data_body, NoteTopicDTO, note_topic_exception)

        return NoteTopicDTO(**note_topic.model_dump())

    @classmethod
    async def make_validation(cls, note_topic: NoteTopicDTO) -> None:
        await cls._check_note_topic_deleted_(note_topic)
        await cls._check_note_topic_strings_length_(note_topic)

    @classmethod
    async def verify_rate_success_none(cls, rate_success: Optional[Decimal]) -> None:
        if not rate_success:
            raise NoteException("note topic rate success is required", HttpStatus.BAD_REQUEST)

    @classmethod
    async def verify_rate_success(cls, rate_success: Optional[Decimal], minimal: Decimal) -> None:
        if not rate_success:
            raise NoteException("note topic rate success is required", HttpStatus.BAD_REQUEST)
        if rate_success < minimal:
            raise NoteException(f"note topic rate success must be at least {minimal}", HttpStatus.BAD_REQUEST)

    @classmethod
    async def rate_success_seventh_percent(cls, note_topic: NoteTopicDTO) -> None:
        seventh_percent = Decimal("70.0")

        if not note_topic.rate_success or note_topic.rate_success < seventh_percent:
            raise NoteException(
                "you can't finish note topic with success rate less than 70%",
                HttpStatus.BAD_REQUEST
            )

    @classmethod
    async def _check_note_topic_deleted_(cls, note_topic: NoteTopicDTO) -> None:
        if note_topic.deleted:
            raise NoteException("note topic was deleted", HttpStatus.NOT_FOUND)

    @classmethod
    async def _check_note_topic_strings_length_(cls, note_topic: NoteTopicDTO) -> None:
        if not Regex.STRING_255.value.match(note_topic.name):
            raise NoteException(
                "note topic name doesn't match between 1 util 255 characters",
                HttpStatus.BAD_REQUEST
            )
        if not Regex.STRING_1024.value.match(note_topic.description):
            raise NoteException(
                "note topic description doesn't match between 1 until 1024 characters",
                HttpStatus.BAD_REQUEST
            )
