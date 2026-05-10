from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field

class TaskDurationCreate(BaseModel):
    title: str
    duration_minutes: int = Field(gt=0)
    deadline: Optional[datetime] = None
    priority: int = Field(default=1, ge=1, le=5)
    notes: Optional[str] = None

class TaskFixedCreate(BaseModel):
    title: str
    start: datetime
    end: datetime
    deadline: Optional[datetime] = None
    priority: int = Field(default=1, ge=1, le=5)
    notes: Optional[str] = None

class TaskRead(BaseModel):
    id: str
    title: str
    task_type: Literal["duration", "fixed"]
    duration_minutes: int
    deadline: Optional[datetime] = None
    fixed_start: Optional[datetime] = None
    fixed_end: Optional[datetime] = None
    priority: int
    notes: Optional[str] = None
    created_at: datetime