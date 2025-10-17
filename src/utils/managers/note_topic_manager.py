from re import match
from typing import Dict, Any

from src.exceptions.note_exception import NoteException
from src.models_dtos.note_topic_dto import NoteTopicDTO
from src.utils.payload_dto import payload_dto
from src.utils.regex import Regex


class NoteTopicManager:
    @classmethod
    async def convert_payload_to_note_subject_dto(cls, data_body: Dict[str, Any]) -> NoteTopicDTO:
        note_subject_exception = NoteException("invalid payload for note topic")

        note_subject = await payload_dto(data_body, NoteTopicDTO, note_subject_exception)

        return NoteTopicDTO(**note_subject)

    @classmethod
    async def make_validation(cls, note_subject: NoteTopicDTO) -> None:
        await cls._check_note_topic_deleted_(note_subject)
        await cls._check_note_topic_strings_length_(note_subject)

    @classmethod
    async def _check_note_topic_deleted_(cls, note_subject: NoteTopicDTO) -> None:
        if note_subject.deleted:
            raise NoteException("note topic was deleted")

    @classmethod
    async def _check_note_topic_strings_length_(cls, note_topic: NoteTopicDTO) -> None:
        if not match(Regex.STRING_1024.value, note_topic.description):
            raise NoteException("note topic description doesn't match between 1 until 1024 characters")
