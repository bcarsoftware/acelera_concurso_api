from starlette.requests import Request
from starlette.responses import JSONResponse

from src.controllers.pomodoro.controller_pomodoro_interface import PomodoroControllerInterface
from src.core.constraints import HttpStatus
from src.core.response_factory import response_factory
from src.services.pomodoro.service_pomodoro import ServicePomodoro
from src.services.pomodoro.service_pomodoro_interface import ServicePomodoroInterface
from src.utils.managers.pomodoro_manager import PomodoroManager


class PomodoroController(PomodoroControllerInterface):
    service_pomodoro: ServicePomodoroInterface

    def __init__(self) -> None:
        self.service_pomodoro = ServicePomodoro()

    async def create_pomodoro(self, request: Request) -> JSONResponse:
        payload_dto = await request.json()

        pomodoro_dto = await PomodoroManager.convert_payload_to_pomodoro_dto(payload_dto)

        response = await self.service_pomodoro.create_pomodoro(pomodoro_dto)

        return await response_factory(
            data=response,
            message="pomodoro created successfully",
            status_code=HttpStatus.CREATED
        )

    async def update_pomodoro(self, request: Request, pomodoro_id: int) -> JSONResponse:
        payload_dto = await request.json()

        pomodoro_dto = await PomodoroManager.convert_payload_to_pomodoro_dto(payload_dto)

        response = await self.service_pomodoro.update_pomodoro(pomodoro_dto, pomodoro_id)

        return await response_factory(
            data=response,
            message="pomodoro updated successfully",
            status_code=HttpStatus.OK
        )

    async def get_all_pomodoros_by_user_id(self, request: Request, user_id: int) -> JSONResponse:
        responses = await self.service_pomodoro.get_all_pomodoros_by_user_id(user_id)

        return await response_factory(
            data=responses,
            message="pomodoros found successfully",
            status_code=HttpStatus.OK
        )

    async def delete_pomodoro(self, request: Request, user_id: int, pomodoro_id: int) -> JSONResponse:
        response = await self.service_pomodoro.delete_pomodoro(user_id, pomodoro_id)

        return await response_factory(
            data=response,
            message="pomodoro deleted successfully",
            status_code=HttpStatus.OK
        )
