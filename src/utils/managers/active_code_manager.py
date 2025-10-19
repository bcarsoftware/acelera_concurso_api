from typing import Dict

from src.exceptions.active_code_exception import ActiveCodeException
from src.models_dtos.active_code_dto import ActiveCodeDTO
from src.utils.payload_dto import payload_dto


class ActiveCodeManager:
    @classmethod
    async def convert_payload_to_active_code_dto(cls, payload: Dict[str, str]) -> ActiveCodeDTO:
        active_code_exception = ActiveCodeException("payload doesn't match required data", 422)

        active_code_dto = await payload_dto(payload, ActiveCodeDTO, active_code_exception)

        return ActiveCodeDTO(**active_code_dto)

    @classmethod
    async def verify_validation(cls, active_code_dto: ActiveCodeDTO) -> None:
        if not active_code_dto.code or not active_code_dto.token:
            raise ActiveCodeException("code or token is empty or null")
