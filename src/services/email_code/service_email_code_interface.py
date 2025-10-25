from abc import ABC, abstractmethod

from src.models_dtos.active_code_dto import ActiveCodeDTO
from src.models_dtos.email_dto import EmailDTO


class ServiceEmailCodeInterface(ABC):
    @abstractmethod
    async def send_checker_code_by_email(self, email_dto: EmailDTO) -> ActiveCodeDTO:
        pass

    @abstractmethod
    async def verify_encrypted_verification_code(self, active_code_dto: ActiveCodeDTO) -> ActiveCodeDTO:
        pass
