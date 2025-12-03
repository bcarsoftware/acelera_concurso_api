from decimal import Decimal
from typing import Dict, Any, Optional

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

        return NoteSubjectDTO(**note_subject.model_dump())

    @classmethod
    async def make_validation(cls, note_subject: NoteSubjectDTO) -> None:
        await cls._check_note_subject_deleted_(note_subject)
        await cls._check_note_subject_strings_length_(note_subject)

    @classmethod
    async def verify_rate_success_none(cls, rate_success: Optional[Decimal]) -> None:
        if not rate_success:
            raise NoteException("note subject rate success is required", HttpStatus.BAD_REQUEST)

    @classmethod
    async def verify_rate_success(cls, rate_success: Optional[Decimal], minimal: Decimal) -> None:
        if not rate_success:
            raise NoteException("note subject rate success is required", HttpStatus.BAD_REQUEST)
        if rate_success < minimal:
            raise NoteException(f"note subject rate success must be at least {minimal}", HttpStatus.BAD_REQUEST)

    @classmethod
    async def _check_note_subject_deleted_(cls, note_subject: NoteSubjectDTO) -> None:
        if note_subject.deleted:
            raise NoteException(
                "note subject was deleted",
                HttpStatus.NOT_FOUND
            )

    @classmethod
    async def _check_note_subject_strings_length_(cls, note_subject: NoteSubjectDTO) -> None:
        if not Regex.STRING_255.value.match(note_subject.name):
            raise NoteException(
                "note subject name doesn't match between 1 util 255 characters",
                HttpStatus.BAD_REQUEST
            )
        if not Regex.STRING_1024.value.match(note_subject.description):
            raise NoteException(
                "note subject description doesn't match between 1 until 1024 characters",
                HttpStatus.BAD_REQUEST
            )
