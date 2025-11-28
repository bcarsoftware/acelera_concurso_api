from abc import ABC, abstractmethod

from fastapi import Request
from fastapi.responses import JSONResponse


class RateLogControllerInterface(ABC):
    @abstractmethod
    async def create_rate_log_entry(self, request: Request) -> JSONResponse:
        pass

    @abstractmethod
    async def find_rate_logs_entry(self, request: Request) -> JSONResponse:
        pass
