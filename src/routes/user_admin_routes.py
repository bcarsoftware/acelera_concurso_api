from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from src.controllers.user_admin.controller_user_admin import UserAdminController
from src.controllers.user_admin.controller_user_admin_interface import UserAdminControllerInterface
from src.core.authentication import admin_authenticated
from src.core.exception_handler import exception_handler


user_admin_route = APIRouter(prefix="/user-admin")

controller_user_admin: UserAdminControllerInterface = UserAdminController()


@user_admin_route.post("")
@exception_handler
async def create_user_admin(request: Request) -> JSONResponse:
    return await controller_user_admin.create_user_admin(request)


@user_admin_route.post("/login")
@exception_handler
async def login_user_admin(request: Request) -> JSONResponse:
    return await controller_user_admin.login_user_admin(request)


@admin_authenticated
@user_admin_route.patch("/{user_admin_id}")
@exception_handler
async def update_user_admin(request: Request, user_admin_id: int) -> JSONResponse:
    return await controller_user_admin.update_user_admin(request, user_admin_id)
