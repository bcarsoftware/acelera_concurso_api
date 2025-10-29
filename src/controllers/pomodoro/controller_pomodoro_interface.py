from abc import ABC, abstractmethod

from fastapi import Request
from fastapi.responses import JSONResponse


class PomodoroControllerInterface(ABC):
    @abstractmethod
    async def create_pomodoro(self, request: Request) -> JSONResponse:
        pass

    @abstractmethod
    async def update_pomodoro(self, request: Request, pomodoro_id: int) -> JSONResponse:
        pass

    @abstractmethod
    async def get_all_pomodoros_by_user_id(self, request: Request, user_id: int) -> JSONResponse:
        pass

    @abstractmethod
    async def delete_pomodoro(self, request: Request, user_id: int, pomodoro_id: int) -> JSONResponse:
        pass
