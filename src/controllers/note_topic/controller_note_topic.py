from fastapi import Request
from fastapi.responses import JSONResponse

from src.controllers.note_topic.controller_note_topic_interface import NoteTopicControllerInterface
from src.core.constraints import HttpStatus
from src.core.response_factory import response_factory
from src.services.note_topic.service_note_topic import ServiceNoteTopic
from src.services.note_topic.service_note_topic_interface import ServiceNoteTopicInterface
from src.utils.managers.note_topic_manager import NoteTopicManager


class NoteTopicController(NoteTopicControllerInterface):
    service_note_topic: ServiceNoteTopicInterface

    def __init__(self) -> None:
        self.service_note_topic = ServiceNoteTopic()

    async def create_note_topic(self, request: Request) -> JSONResponse:
        payload = await request.json()

        note_topic_dto = await NoteTopicManager.convert_payload_to_note_topic_dto(payload)

        note_topic = await self.service_note_topic.create_note_topic(note_topic_dto)

        return await response_factory(
            data=note_topic,
            message="note topic created successfully",
            status_code=HttpStatus.CREATED
        )

    async def update_note_topic(self, request: Request, note_topic_id: int) -> JSONResponse:
        payload = await request.json()

        note_topic_dto = await NoteTopicManager.convert_payload_to_note_topic_dto(payload)

        note_topic = await self.service_note_topic.update_note_topic(note_topic_dto, note_topic_id)

        return await response_factory(
            data=note_topic,
            message="note topic updated successfully",
            status_code=HttpStatus.OK
        )

    async def find_note_topic_by_topic_id(self, request: Request, topic_id: int) -> JSONResponse:
        note_topics = await self.service_note_topic.find_note_topic_by_topic_id(topic_id)

        return await response_factory(
            data=note_topics,
            message="note topic found successfully",
            status_code=HttpStatus.OK
        )

    async def finish_note_topic(self, request: Request, note_topic_id: int) -> JSONResponse:
        payload = await request.json()

        note_topic_dto = await NoteTopicManager.convert_payload_to_note_topic_dto(payload)

        note_topic = await self.service_note_topic.update_note_topic(note_topic_dto, note_topic_id)

        return await response_factory(
            data=note_topic,
            message="note topic finished successfully",
            status_code=HttpStatus.OK
        )

    async def delete_note_topic(self, request: Request, note_topic_id: int) -> JSONResponse:
        note_topic = await self.service_note_topic.delete_note_topic(note_topic_id)

        return await response_factory(
            data=note_topic,
            message="note topic deleted successfully",
            status_code=HttpStatus.OK
        )
