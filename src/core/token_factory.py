from datetime import datetime, timedelta, timezone

from typing import Any

from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError

from src.core.constraints import Constraints
from src.exceptions.jwt_exception import JWTException


class TokenFactory:
    @classmethod
    async def create_token(cls, data: Any, time: int = 10) -> str:
        if time <= 0:
            raise JWTException("time must be positive integer")

        secret_key = await cls._get_secret_key_()
        algorithm = await cls._get_algorithm_()

        payload = {
            "data": data,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=time),
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
            raise JWTException("this token has expired")
        except InvalidTokenError:
            raise JWTException("this token is invalid")

    @classmethod
    async def _get_algorithm_(cls) -> str:
        algorithm = Constraints.ALGORITHM

        if algorithm is None:
            raise JWTException("algorithm is not set in environment")

        return algorithm

    @classmethod
    async def _get_secret_key_(cls) -> str:
        secret_key = Constraints.SECRET_KEY

        if not secret_key:
            raise JWTException("secret key must be set in environment")

        return secret_key
