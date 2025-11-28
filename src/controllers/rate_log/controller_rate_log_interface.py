from abc import ABC, abstractmethod

from fastapi import Request
from fastapi.responses import JSONResponse


class RateLogControllerInterface(ABC):
    @abstractmethod
    async def find_rate_logs_entry(self, request: Request) -> JSONResponse:
        pass
