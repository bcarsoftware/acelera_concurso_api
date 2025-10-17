from typing import Any, Type

from pydantic import BaseModel, ValidationError

from src.exceptions.default_exception import DefaultException
from src.utils.strip_strings import strip_strings


async def payload_dto(payload: Any, type_dto: Type[BaseModel], exception_obj: DefaultException):
    data = await strip_strings(payload)

    try:
        return type_dto.model_validate(data)
    except ValidationError:
        raise exception_obj
