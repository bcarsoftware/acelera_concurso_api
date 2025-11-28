from typing import List

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.constraints import HttpStatus
from src.db.model.models import RateLog
from src.exceptions.database_exception import DatabaseException
from src.models_dtos.rate_log_dto import RateLogDTO
from src.models_responses.rate_log_response import RateLogResponse
from src.repositories.rate_log.repository_rate_log_interface import RateLogRepositoryInterface


class RateLogRepository(RateLogRepositoryInterface):
    async def find_rate_logs_entry(self, rate_log_dto: RateLogDTO) -> List[RateLogResponse]:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(RateLog).filter(
                        and_(
                            RateLog.subject == rate_log_dto.subject,
                            RateLog.topic == rate_log_dto.topic,
                            RateLog.note_subject == rate_log_dto.note_subject,
                            RateLog.note_topic == rate_log_dto.note_topic,
                            RateLog.user_id == rate_log_dto.user_id,
                        )
                    )
                )

                rate_logs = response.scalars().all()

                if not rate_logs:
                    raise DatabaseException("note topic not found", HttpStatus.NOT_FOUND)
            return [
                RateLogResponse.model_validate(log_rate)
                for log_rate in rate_logs
            ]
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)
