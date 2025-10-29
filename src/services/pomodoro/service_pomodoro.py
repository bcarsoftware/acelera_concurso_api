from typing import List

from src.models_dtos.pomodoro_dto import PomodoroDTO
from src.models_responses.pomodoro_response import PomodoroResponse
from src.repositories.pomodoro.repository_pomodoro import PomodoroRepository
from src.repositories.pomodoro.repository_pomodoro_interface import PomodoroRepositoryInterface
from src.services.pomodoro.service_pomodoro_interface import ServicePomodoroInterface
from src.utils.managers.pomodoro_manager import PomodoroManager


class ServicePomodoro(ServicePomodoroInterface):
    repository_pomodoro: PomodoroRepositoryInterface

    def __init__(self) -> None:
        self.repository_pomodoro = PomodoroRepository()

    async def create_pomodoro(self, pomodoro_dto: PomodoroDTO) -> PomodoroResponse:
        await PomodoroManager.make_validation(pomodoro_dto)

        return await self.repository_pomodoro.create_pomodoro(pomodoro_dto)

    async def update_pomodoro(self, pomodoro_dto: PomodoroDTO, pomodoro_id: int) -> PomodoroResponse:
        await PomodoroManager.make_validation(pomodoro_dto)

        return await self.repository_pomodoro.update_pomodoro(pomodoro_dto, pomodoro_id)

    async def get_all_pomodoros_by_user_id(self, user_id: int) -> List[PomodoroResponse]:
        return await self.repository_pomodoro.get_all_pomodoros_by_user_id(user_id)

    async def delete_pomodoro(self, user_id: int, pomodoro_id: int) -> PomodoroResponse:
        return await self.repository_pomodoro.delete_pomodoro(user_id, pomodoro_id)
