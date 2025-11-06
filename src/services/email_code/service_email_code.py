from src.core.constraints import Constraints, HttpStatus
from src.core.token_factory import TokenFactory
from src.enums.enum_token_time import EnumTokenTime
from src.exceptions.active_code_exception import ActiveCodeException
from src.exceptions.send_email_exception import SendEmailException
from src.models_dtos.active_code_dto import ActiveCodeDTO
from src.models_dtos.email_dto import EmailDTO
from src.services.email_code.service_email_code_interface import ServiceEmailCodeInterface
from src.utils.email_code_util import EmailCodeUtil
from src.utils.managers.active_code_manager import ActiveCodeManager
from src.utils.password_util import PasswordUtil


class ServiceEmailCode(ServiceEmailCodeInterface):
    async def send_checker_code_by_email(self, email_dto: EmailDTO) -> ActiveCodeDTO:
        verification_code = await EmailCodeUtil.send_email_verification_code(email_dto.email)

        expire_in = await self._get_expire_code_time_()

        token = await TokenFactory.create_token(
            ActiveCodeDTO(secure_code=verification_code),
            expire_in,
            EnumTokenTime.MINUTES
        )

        return ActiveCodeDTO(secure_code=verification_code, token=token)

    async def verify_encrypted_verification_code(self, active_code_dto: ActiveCodeDTO) -> ActiveCodeDTO:
        await ActiveCodeManager.make_validation(active_code_dto)

        if not active_code_dto.code:
            raise ActiveCodeException("missing code param to compare")

        await TokenFactory.verify_token(active_code_dto.token)

        response = await PasswordUtil.verify(active_code_dto.code, active_code_dto.secure_code)

        if not response:
            raise ActiveCodeException("invalid verification code")

        return active_code_dto

    @staticmethod
    async def _get_expire_code_time_() -> float:
        expire = Constraints.EXPIRE_CODE_TIME

        if expire is None:
            raise SendEmailException("expire time not set", HttpStatus.NOT_FOUND)
        if not expire.replace(".", "").isnumeric():
            raise SendEmailException("expire time not valid", HttpStatus.BAD_REQUEST)

        return float(expire)
