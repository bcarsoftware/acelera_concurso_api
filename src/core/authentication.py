from functools import wraps
from typing import Callable, Any

from fastapi import Request

from src.core.constraints import HttpStatus
from src.core.token_factory import TokenFactory
from src.exceptions.jwt_exception import JWTException


def authenticated(function: Callable[..., Any], *args: Any):
    @wraps(function)
    async def wrapper(**kwargs: Any) -> Any:
        request: Request = kwargs["request"]

        headers = request.headers

        token = headers.get("Authorization")

        if token is None:
            raise JWTException("token authentication required", HttpStatus.NOT_AUTHORIZED)

        token = token.replace("Bearer", "").strip()

        try:
            await TokenFactory.verify_token(token)
        except JWTException as jtw_e:
            print(jtw_e)
            raise JWTException("user not authorized", HttpStatus.NOT_AUTHORIZED)

    return wrapper
