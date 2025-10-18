from fastapi import APIRouter, Request
from starlette.responses import JSONResponse

from src.controllers.email_code.controller_email_code import EmailCodeController
from src.controllers.email_code.controller_email_code_interface import EmailCodeControllerInterface

email_code_routes = APIRouter(prefix="/email-code")

email_code_controller: EmailCodeControllerInterface = EmailCodeController()


@email_code_routes.post("")
async def send_checker_code_by_email(request: Request) -> JSONResponse:
    return await email_code_controller.send_checker_code_by_email(request)
