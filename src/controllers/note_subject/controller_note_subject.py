from starlette.requests import Request
from starlette.responses import JSONResponse

from src.controllers.note_subject.controller_note_subject_interface import NoteSubjectControllerInterface
from src.core.constraints import HttpStatus
from src.core.response_factory import response_factory
from src.services.note_subject.service_note_subject import ServiceNoteSubject
from src.services.note_subject.service_note_subject_interface import ServiceNoteSubjectInterface
from src.utils.managers.note_subject_manager import NoteSubjectManager


class NoteSubjectController(NoteSubjectControllerInterface):
    def __init__(self) -> None:
        self.service_note_subject: ServiceNoteSubjectInterface = ServiceNoteSubject()

    async def create_note_subject(self, request: Request) -> JSONResponse:
        payload = await request.json()

        note_subject_dto = await NoteSubjectManager.convert_payload_to_note_subject_dto(payload)

        response = await self.service_note_subject.create_note_subject(note_subject_dto)

        return await response_factory(
            data=response,
            message="note subject created successfully",
            status_code=HttpStatus.CREATED
        )

    async def update_note_subject(self, request: Request, note_subject_id: int) -> JSONResponse:
        payload = await request.json()

        note_subject_dto = await NoteSubjectManager.convert_payload_to_note_subject_dto(payload)

        response = await self.service_note_subject.update_note_subject(note_subject_dto, note_subject_id)

        return await response_factory(
            data=response,
            message="note subject updated successfully",
            status_code=HttpStatus.OK
        )

    async def find_note_subject_by_subject_id(self, request: Request, subject_id: int) -> JSONResponse:
        responses = await self.service_note_subject.find_note_subject_by_subject_id(subject_id)

        return await response_factory(
            data=responses,
            message="note subject found successfully",
            status_code=HttpStatus.OK
        )

    async def finish_note_subject(self, request: Request, note_subject_id: int) -> JSONResponse:
        payload = await request.json()

        note_subject_dto = await NoteSubjectManager.convert_payload_to_note_subject_dto(payload)

        response = await self.service_note_subject.finish_note_subject(note_subject_dto, note_subject_id)

        return await response_factory(
            data=response,
            message="note subject finished successfully",
            status_code=HttpStatus.OK
        )

    async def delete_note_subject(self, request: Request, note_subject_id: int) -> JSONResponse:
        response = await self.service_note_subject.delete_note_subject(note_subject_id)

        return await response_factory(
            data=response,
            message="note subject deleted successfully",
            status_code=HttpStatus.OK
        )
