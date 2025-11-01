from datetime import date
from re import match
from typing import Any, Dict

from src.core.constraints import HttpStatus
from src.exceptions.user_exception import UserException
from src.models_dtos.login_dto import LoginDTO
from src.models_dtos.user_dto import UserDTO
from src.utils.payload_dto import payload_dto
from src.utils.regex import Regex


class UserManager:
    @classmethod
    async def convert_payload_to_login_dto(cls, data_body: Dict[str, Any]) -> LoginDTO:
        user_exception = UserException(
            "invalid payload for user login",
            HttpStatus.UNPROCESSABLE_ENTITY
        )

        login_dto = await payload_dto(data_body, LoginDTO, user_exception)

        return LoginDTO(**login_dto)

    @classmethod
    async def convert_payload_to_user_dto(cls, data_body: Dict[str, Any]) -> UserDTO:
        user_exception = UserException(
            "invalid payload for user",
            HttpStatus.UNPROCESSABLE_ENTITY
        )

        user_dto = await payload_dto(data_body, UserDTO, user_exception)

        return UserDTO(**user_dto)

    @classmethod
    async def make_validation(cls, user_dto: UserDTO) -> None:
        await cls._check_user_deleted_(user_dto)
        await cls._checker_user_date_born_(user_dto)
        await cls._checker_user_strings_length_(user_dto)
        await cls._check_user_access_(user_dto)

    @classmethod
    async def make_email_verification(cls, login_dto: LoginDTO) -> None:
        if not match(Regex.STRING_281.value, login_dto.username):
            raise UserException("invalid email length", HttpStatus.BAD_REQUEST)
        if not match(Regex.EMAIL.value, login_dto.username):
            raise UserException("invalid email for user", HttpStatus.BAD_REQUEST)

    @classmethod
    async def make_password_verification(cls, user_dto: LoginDTO) -> None:
        if not match(Regex.STRING_4_32.value, user_dto.password):
            raise UserException("password doesn't match length between 4 until 32 characters",
                HttpStatus.BAD_REQUEST)
        if user_dto.password.count(" ") > 0:
            raise UserException("password can't contain spaces", HttpStatus.BAD_REQUEST)

    @classmethod
    async def _check_user_deleted_(cls, user_dto: UserDTO) -> None:
        if user_dto.deleted:
            raise UserException("you can't create an user that is deleted", HttpStatus.NOT_FOUND)

    @classmethod
    async def _checker_user_date_born_(cls, user_dto: UserDTO) -> None:
        if user_dto.born > date.today():
            raise UserException("you can't create an user that didn't born", HttpStatus.BAD_REQUEST)

    @classmethod
    async def _check_user_access_(cls, user_dto: UserDTO) -> None:
        if not match(Regex.USERNAME.value, user_dto.username):
            raise UserException("username does not match the pattern", HttpStatus.BAD_REQUEST)
        if not match(Regex.EMAIL.value, user_dto.email):
            raise UserException("email does not match the pattern", HttpStatus.BAD_REQUEST)
        if user_dto.password.count(" ") > 0:
            raise UserException("password can't contain spaces", HttpStatus.BAD_REQUEST)

    @classmethod
    async def _checker_user_strings_length_(cls, user_dto: UserDTO) -> None:
        if not match(Regex.STRING_64.value, user_dto.first_name):
            raise UserException(
                "first name doesn't match length between 1 until 64 characters",
                HttpStatus.BAD_REQUEST
            )
        if not match(Regex.STRING_255.value, user_dto.last_name):
            raise UserException(
                "last name doesn't match length between 1 until 255 characters",
                HttpStatus.BAD_REQUEST
            )
        if not match(Regex.STRING_128.value, user_dto.username):
            raise UserException(
                "username doesn't match length between 1 until 128 characters",
                HttpStatus.BAD_REQUEST
            )
        if not match(Regex.STRING_281.value, user_dto.email):
            raise UserException(
                "email doesn't match length between 1 until 281 characters",
                HttpStatus.BAD_REQUEST
            )
        if not match(Regex.STRING_4_32.value, user_dto.password):
            raise UserException(
                "password doesn't match length between 4 until 32 characters",
                HttpStatus.BAD_REQUEST
            )
