from starlette.requests import Request
from starlette.responses import JSONResponse

from src.controllers.topic.controller_topic_interface import TopicControllerInterface
from src.core.constraints import HttpStatus, ParamNames
from src.core.response_factory import response_factory
from src.utils.header_param import get_header_param_by_name
from src.utils.managers.topic_manager import TopicManager


class TopicController(TopicControllerInterface):
    async def create_topic(self, request: Request) -> JSONResponse:
        payload = await request.json()

        topic_dto = await TopicManager.convert_payload_to_topic_dto(payload)

        return await response_factory(
            data={},
            message="topic created successfully",
            status_code=HttpStatus.CREATED
        )

    async def update_topic(self, request: Request, topic_id: int) -> JSONResponse:
        payload = await request.json()

        topic_dto = await TopicManager.convert_payload_to_topic_dto(payload)

        return await response_factory(
            data={},
            message="topic updated successfully",
            status_code=HttpStatus.OK
        )

    async def get_topics(self, request: Request) -> JSONResponse:
        subject_id = await get_header_param_by_name(request, ParamNames.SUBJECT_ID)

        return await response_factory(
            data=[],
            message="topic find successfully",
            status_code=HttpStatus.OK
        )

    async def get_topic_by_name(self, request: Request, name: str) -> JSONResponse:
        subject_id = await get_header_param_by_name(request, ParamNames.SUBJECT_ID)

        return await response_factory(
            data=[],
            message="topic find successfully",
            status_code=HttpStatus.OK
        )

    async def get_topic_by_status(self, request: Request, status: str) -> JSONResponse:
        subject_id = await get_header_param_by_name(request, ParamNames.SUBJECT_ID)

        return await response_factory(
            data=[],
            message="topic find successfully",
            status_code=HttpStatus.OK
        )

    async def delete_topic(self, request: Request, topic_id: int) -> JSONResponse:
        return await response_factory(
            data={},
            message="topic deleted successfully",
            status_code=HttpStatus.OK
        )