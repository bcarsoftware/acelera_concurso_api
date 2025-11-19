from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from src.controllers.user.controller_user import UserController
from src.controllers.user.controller_user_interface import UserControllerInterface
from src.core.authentication import authenticated
from src.core.exception_handler import exception_handler

user_rote = APIRouter(prefix="/user", tags=["User"])

user_controller: UserControllerInterface = UserController()


@exception_handler
@user_rote.post("/")
async def add_user(request: Request) -> JSONResponse:
    return await user_controller.add_user(request)


@exception_handler
@user_rote.get("/{user_id}")
@authenticated
async def get_user_by_user_id(request: Request, user_id: int) -> JSONResponse:
    return await user_controller.get_user_by_user_id(request, user_id)


@exception_handler
@user_rote.patch("/recovery")
async def recover_user(request: Request) -> JSONResponse:
    return await user_controller.recover_user(request)


@exception_handler
@user_rote.patch("/{user_id}")
@authenticated
async def update_user(request: Request, user_id: int) -> JSONResponse:
    return await user_controller.update_user(request, user_id)


@exception_handler
@user_rote.post("/login")
async def login_user(request: Request) -> JSONResponse:
    return await user_controller.login_user(request)


@exception_handler
@user_rote.patch("/{user_id}/password")
@authenticated
async def update_user_password(request: Request, user_id: int) -> JSONResponse:
    return await user_controller.update_user_password(request, user_id)


@exception_handler
@user_rote.delete("/{user_id}")
@authenticated
async def delete_user(request: Request, user_id: int) -> JSONResponse:
    return await user_controller.delete_user(request, user_id)
