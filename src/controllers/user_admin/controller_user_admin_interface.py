from abc import ABC, abstractmethod

from fastapi import Request
from fastapi.responses import JSONResponse


class UserAdminControllerInterface(ABC):
    @abstractmethod
    async def create_user_admin(self, request: Request) -> JSONResponse:
        pass

    @abstractmethod
    async def login_user_admin(self, request: Request) -> JSONResponse:
        pass

    @abstractmethod
    async def update_user_admin(self, request: Request, user_admin_id: int) -> JSONResponse:
        pass
