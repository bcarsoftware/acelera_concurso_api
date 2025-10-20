from abc import ABC, abstractmethod
from typing import List

from src.models_dtos.public_tender_dto import PublicTenderDTO
from src.models_responses.public_tender_response import PublicTenderResponse


class ServicePublicTenderInterface(ABC):
    @abstractmethod
    async def public_tender_create(self, public_tender: PublicTenderDTO) -> PublicTenderResponse:
        pass

    @abstractmethod
    async def public_tender_patch(self, public_tender: PublicTenderDTO, public_tender_id: int) -> PublicTenderResponse:
        pass

    @abstractmethod
    async def public_tender_list(self, public_tender_id: int) -> List[PublicTenderResponse]:
        pass

    @abstractmethod
    async def public_tender_institute_list(self, institute: str, public_tender_id: int) -> List[PublicTenderResponse]:
        pass

    @abstractmethod
    async def public_tender_board_list(self, tender_board: str, public_tender_id: int) -> List[PublicTenderResponse]:
        pass

    @abstractmethod
    async def public_tender_delete(self, user_id: int) -> PublicTenderResponse:
        pass
