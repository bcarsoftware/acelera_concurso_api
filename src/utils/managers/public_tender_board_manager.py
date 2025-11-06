from re import match
from typing import Dict, Any

from src.core.constraints import HttpStatus
from src.exceptions.public_tender_board_exception import PublicTenderBoardException
from src.exceptions.public_tender_exception import PublicTenderException
from src.models_dtos.public_tender_board_dto import PublicTenderBoardDTO
from src.utils.payload_dto import payload_dto
from src.utils.regex import Regex


class PublicTenderBoardManager:
    @classmethod
    async def convert_payload_to_public_tender_board_dto(cls, data_body: Dict[str, Any]) -> PublicTenderBoardDTO:
        public_tender_board_exception = PublicTenderBoardException(
            "invalid payload for public tender board",
            HttpStatus.UNPROCESSABLE_ENTITY
        )

        public_tender_board_dto = await payload_dto(data_body, PublicTenderBoardDTO, public_tender_board_exception)

        return PublicTenderBoardDTO(**public_tender_board_dto.model_dump())

    @classmethod
    async def make_validation(cls, public_tender_board_dto: PublicTenderBoardDTO) -> None:
        await cls._check_public_tender_board_strings_length_(public_tender_board_dto)

    @classmethod
    async def _check_public_tender_board_strings_length_(cls, public_tender_board_dto: PublicTenderBoardDTO) -> None:
        if not match(Regex.STRING_2_32.value, public_tender_board_dto.sail):
            raise PublicTenderException(
                "public tender board sail length doesn't match between 2 until 32 characters",
                HttpStatus.BAD_REQUEST
            )
        if not match(Regex.STRING_128.value, public_tender_board_dto.name):
            raise PublicTenderException(
                "public tender board length doesn't match between 1 until 128 characters",
                HttpStatus.BAD_REQUEST
            )
