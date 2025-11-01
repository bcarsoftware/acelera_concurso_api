from abc import ABC, abstractmethod

from fastapi import Request
from fastapi.responses import JSONResponse


class UserControllerInterface(ABC):
    @abstractmethod
    async def add_user(self, request: Request) -> JSONResponse:
        pass

    @abstractmethod
    async def recover_user(self, request: Request) -> JSONResponse:
        pass

    @abstractmethod
    async def update_user(self, request: Request, user_id: str) -> JSONResponse:
        pass

    @abstractmethod
    async def login_user(self, request: Request) -> JSONResponse:
        pass

    @abstractmethod
    async def delete_user(self, request: Request, user_id: int) -> JSONResponse:
        pass
