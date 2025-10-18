from fastapi import Request
from fastapi.responses import JSONResponse

from src.controllers.email_code.controller_email_code_interface import EmailCodeControllerInterface
from src.core.response_factory import response_factory
from src.services.email_code.service_email_code import ServiceEmailCode
from src.services.email_code.service_email_code_interface import ServiceEmailCodeInterface
from src.utils.managers.email_code_manager import EmailCodeManager


class EmailCodeController(EmailCodeControllerInterface):
    def __init__(self):
        self.service_email_code: ServiceEmailCodeInterface = ServiceEmailCode()

    async def send_checker_code_by_email(self, request: Request) -> JSONResponse:
        payload = await request.json()

        email_dto = await EmailCodeManager.convert_payload_to_topic_dto(payload)
        
        response = await self.service_email_code.send_checker_code_by_email(email_dto)

        return await response_factory(response, "code sent with success")
