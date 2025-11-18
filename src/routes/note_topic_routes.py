from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from src.controllers.note_topic.controller_note_topic import NoteTopicController
from src.controllers.note_topic.controller_note_topic_interface import NoteTopicControllerInterface
from src.core.authentication import authenticated
from src.core.exception_handler import exception_handler

note_topic_route = APIRouter(prefix="/note-topic", tags=["Note Topic"])

controller_note_topic: NoteTopicControllerInterface = NoteTopicController()


@exception_handler
@note_topic_route.post("")
@authenticated
async def create_note_topic(request: Request) -> JSONResponse:
    return await controller_note_topic.create_note_topic(request)


@exception_handler
@note_topic_route.patch("/{note_topic_id}")
@authenticated
async def update_note_topic(request: Request, note_topic_id: int) -> JSONResponse:
    return await controller_note_topic.update_note_topic(request, note_topic_id)


@exception_handler
@note_topic_route.get("/{topic_id}/topic")
@authenticated
async def find_note_topic_by_topic_id(request: Request, topic_id: int) -> JSONResponse:
    return await controller_note_topic.find_note_topic_by_topic_id(request, topic_id)


@exception_handler
@note_topic_route.patch("/{note_topic_id}/finish")
@authenticated
async def finish_note_topic(request: Request, note_topic_id: int) -> JSONResponse:
    return await controller_note_topic.finish_note_topic(request, note_topic_id)


@exception_handler
@note_topic_route.delete("/{note_topic_id}")
@authenticated
async def delete_note_topic(request: Request, note_topic_id: int) -> JSONResponse:
    return await controller_note_topic.delete_note_topic(request, note_topic_id)
