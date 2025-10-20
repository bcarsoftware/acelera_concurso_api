from datetime import date
from re import match
from typing import Dict, Any

from src.exceptions.public_tender_exception import PublicTenderException
from src.models_dtos.public_tender_dto import PublicTenderDTO
from src.utils.payload_dto import payload_dto
from src.utils.regex import Regex


class PublicTenderManager:
    @classmethod
    async def convert_payload_to_public_tender_dto(cls, data_body: Dict[str, Any]) -> PublicTenderDTO:
        public_tender_exception = PublicTenderException("invalid payload for public tender", 422)

        public_tender_dto = await payload_dto(data_body, PublicTenderDTO, public_tender_exception)

        return PublicTenderDTO(**public_tender_dto)

    @classmethod
    async def make_validation(cls, public_tender_dto: PublicTenderDTO) -> None:
        await cls._check_public_tender_deleted_(public_tender_dto)
        await cls._check_tender_date_(public_tender_dto)
        await cls._check_public_tender_strings_length_(public_tender_dto)

    @classmethod
    async def _check_public_tender_deleted_(cls, public_tender_dto: PublicTenderDTO) -> None:
        if public_tender_dto.deleted:
            raise PublicTenderException("public tender deleted")

    @classmethod
    async def _check_tender_date_(cls, public_tender_dto: PublicTenderDTO) -> None:
        if public_tender_dto.tender_date < date.today():
            raise PublicTenderException("public tender date can't be before today")

    @classmethod
    async def _check_public_tender_strings_length_(cls, public_tender_dto: PublicTenderDTO) -> None:
        if not match(Regex.STRING_255.value, public_tender_dto.tender_name):
            raise PublicTenderException("public tender name length doesn't match between 1 until 255 characters")
        if not match(Regex.STRING_255.value, public_tender_dto.tender_board):
            raise PublicTenderException("public tender board length doesn't match between 1 until 255 characters")
        if public_tender_dto.notice_link and not match(Regex.STRING_1024.value, public_tender_dto.notice_link):
            raise PublicTenderException("public tender notice link length doesn't match between 1 until 1024 characters")
        if public_tender_dto.institute and not match(Regex.STRING_128.value, public_tender_dto.institute):
            raise PublicTenderException("public tender institute length doesn't match between 1 until 128 characters")
        if not match(Regex.STRING_128.value, public_tender_dto.work_tile):
            raise PublicTenderException("public tender work tile length doesn't match between 1 until 128 characters")
