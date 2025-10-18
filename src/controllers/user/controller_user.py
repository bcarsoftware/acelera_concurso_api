from starlette.requests import Request
from starlette.responses import JSONResponse

from src.controllers.user.controller_user_interface import UserControllerInterface
from src.services.user.service_user import ServiceUser
from src.services.user.service_user_interface import ServiceUserInterface
from src.utils.managers.user_manager import UserManager


class UserController(UserControllerInterface):
    def __init__(self) -> None:
        self.user_service: ServiceUserInterface = ServiceUser()

    async def add_user(self, request: Request) -> JSONResponse:
        payload = await request.json()

        user_dto = await UserManager.convert_payload_to_user_dto(payload)

        return await self.user_service.add_user(user_dto)

    async def recover_user(self, request: Request) -> JSONResponse:
        payload = await request.json()

        recovery_dto = await UserManager.convert_payload_to_login_dto(payload)

        return await self.user_service.recover_user(recovery_dto)

    async def update_user(self, request: Request, user_id: str) -> JSONResponse:
        payload = await request.json()

        user_dto = await UserManager.convert_payload_to_user_dto(payload)

        return await self.user_service.update_user(user_dto, user_id)

    async def login_user(self, request: Request) -> JSONResponse:
        payload = await request.json()

        login_dto = await UserManager.convert_payload_to_login_dto(payload)

        return await self.user_service.login_user(login_dto)

    async def logout_user(self, request: Request) -> JSONResponse:
        # TODO: need to be done an implementation
        return await self.user_service.logout_user(request)

    async def delete_user(self, user_id: int) -> JSONResponse:
        return await self.user_service.delete_user(user_id)
