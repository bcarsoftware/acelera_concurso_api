from starlette.requests import Request
from starlette.responses import JSONResponse

from src.controllers.subject.controller_subject_interface import SubjectControllerInterface
from src.core.constraints import HttpStatus, ParamNames
from src.core.response_factory import response_factory
from src.services.subject.service_subject import ServiceSubject
from src.services.subject.service_subject_interface import ServiceSubjectInterface
from src.utils.header_param import get_header_param_by_name
from src.utils.managers.subject_manager import SubjectManager


class SubjectController(SubjectControllerInterface):
    def __init__(self) -> None:
        self.service_subject: ServiceSubjectInterface = ServiceSubject()

    async def create_subject(self, request: Request) -> JSONResponse:
        payload = await request.json()

        subject_dto = await SubjectManager.convert_payload_to_subject_dto(payload)

        response = await self.service_subject.create_subject(subject_dto)

        return await response_factory(
            data=response.model_dump(mode="json"),
            message="subject created successfully",
            status_code=HttpStatus.CREATED
        )

    async def update_subject(self, request: Request, subject_id: int) -> JSONResponse:
        payload = await request.json()

        subject_dto = await SubjectManager.convert_payload_to_subject_dto(payload)

        response = await self.service_subject.update_subject(subject_dto, subject_id)

        return await response_factory(
            data=response.model_dump(mode="json"),
            message="subject updated successfully",
            status_code=HttpStatus.OK
        )

    async def get_subjects(self, request: Request) -> JSONResponse:
        public_tender_id = await get_header_param_by_name(request, ParamNames.TENDER_ID)

        responses = await self.service_subject.get_subjects(public_tender_id)
        responses = [response.model_dump(mode="json") for response in responses]

        return await response_factory(
            data=responses,
            message="subject find successfully",
            status_code=HttpStatus.OK
        )

    async def get_subject_by_name(self, request: Request, name: str) -> JSONResponse:
        public_tender_id = await get_header_param_by_name(request, ParamNames.TENDER_ID)

        responses = await self.service_subject.get_subject_by_name(public_tender_id, name)
        responses = [response.model_dump(mode="json") for response in responses]

        return await response_factory(
            data=responses,
            message="subject find successfully",
            status_code=HttpStatus.OK
        )

    async def finish_subject(self, request: Request, subject_id: int) -> JSONResponse:
        response = await self.service_subject.finish_subject(subject_id)

        return await response_factory(
            data=response.model_dump(mode="json"),
            message="subject finished successfully",
            status_code=HttpStatus.OK
        )

    async def delete_subject(self, request: Request, subject_id: int) -> JSONResponse:
        response = await self.service_subject.delete_subject(subject_id)

        return await response_factory(
            data=response.model_dump(mode="json"),
            message="subject deleted successfully",
            status_code=HttpStatus.OK
        )
