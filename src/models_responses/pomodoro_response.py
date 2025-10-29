from datetime import datetime

from pydantic import BaseModel


class PomodoroResponse(BaseModel):
    pomodoro_id: int
    user_id: int
    pomodoro_name: str
    focus_minutes: int
    focus_seconds: int
    break_short: int
    break_long: int
    rounds: int
    create_at: datetime
    update_at: datetime
