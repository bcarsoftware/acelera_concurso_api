from typing import Any, Dict

from src.core.constraints import HttpStatus
from src.exceptions.user_admin_exception import UserAdminException
from src.models_dtos.user_admin_dto import UserAdminDTO
from src.utils.payload_dto import payload_dto
from src.utils.regex import Regex


class UserAdminManager:
    @classmethod
    async def convert_payload_to_user_admin_dto(cls, data_body: Dict[str, Any]) -> UserAdminDTO:
        user_admin_exception = UserAdminException(
            "invalid payload for user admin",
            HttpStatus.UNPROCESSABLE_ENTITY
        )

        user_admin_dto = await payload_dto(data_body, UserAdminDTO, user_admin_exception)

        return UserAdminDTO(**user_admin_dto.model_dump())

    @classmethod
    async def make_validation(cls, user_admin_dto: UserAdminDTO) -> None:
        await cls._check_strings_length_(user_admin_dto)
        await cls._check_user_admin_access_(user_admin_dto)

    @classmethod
    async def _check_user_admin_access_(cls, user_admin_dto: UserAdminDTO) -> None:
        if not Regex.USERNAME.value.match(user_admin_dto.username):
            raise UserAdminException("admin username does not match the pattern", HttpStatus.BAD_REQUEST)
        if user_admin_dto.password.count(" ") > 0:
            raise UserAdminException("admin password contains spaces", HttpStatus.BAD_REQUEST)

    @classmethod
    async def _check_strings_length_(cls, user_admin_dto: UserAdminDTO) -> None:
        if not Regex.STRING_255.value.match(user_admin_dto.full_name):
            raise UserAdminException(
                "admin full name doesn't match length between 1 until 255 characters",
                HttpStatus.BAD_REQUEST
            )
        if not Regex.STRING_128.value.match(user_admin_dto.username):
            raise UserAdminException(
                "admin username doesn't match length between 1 until 128 characters",
                HttpStatus.BAD_REQUEST
            )
        if not Regex.STRING_4_32.value.match(user_admin_dto.password):
            raise UserAdminException(
                "admin password doesn't match length between 4 until 32 characters",
                HttpStatus.BAD_REQUEST
            )
