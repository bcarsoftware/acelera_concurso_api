from abc import ABC, abstractmethod

from fastapi import Request
from fastapi.responses import JSONResponse


class StudyTipsControllerInterface(ABC):
    @abstractmethod
    async def create_study_tip(self, request: Request) -> JSONResponse:
        pass

    @abstractmethod
    async def update_study_tip(self, request: Request, study_tip_id: int, user_id: int) -> JSONResponse:
        pass

    @abstractmethod
    async def find_study_tips_by_user_id(self, request: Request, user_id: int) -> JSONResponse:
        pass

    @abstractmethod
    async def delete_one_or_more_study_tip(self, request: Request, user_id: int) -> JSONResponse:
        pass
