from starlette.requests import Request
from starlette.responses import JSONResponse

from src.controllers.user.controller_user_interface import UserControllerInterface
from src.core.constraints import HttpStatus, Constraints
from src.core.response_factory import response_factory
from src.core.token_factory import TokenFactory
from src.enums.enum_token_time import EnumTokenTime
from src.services.user.service_user import ServiceUser
from src.services.user.service_user_interface import ServiceUserInterface
from src.utils.managers.user_manager import UserManager


class UserController(UserControllerInterface):
    def __init__(self) -> None:
        self.user_service: ServiceUserInterface = ServiceUser()

    async def add_user(self, request: Request) -> JSONResponse:
        payload = await request.json()

        user_dto = await UserManager.convert_payload_to_user_dto(payload)

        response = await self.user_service.add_user(user_dto)

        return await response_factory(
            data=response,
            message="user created successfully",
            status_code=HttpStatus.CREATED,
        )

    async def recover_user(self, request: Request) -> JSONResponse:
        payload = await request.json()

        recovery_dto = await UserManager.convert_payload_to_login_dto(payload)

        response = await self.user_service.recover_user(recovery_dto)

        return await response_factory(
            data=response,
            message="user created successfully",
            status_code=HttpStatus.CREATED,
        )

    async def update_user(self, request: Request, user_id: str) -> JSONResponse:
        payload = await request.json()

        user_dto = await UserManager.convert_payload_to_user_dto(payload)

        response = await self.user_service.update_user(user_dto, user_id)

        return await response_factory(
            data=response,
            message="user created successfully",
            status_code=HttpStatus.CREATED,
        )

    async def login_user(self, request: Request) -> JSONResponse:
        payload = await request.json()

        login_dto = await UserManager.convert_payload_to_login_dto(payload)

        response = await self.user_service.login_user(login_dto)

        token = await TokenFactory.create_token(response, Constraints.EXPIRE_TOKEN_SESSION, EnumTokenTime.DAYS)

        user_with_token = {
            "user": { **response.model_dump() },
            "token": token,
        }

        return await response_factory(
            data=user_with_token,
            message="user created successfully",
            status_code=HttpStatus.CREATED,
        )

    async def logout_user(self, request: Request) -> JSONResponse:
        # TODO: need to be done an implementation
        return await self.user_service.logout_user(request)

    async def delete_user(self, user_id: int) -> JSONResponse:
        response = await self.user_service.delete_user(user_id)

        return await response_factory(
            data=response,
            message="user deleted successfully",
            status_code=HttpStatus.CREATED,
        )
