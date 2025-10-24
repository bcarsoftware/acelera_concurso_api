from re import match
from typing import Any, Dict

from src.core.constraints import HttpStatus
from src.exceptions.study_tips_exception import StudyTipsException
from src.models_dtos.study_tips_dto import StudyTipsDTO
from src.utils.payload_dto import payload_dto
from src.utils.regex import Regex


class TopicManager:
    @classmethod
    async def convert_payload_to_study_tips_dto(cls, data_body: Dict[str, Any]) -> StudyTipsDTO:
        study_tips_exception = StudyTipsException(
            "invalid payload for study tips",
            HttpStatus.UNPROCESSABLE_ENTITY
        )

        study_tips_dto = await payload_dto(data_body, StudyTipsDTO, study_tips_exception)

        return StudyTipsDTO(**study_tips_dto)

    @classmethod
    async def make_validation(cls, study_tips_dto: StudyTipsDTO) -> None:
        await cls._check_study_tips_deleted_(study_tips_dto)
        await cls._check_study_tips_strings_length_(study_tips_dto)

    @classmethod
    async def _check_study_tips_deleted_(cls, study_tips_dto: StudyTipsDTO) -> None:
        if study_tips_dto.deleted:
            raise StudyTipsException(
                "study tip has been deleted",
                HttpStatus.NOT_FOUND
            )

    @classmethod
    async def _check_study_tips_strings_length_(cls, study_tips_dto: StudyTipsDTO) -> None:
        if not match(Regex.STRING_255.value, study_tips_dto.name):
            raise StudyTipsException(
                "name doesn't match length between 1 until 255 characters",
                HttpStatus.NOT_FOUND
            )
        if study_tips_dto.description and not match(Regex.STRING_1024.value, study_tips_dto.description):
            raise StudyTipsException(
                "description doesn't match length between 1 until 1024 characters",
                HttpStatus.BAD_REQUEST
            )
