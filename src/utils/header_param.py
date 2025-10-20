from typing import Any

from fastapi import Request

from src.exceptions.header_exception import HeaderException


async def get_header_param_by_name(request: Request, param_name: str) -> Any | None:
    param = request.headers.get(param_name) or None

    if param is None:
        raise HeaderException(f"param '{param_name}' not found at header")

    return param
