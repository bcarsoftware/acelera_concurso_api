from starlette.requests import Request
from starlette.responses import JSONResponse

from src.controllers.user.controller_user_interface import UserControllerInterface


class UserController(UserControllerInterface):
    async def add_user(self, request: Request) -> JSONResponse:
        pass

    async def recover_user(self, request: Request) -> JSONResponse:
        pass

    async def update_user(self, request: Request, user_id: str) -> JSONResponse:
        pass

    async def login_user(self, request: Request) -> JSONResponse:
        pass

    async def logout_user(self, request: Request) -> JSONResponse:
        pass

    async def delete_user(self, user_id: int) -> JSONResponse:
        pass
