from fastapi import APIRouter, Request
from starlette.responses import JSONResponse

from src.controllers.pomodoro.controller_pomodoro import PomodoroController
from src.controllers.pomodoro.controller_pomodoro_interface import PomodoroControllerInterface
from src.core.authentication import authenticated
from src.core.exception_handler import exception_handler


pomodoro_route =  APIRouter(prefix="/pomodoro", tags=["Pomodoro"])
controller_pomodoro: PomodoroControllerInterface = PomodoroController()


@exception_handler
@pomodoro_route.post("")
@authenticated
async def create_pomodoro(request: Request) -> JSONResponse:
    return await controller_pomodoro.create_pomodoro(request)


@exception_handler
@pomodoro_route.patch("/{pomodoro_id}")
@authenticated
async def update_pomodoro(request: Request, pomodoro_id: int) -> JSONResponse:
    return await controller_pomodoro.update_pomodoro(request, pomodoro_id)


@exception_handler
@pomodoro_route.get("/{user_id}/user")
@authenticated
async def get_all_pomodoros_by_user_id(request: Request, user_id: int) -> JSONResponse:
    return await controller_pomodoro.get_all_pomodoros_by_user_id(request, user_id)


@exception_handler
@pomodoro_route.delete("/{pomodoro_id}/user/{user_id}")
@authenticated
async def delete_pomodoro(request: Request, user_id: int, pomodoro_id: int) -> JSONResponse:
    return await controller_pomodoro.delete_pomodoro(request, user_id, pomodoro_id)
