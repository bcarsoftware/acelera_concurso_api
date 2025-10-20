from typing import List

from src.models_dtos.public_tender_dto import PublicTenderDTO
from src.models_responses.public_tender_response import PublicTenderResponse
from src.services.public_tender.service_public_tender_interface import ServicePublicTenderInterface
from src.utils.managers.public_tender_manager import PublicTenderManager


class ServicePublicTender(ServicePublicTenderInterface):
    async def public_tender_create(self, public_tender: PublicTenderDTO) -> PublicTenderResponse:
        await PublicTenderManager.make_validation(public_tender)
        pass

    async def public_tender_patch(self, public_tender: PublicTenderDTO, public_tender_id: int) -> PublicTenderResponse:
        await PublicTenderManager.make_validation(public_tender)
        pass

    async def public_tender_list(self, user_id: int) -> List[PublicTenderResponse]:
        pass

    async def public_tender_institute_list(self, institute: str, user_id: int) -> List[PublicTenderResponse]:
        pass

    async def public_tender_board_list(self, tender_board: str, user_id: int) -> List[PublicTenderResponse]:
        pass

    async def public_tender_delete(self, public_tender_id: int) -> PublicTenderResponse:
        pass
