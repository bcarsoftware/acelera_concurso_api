from typing import Any, Dict

from src.core.constraints import HttpStatus
from src.exceptions.send_email_exception import SendEmailException
from src.models_dtos.email_dto import EmailDTO
from src.utils.payload_dto import payload_dto
from src.utils.regex import Regex


class EmailCodeManager:
    @classmethod
    async def convert_payload_to_topic_dto(cls, data_body: Dict[str, Any]) -> EmailDTO:
        email_exception = SendEmailException(
            "invalid payload for checker email",
            HttpStatus.UNPROCESSABLE_ENTITY
        )

        email_dto = await payload_dto(data_body, EmailDTO, email_exception)

        return EmailDTO(**email_dto.model_dump())

    @classmethod
    async def make_validation(cls, email_dto: EmailDTO) -> None:
        if not Regex.STRING_281.value.match(email_dto.email):
            raise SendEmailException("email length isn't between 1 and 281", HttpStatus.BAD_REQUEST)
        if not Regex.EMAIL.value.match(email_dto.email):
            raise SendEmailException("invalid email found", HttpStatus.BAD_REQUEST)
