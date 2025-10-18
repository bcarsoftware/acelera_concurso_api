from abc import ABC, abstractmethod

from fastapi import Request
from fastapi.responses import JSONResponse


class EmailCodeControllerInterface(ABC):
    @abstractmethod
    async def send_checker_code_by_email(self, request: Request) -> JSONResponse:
        pass
