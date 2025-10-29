from abc import ABC, abstractmethod
from typing import List

from sqlalchemy.ext.asyncio import AsyncEngine

from src.db.core.db_base import get_engine
from src.models_dtos.pomodoro_dto import PomodoroDTO
from src.models_responses.pomodoro_response import PomodoroResponse


class PomodoroRepositoryInterface(ABC):
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

    @property
    def _engine_(self) -> AsyncEngine:
        eng = get_engine()
        return next(eng)
