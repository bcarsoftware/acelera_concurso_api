from datetime import datetime, timedelta, timezone

from typing import Any

from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError

from src.core.constraints import Constraints, HttpStatus
from src.enums.enum_token_time import EnumTokenTime
from src.exceptions.jwt_exception import JWTException


class TokenFactory:
    @classmethod
    async def create_token(cls, data: Any, time: float, time_select: EnumTokenTime) -> str:
        if time <= 0:
            raise JWTException("time must be positive integer", HttpStatus.BAD_REQUEST)

        secret_key = await cls._get_secret_key_()
        algorithm = await cls._get_algorithm_()

        time_delta = await cls._get_time_delta_(time, time_select)

        payload = {
            "data": data,
            "exp": datetime.now(timezone.utc) + time_delta,
        }

        encoded_jwt = encode(payload, secret_key, algorithm=algorithm)

        return encoded_jwt

    @classmethod
    async def get_data_from_token(cls, token: str) -> Any:
        await cls.verify_token(token)

        secret_key = await cls._get_secret_key_()
        algorithm = await cls._get_algorithm_()

        response = decode(token, secret_key, algorithms=[algorithm])

        return response["data"]

    @classmethod
    async def verify_token(cls, token: str) -> None:
        secret_key = await cls._get_secret_key_()
        algorithm = await cls._get_algorithm_()

        try:
            decode(token, secret_key, algorithms=[algorithm])
        except ExpiredSignatureError:
            raise JWTException("this token has expired", HttpStatus.BAD_REQUEST)
        except InvalidTokenError:
            raise JWTException("this token is invalid", HttpStatus.BAD_REQUEST)

    @classmethod
    async def _get_algorithm_(cls) -> str:
        algorithm = Constraints.ALGORITHM

        if algorithm is None:
            raise JWTException("algorithm is not set in environment", HttpStatus.NOT_FOUND)

        return algorithm

    @classmethod
    async def _get_secret_key_(cls) -> str:
        secret_key = Constraints.SECRET_KEY

        if not secret_key:
            raise JWTException("secret key must be set in environment", HttpStatus.NOT_FOUND)

        return secret_key

    @staticmethod
    async def _get_time_delta_(time: float, enum_time: EnumTokenTime) -> timedelta:
        return {
            EnumTokenTime.DAYS: timedelta(days=time),
            EnumTokenTime.SECONDS: timedelta(seconds=time),
            EnumTokenTime.MICROSECONDS: timedelta(microseconds=time),
            EnumTokenTime.MILLISECONDS: timedelta(milliseconds=time),
            EnumTokenTime.MINUTES: timedelta(minutes=time),
            EnumTokenTime.HOURS: timedelta(hours=time),
            EnumTokenTime.WEEKS: timedelta(weeks=time),
        }.get(enum_time)
