from decimal import Decimal
from re import match
from typing import Dict, Any

from src.core.constraints import HttpStatus
from src.exceptions.note_exception import NoteException
from src.models_dtos.note_subject_dto import NoteSubjectDTO
from src.utils.payload_dto import payload_dto
from src.utils.regex import Regex


class NoteSubjectManager:
    @classmethod
    async def convert_payload_to_note_subject_dto(cls, data_body: Dict[str, Any]) -> NoteSubjectDTO:
        note_subject_exception = NoteException(
            "invalid payload for note subject",
            HttpStatus.UNPROCESSABLE_ENTITY
        )

        note_subject = await payload_dto(data_body, NoteSubjectDTO, note_subject_exception)

        return NoteSubjectDTO(**note_subject)

    @classmethod
    async def make_validation(cls, note_subject: NoteSubjectDTO) -> None:
        await cls._check_note_subject_deleted_(note_subject)
        await cls._check_note_subject_strings_length_(note_subject)

    @classmethod
    async def rate_success_seventh_percent(cls, note_subject: NoteSubjectDTO) -> None:
        seventh_percent = Decimal("70.0")

        if not note_subject.rate_success or note_subject.rate_success < seventh_percent:
            raise NoteException(
                "you can't finish note subject with success rate less than 70%",
                HttpStatus.BAD_REQUEST
            )

    @classmethod
    async def _check_note_subject_deleted_(cls, note_subject: NoteSubjectDTO) -> None:
        if note_subject.deleted:
            raise NoteException(
                "note subject was deleted",
                HttpStatus.NOT_FOUND
            )

    @classmethod
    async def _check_note_subject_strings_length_(cls, note_subject: NoteSubjectDTO) -> None:
        if not match(Regex.STRING_1024.value, note_subject.description):
            raise NoteException(
                "note subject description doesn't match between 1 until 1024 characters",
                HttpStatus.BAD_REQUEST
            )
