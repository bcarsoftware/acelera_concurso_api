from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from src.core.exception_handler import exception_handler

user_rotes = APIRouter(prefix="/user")


@exception_handler
@user_rotes.post("")
async def add_user(request: Request) -> JSONResponse:
    pass


@exception_handler
@user_rotes.patch("/recovery")
async def recover_user(request: Request) -> JSONResponse:
    pass


@exception_handler
@user_rotes.patch("/{user_id}")
async def update_user(request: Request, user_id: str) -> JSONResponse:
    pass


@exception_handler
@user_rotes.post("/login")
async def login_user(request: Request) -> JSONResponse:
    pass


@exception_handler
@user_rotes.post("/logout")
async def logout_user(request: Request) -> JSONResponse:
    pass


@exception_handler
@user_rotes.delete("/delete/{user_id}")
async def delete_user(user_id: int) -> JSONResponse:
    pass
