from typing import List

from src.core.constraints import Points
from src.models_dtos.subject_dto import SubjectDTO
from src.models_responses.subject_response import SubjectResponse
from src.repositories.note_subject.repository_note_subject import NoteSubjectRepository
from src.repositories.note_subject.repository_note_subject_interface import NoteSubjectRepositoryInterface
from src.repositories.subject.repository_subject import SubjectRepository
from src.repositories.subject.repository_subject_interface import SubjectRepositoryInterface
from src.services.subject.service_subject_interface import ServiceSubjectInterface
from src.utils.managers.subject_manager import SubjectManager


class ServiceSubject(ServiceSubjectInterface):
    def __init__(self) -> None:
        self.subject_repository: SubjectRepositoryInterface = SubjectRepository()
        self.note_subject_repository: NoteSubjectRepositoryInterface = NoteSubjectRepository()

    async def create_subject(self, subject_dto: SubjectDTO) -> SubjectResponse:
        await SubjectManager.make_validation(subject_dto)

        return await self.subject_repository.create_subject(subject_dto)

    async def update_subject(self, subject_dto: SubjectDTO, subject_id: int) -> SubjectResponse:
        await SubjectManager.make_validation(subject_dto)

        return await self.subject_repository.update_subject(subject_dto, subject_id)

    async def get_subjects(self, tender_id: int) -> List[SubjectResponse]:
        return await self.subject_repository.get_subjects(tender_id)

    async def get_subject_by_name(self, tender_id: int, name: str) -> List[SubjectResponse]:
        return await self.subject_repository.get_subject_by_name(tender_id, name)

    async def finish_subject(self, subject_id: int) -> SubjectResponse:
        note_subjects_unfinished = await self.note_subject_repository.exists_note_subjects_incomplete(subject_id)

        await SubjectManager.lock_unfinished_notes_subject(note_subjects_unfinished)

        return await self.subject_repository.finish_subject(subject_id)

    async def delete_subject(self, subject_id: int) -> SubjectResponse:
        note_subjects_unfinished = await self.note_subject_repository.exists_note_subjects_incomplete(subject_id)

        await SubjectManager.lock_unfinished_notes_subject(note_subjects_unfinished)

        counted_notes_finished = await self.note_subject_repository.count_finished_note_subjects(subject_id)
        points = counted_notes_finished * Points.NOTE_POINTS + Points.SUBJECT_POINTS

        return await self.subject_repository.delete_subject(subject_id, points)
