from typing import Any, Dict

from src.core.constraints import HttpStatus
from src.exceptions.rate_log_exception import RateLogException
from src.models_dtos.rate_log_dto import RateLogDTO
from src.utils.payload_dto import payload_dto


class RateLogManager:
    @classmethod
    async def convert_payload_to_rate_log_dto(cls, data_body: Dict[str, Any]) -> RateLogDTO:
        rate_log_exception = RateLogException(
            "invalid payload for study tips",
            HttpStatus.UNPROCESSABLE_ENTITY
        )

        rate_log_dto = await payload_dto(data_body, RateLogDTO, rate_log_exception)

        return RateLogDTO(**rate_log_dto.model_dump())

    @classmethod
    async def make_validation(cls, rate_log_dto: RateLogDTO) -> None:
        invalid = (
            not rate_log_dto.subject and
            not rate_log_dto.topic and
            not rate_log_dto.note_topic and
            not rate_log_dto.note_subject
        )

        if invalid:
            raise RateLogException(
                "you need to define at least one of subject, topic, note_topic, note_subject as true",
                HttpStatus.BAD_REQUEST
            )
