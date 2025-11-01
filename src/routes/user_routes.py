from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from src.controllers.user.controller_user import UserController
from src.controllers.user.controller_user_interface import UserControllerInterface
from src.core.authentication import authenticated
from src.core.exception_handler import exception_handler

user_rote = APIRouter(prefix="/user")

user_controller: UserControllerInterface = UserController()


@exception_handler
@user_rote.post("/")
async def add_user(request: Request) -> JSONResponse:
    return await user_controller.add_user(request)


@exception_handler
@user_rote.patch("/recovery")
async def recover_user(request: Request) -> JSONResponse:
    return await user_controller.recover_user(request)


@exception_handler
@user_rote.patch("/{user_id}")
@authenticated
async def update_user(request: Request, user_id: str) -> JSONResponse:
    return await user_controller.update_user(request, user_id)


@exception_handler
@user_rote.post("/login")
async def login_user(request: Request) -> JSONResponse:
    return await user_controller.login_user(request)


@exception_handler
@user_rote.delete("/{user_id}")
@authenticated
async def delete_user(request: Request, user_id: int) -> JSONResponse:
    return await user_controller.delete_user(request, user_id)
