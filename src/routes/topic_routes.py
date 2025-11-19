from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from src.controllers.topic.controller_topic import TopicController
from src.controllers.topic.controller_topic_interface import TopicControllerInterface
from src.core.authentication import authenticated
from src.core.exception_handler import exception_handler

topic_route = APIRouter(prefix="/topic", tags=["Topic"])

controller_topic: TopicControllerInterface = TopicController()


@exception_handler
@topic_route.post("")
@authenticated
async def create_topic(request: Request) -> JSONResponse:
    return await controller_topic.create_topic(request)


@exception_handler
@topic_route.patch("/{topic_id}")
@authenticated
async def update_topic(request: Request, topic_id: int) -> JSONResponse:
    return await controller_topic.update_topic(request, topic_id)


@exception_handler
@topic_route.get("")
@authenticated
async def get_topics(request: Request) -> JSONResponse:
    return await controller_topic.get_topics(request)


@exception_handler
@topic_route.patch("/{topic_id}/finish")
@authenticated
async def finish_topic(request: Request, topic_id: int) -> JSONResponse:
    return await controller_topic.finish_topic(request, topic_id)


@exception_handler
@topic_route.delete("/{topic_id}")
@authenticated
async def delete_topic(request: Request, topic_id: int) -> JSONResponse:
    return await controller_topic.delete_topic(request, topic_id)
