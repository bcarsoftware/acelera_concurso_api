from abc import ABC, abstractmethod
from typing import List

from src.models_dtos.pomodoro_dto import PomodoroDTO
from src.models_responses.pomodoro_response import PomodoroResponse


class ServicePomodoroInterface(ABC):
    @abstractmethod
    async def create_pomodoro(self, pomodoro_dto: PomodoroDTO) -> PomodoroResponse:
        pass

    @abstractmethod
    async def update_pomodoro(self, pomodoro_dto: PomodoroDTO, pomodoro_id: int) -> PomodoroResponse:
        pass

    @abstractmethod
    async def get_all_pomodoros_by_user_id(self, user_id: int) -> List[PomodoroResponse]:
        pass

    @abstractmethod
    async def delete_pomodoro(self, user_id: int, pomodoro_id: int) -> PomodoroResponse:
        pass
