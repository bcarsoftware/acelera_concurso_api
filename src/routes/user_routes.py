from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from src.controllers.user.controller_user import UserController
from src.controllers.user.controller_user_interface import UserControllerInterface
from src.core.exception_handler import exception_handler

user_rotes = APIRouter(prefix="/user")

user_controller: UserControllerInterface = UserController()


@exception_handler
@user_rotes.post("")
async def add_user(request: Request) -> JSONResponse:
    return await user_controller.add_user(request)


@exception_handler
@user_rotes.patch("/recovery")
async def recover_user(request: Request) -> JSONResponse:
    return await user_controller.recover_user(request)


@exception_handler
@user_rotes.patch("/{user_id}")
async def update_user(request: Request, user_id: str) -> JSONResponse:
    return await user_controller.update_user(request, user_id)


@exception_handler
@user_rotes.post("/login")
async def login_user(request: Request) -> JSONResponse:
    return await user_controller.login_user(request)


@exception_handler
@user_rotes.post("/logout")
async def logout_user(request: Request) -> JSONResponse:
    return await user_controller.logout_user(request)


@exception_handler
@user_rotes.delete("/delete/{user_id}")
async def delete_user(user_id: int) -> JSONResponse:
    return await user_controller.delete_user(user_id)
