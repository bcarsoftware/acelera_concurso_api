from re import match
from typing import Dict, Any

from src.exceptions.subject_exception import SubjectException
from src.models_dtos.subject_dto import SubjectDTO
from src.utils.payload_dto import payload_dto
from src.utils.regex import Regex


class SubjectManager:
    @classmethod
    async def convert_payload_to_subject_dto(cls, data_body: Dict[str, Any]) -> SubjectDTO:
        public_tender_exception = SubjectException("invalid payload for subject", 422)

        subject_dto = await payload_dto(data_body, SubjectDTO, public_tender_exception)

        return SubjectDTO(**subject_dto)

    @classmethod
    async def make_validation(cls, subject_dto: SubjectDTO) -> None:
        await cls._check_subject_deleted_(subject_dto)
        await cls._check_subject_strings_length_(subject_dto)

    @classmethod
    async def _check_subject_deleted_(cls, subject_dto: SubjectDTO) -> None:
        if subject_dto.deleted:
            raise SubjectException("subject was deleted")

    @classmethod
    async def _check_subject_strings_length_(cls, subject_dto: SubjectDTO) -> None:
        if not match(Regex.STRING_255.value, subject_dto.name):
            raise SubjectException("subject name length doesn't match between 1 until 255 characters")
