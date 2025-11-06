from fastapi import APIRouter, Request
from starlette.responses import JSONResponse

from src.controllers.email_code.controller_email_code import EmailCodeController
from src.controllers.email_code.controller_email_code_interface import EmailCodeControllerInterface
from src.core.exception_handler import exception_handler

email_code_route = APIRouter(prefix="/email-code", tags=["Email Code"])

email_code_controller: EmailCodeControllerInterface = EmailCodeController()


@exception_handler
@email_code_route.post("")
async def send_checker_code_by_email(request: Request) -> JSONResponse:
    return await email_code_controller.send_checker_code_by_email(request)


@exception_handler
@email_code_route.post("/verify")
async def send_verification_code_by_email(request: Request) -> JSONResponse:
    return await email_code_controller.verify_encrypted_verification_code(request)
