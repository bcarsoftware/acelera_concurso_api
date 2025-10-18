from abc import ABC, abstractmethod
from typing import Any

from src.models_dtos.email_dto import EmailDTO


class ServiceEmailCodeInterface(ABC):
    @abstractmethod
    async def send_checker_code_by_email(self, email_dto: EmailDTO) -> Any:
        pass
