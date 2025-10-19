from typing import Dict

from src.core.constraints import Constraints
from src.core.token_factory import TokenFactory
from src.models_dtos.email_dto import EmailDTO
from src.services.email_code.service_email_code_interface import ServiceEmailCodeInterface
from src.utils.email_code_util import EmailCodeUtil


class ServiceEmailCode(ServiceEmailCodeInterface):
    async def send_checker_code_by_email(self, email_dto: EmailDTO) -> Dict[str, str]:
        varification_code = await EmailCodeUtil.send_email_verification_code(email_dto.email)

        token = await TokenFactory.create_token(varification_code, Constraints.EXPIRE_CODE_TIME)

        return { "code": varification_code, "token": token }
