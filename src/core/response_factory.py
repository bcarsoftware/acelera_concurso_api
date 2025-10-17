from typing import Any, Optional, Dict

from fastapi import status
from fastapi.responses import JSONResponse


async def response_factory(
    data: Optional[Any] = None,
    message: str = "Successful Operation!",
    status_code: int = status.HTTP_200_OK,
    headers: dict = None,
    status_type: str = "success",
    meta: Optional[Dict[str, Any]] = None
) -> JSONResponse:
    headers = headers or {
        "Content-Type": "application/json"
    }

    content = {
        "status": status_type,
        "message": message,
        "data": data if data is not None else {},
        "meta": meta if meta is not None else {}
    }

    return JSONResponse(content=content, status_code=status_code, headers=headers)
