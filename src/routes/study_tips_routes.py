from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from src.controllers.study_tips.controlelr_study_tips import StudyTipsController
from src.controllers.study_tips.controller_study_tips_interface import StudyTipsControllerInterface
from src.core.authentication import authenticated
from src.core.exception_handler import exception_handler

study_tips_router = APIRouter(prefix="/study-tips")

controller_study_tips: StudyTipsControllerInterface = StudyTipsController()


@exception_handler
@study_tips_router.post("/")
@authenticated
async def create_study_tip(request: Request) -> JSONResponse:
    return await controller_study_tips.create_study_tip(request)


@exception_handler
@study_tips_router.patch("/{study_tip_id}/user/{user_id}")
@authenticated
async def update_study_tip(request: Request, study_tip_id: int, user_id: int) -> JSONResponse:
    return await controller_study_tips.update_study_tip(request, study_tip_id, user_id)


@exception_handler
@study_tips_router.get("/{user_id}")
@authenticated
async def find_study_tips_by_user_id(request: Request, user_id: int) -> JSONResponse:
    return await controller_study_tips.find_study_tips_by_user_id(request, user_id)


@exception_handler
@study_tips_router.delete("/{user_id}")
@authenticated
async def delete_one_or_more_study_tip(request: Request, user_id: int) -> JSONResponse:
    return await controller_study_tips.delete_one_or_more_study_tip(request, user_id)
