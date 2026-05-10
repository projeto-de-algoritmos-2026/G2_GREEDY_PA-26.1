from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Literal
from uuid import uuid4

TaskType = Literal["duration", "fixed"]

@dataclass
class Task:
    id: str
    title: str
    task_type: TaskType
    duration_minutes: int
    deadline: Optional[datetime] = None
    fixed_start: Optional[datetime] = None
    fixed_end: Optional[datetime] = None
    priority: int = 1
    notes: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

    @staticmethod
    def new_id() -> str:
        return uuid4().hex