from starlette.requests import Request
from starlette.responses import JSONResponse

from src.controllers.topic.controller_topic_interface import TopicControllerInterface
from src.core.constraints import HttpStatus, ParamNames
from src.core.response_factory import response_factory
from src.services.topic.service_topic import ServiceTopic
from src.services.topic.service_topic_interface import ServiceTopicInterface
from src.utils.header_param import get_header_param_by_name
from src.utils.managers.topic_manager import TopicManager


class TopicController(TopicControllerInterface):
    def __init__(self) -> None:
        self.service_topic: ServiceTopicInterface = ServiceTopic()

    async def create_topic(self, request: Request) -> JSONResponse:
        payload = await request.json()

        topic_dto = await TopicManager.convert_payload_to_topic_dto(payload)

        response = await self.service_topic.create_topic(topic_dto)

        return await response_factory(
            data=response.model_dump(mode="json"),
            message="topic created successfully",
            status_code=HttpStatus.CREATED
        )

    async def update_topic(self, request: Request, topic_id: int) -> JSONResponse:
        payload = await request.json()

        topic_dto = await TopicManager.convert_payload_to_topic_dto(payload)

        response = await self.service_topic.update_topic(topic_dto, topic_id)

        return await response_factory(
            data=response.model_dump(mode="json"),
            message="topic updated successfully",
            status_code=HttpStatus.OK
        )

    async def get_topics(self, request: Request) -> JSONResponse:
        subject_id = await get_header_param_by_name(request, ParamNames.SUBJECT_ID)

        responses = await self.service_topic.get_topics(int(subject_id))
        responses = [response.model_dump(mode="json") for response in responses]

        return await response_factory(
            data=responses,
            message="topic find successfully",
            status_code=HttpStatus.OK
        )

    async def get_topic_by_name(self, request: Request, name: str) -> JSONResponse:
        subject_id = await get_header_param_by_name(request, ParamNames.SUBJECT_ID)

        responses = await self.service_topic.get_topic_by_name(int(subject_id), name)
        responses = [response.model_dump(mode="json") for response in responses]

        return await response_factory(
            data=responses,
            message="topic find successfully",
            status_code=HttpStatus.OK
        )

    async def get_topic_by_status(self, request: Request, status: str) -> JSONResponse:
        subject_id = await get_header_param_by_name(request, ParamNames.SUBJECT_ID)

        responses = await self.service_topic.get_topic_by_status(int(subject_id), status)
        responses = [response.model_dump(mode="json") for response in responses]

        return await response_factory(
            data=responses,
            message="topic find successfully",
            status_code=HttpStatus.OK
        )

    async def finish_topic(self, request: Request, topic_id: int) -> JSONResponse:
        response = await self.service_topic.finish_topic(topic_id)

        return await response_factory(
            data=response.model_dump(mode="json"),
            message="topic finished successfully",
            status_code=HttpStatus.OK
        )

    async def delete_topic(self, request: Request, topic_id: int) -> JSONResponse:
        response = await self.service_topic.delete_topic(topic_id)

        return await response_factory(
            data=response.model_dump(mode="json"),
            message="topic deleted successfully",
            status_code=HttpStatus.OK
        )
