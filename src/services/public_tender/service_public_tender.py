from typing import List

from src.models_dtos.public_tender_dto import PublicTenderDTO
from src.models_responses.public_tender_response import PublicTenderResponse
from src.repositories.public_tender.repository_public_tender import PublicTenderRepository
from src.repositories.public_tender.repository_public_tender_interface import PublicTenderRepositoryInterface
from src.services.public_tender.service_public_tender_interface import ServicePublicTenderInterface
from src.utils.managers.public_tender_manager import PublicTenderManager


class ServicePublicTender(ServicePublicTenderInterface):
    public_tender_repository: PublicTenderRepositoryInterface

    def __init__(self) -> None:
        self.public_tender_repository = PublicTenderRepository()

    async def public_tender_create(self, public_tender: PublicTenderDTO) -> PublicTenderResponse:
        await PublicTenderManager.make_validation(public_tender)

        return await self.public_tender_repository.public_tender_create(public_tender)

    async def public_tender_patch(self, public_tender: PublicTenderDTO, public_tender_id: int) -> PublicTenderResponse:
        await PublicTenderManager.make_validation(public_tender)

        return await self.public_tender_patch(public_tender, public_tender_id)

    async def public_tender_list(self, user_id: int) -> List[PublicTenderResponse]:
        return await self.public_tender_repository.public_tender_list(user_id)

    async def public_tender_institute_list(self, institute: str, user_id: int) -> List[PublicTenderResponse]:
        await PublicTenderManager.verify_institute_empty(institute)

        return await self.public_tender_repository.public_tender_institute_list(institute, user_id)

    async def public_tender_board_list(self, tender_board: str, user_id: int) -> List[PublicTenderResponse]:
        await PublicTenderManager.verify_tender_board_empty(tender_board)

        return await self.public_tender_repository.public_tender_board_list(tender_board, user_id)

    async def public_tender_delete(self, public_tender_id: int) -> PublicTenderResponse:
        return await self.public_tender_repository.public_tender_delete(public_tender_id)
