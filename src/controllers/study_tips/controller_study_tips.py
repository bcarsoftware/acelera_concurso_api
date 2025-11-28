from starlette.requests import Request
from starlette.responses import JSONResponse

from src.controllers.study_tips.controller_study_tips_interface import StudyTipsControllerInterface
from src.core.constraints import HttpStatus
from src.core.response_factory import response_factory
from src.services.study_tips.service_study_tips import ServiceStudyTips
from src.services.study_tips.service_study_tips_interface import ServiceStudyTipsInterface
from src.utils.managers.study_tips_manager import StudyTipsManager


class StudyTipsController(StudyTipsControllerInterface):
    def __init__(self) -> None:
        self.service_study_tips: ServiceStudyTipsInterface = ServiceStudyTips()

    async def create_study_tip(self, request: Request) -> JSONResponse:
        study_tip_json = await request.json()

        study_tip_dto = await StudyTipsManager.convert_payload_to_study_tips_dto(study_tip_json)

        response = await self.service_study_tips.create_study_tip(study_tip_dto)

        return await response_factory(
            data=response.model_dump(mode="json"),
            message="study_tip created successfully",
            status_code=HttpStatus.CREATED
        )

    async def update_study_tip(self, request: Request, study_tip_id: int, user_id: int) -> JSONResponse:
        study_tip_json = await request.json()

        study_tip_dto = await StudyTipsManager.convert_payload_to_study_tips_dto(study_tip_json)

        response = await self.service_study_tips.update_study_tip(study_tip_dto, study_tip_id, user_id)

        return await response_factory(
            data=response.model_dump(mode="json"),
            message="study_tip created successfully",
            status_code=HttpStatus.OK
        )

    async def find_study_tips_by_user_id(self, request: Request, user_id: int) -> JSONResponse:
        responses = await self.service_study_tips.find_study_tips_by_user_id(user_id)
        responses = [response.model_dump(mode="json") for response in responses]

        return await response_factory(
            data=responses,
            message="study_tip created successfully",
            status_code=HttpStatus.OK
        )

    async def delete_one_or_more_study_tip(self, request: Request, user_id: int) -> JSONResponse:
        study_tip_json = await request.json()

        list_ids_dto = await StudyTipsManager.convert_payload_to_list_id_dto(study_tip_json)

        response = await self.service_study_tips.delete_one_or_more_study_tip(list_ids_dto, user_id)

        return await response_factory(
            data={ "response": response, "message": "study_tip deleted successfully" },
            message="study_tip created successfully",
            status_code=HttpStatus.OK
        )
