from abc import ABC, abstractmethod
from typing import List

from src.models_dtos.list_id_dto import ListIDDTO
from src.models_dtos.study_tips_dto import StudyTipsDTO
from src.models_responses.study_tips_response import StudyTipsResponse


class ServiceStudyTipsInterface(ABC):
    @abstractmethod
    async def create_study_tip(self, study_tip_dto: StudyTipsDTO) -> StudyTipsResponse:
        pass

    @abstractmethod
    async def update_study_tip(self, study_tip_dto: StudyTipsDTO, study_tip_id: int, user_id: int) -> StudyTipsResponse:
        pass

    @abstractmethod
    async def find_study_tips_by_user_id(self, user_id: int) -> List[StudyTipsResponse]:
        pass

    @abstractmethod
    async def delete_one_or_more_study_tip(self, list_ids_dto: ListIDDTO, user_id: int) -> bool:
        pass
