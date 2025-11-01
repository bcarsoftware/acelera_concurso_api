from typing import List

from src.models_dtos.list_id_dto import ListIDDTO
from src.models_dtos.study_tips_dto import StudyTipsDTO
from src.models_responses.study_tips_response import StudyTipsResponse
from src.repositories.study_tips.repository_study_tips import StudyTipsRepository
from src.repositories.study_tips.repository_study_tips_interface import StudyTipsRepositoryInterface
from src.services.study_tips.service_study_tips_interface import ServiceStudyTipsInterface
from src.utils.managers.study_tips_manager import StudyTipsManager


class ServiceStudyTips(ServiceStudyTipsInterface):
    def __init__(self) -> None:
        self.repository_study_tips: StudyTipsRepositoryInterface = StudyTipsRepository()

    async def create_study_tip(self, study_tip_dto: StudyTipsDTO) -> StudyTipsResponse:
        await StudyTipsManager.make_validation(study_tip_dto)

        return await self.repository_study_tips.create_study_tip(study_tip_dto)

    async def update_study_tip(self, study_tip_dto: StudyTipsDTO, study_tip_id: int, user_id: int) -> StudyTipsResponse:
        await StudyTipsManager.make_validation(study_tip_dto)

        return await self.repository_study_tips.update_study_tip(study_tip_dto, study_tip_id, user_id)

    async def find_study_tips_by_user_id(self, user_id: int) -> List[StudyTipsResponse]:
        return await self.repository_study_tips.find_study_tips_by_user_id(user_id)

    async def delete_one_or_more_study_tip(self, list_ids_dto: ListIDDTO, user_id: int) -> bool:
        return await self.repository_study_tips.delete_one_or_more_study_tip(list_ids_dto, user_id)
