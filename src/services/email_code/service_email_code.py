from typing import Dict

from src.models_dtos.email_dto import EmailDTO
from src.services.email_code.service_email_code_interface import ServiceEmailCodeInterface
from src.utils.active_email_util import ActiveEmailUtil


class ServiceEmailCode(ServiceEmailCodeInterface):
    async def send_checker_code_by_email(self, email_dto: EmailDTO) -> Dict[str, str]:
        varification_code = await ActiveEmailUtil.send_email_verification_code(email_dto.email)

        return { "code": varification_code }
