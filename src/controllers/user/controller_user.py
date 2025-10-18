from starlette.requests import Request
from starlette.responses import JSONResponse

from src.controllers.user.controller_user_interface import UserControllerInterface
from src.utils.managers.user_manager import UserManager


class UserController(UserControllerInterface):
    async def add_user(self, request: Request) -> JSONResponse:
        payload = await request.json()

        user_dto = await UserManager.convert_payload_to_user_dto(payload)

        await UserManager.make_validation(user_dto)

    async def recover_user(self, request: Request) -> JSONResponse:
        pass

    async def update_user(self, request: Request, user_id: str) -> JSONResponse:
        payload = await request.json()

        user_dto = await UserManager.convert_payload_to_user_dto(payload)

        await UserManager.make_validation(user_dto)

    async def login_user(self, request: Request) -> JSONResponse:
        payload = await request.json()

        login_dto = await UserManager.convert_payload_to_login_dto(payload)

    async def logout_user(self, request: Request) -> JSONResponse:
        pass

    async def delete_user(self, user_id: int) -> JSONResponse:
        pass
