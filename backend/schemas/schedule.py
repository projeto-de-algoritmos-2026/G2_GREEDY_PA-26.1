from datetime import datetime, time
from typing import Optional, List
from pydantic import BaseModel, Field

class WorkweekScheduleRequest(BaseModel):
    start_time: datetime
    work_start_time: time = Field(default=time(8, 0))
    work_end_time: time = Field(default=time(18, 0))
    workdays: List[int] = Field(default_factory=lambda: [0, 1, 2, 3, 4])

class ScheduledItem(BaseModel):
    task_id: str
    title: str
    start: datetime
    end: datetime
    lateness_minutes: Optional[int] = None
    room_id: Optional[int] = None

class IntervalSchedulingResponse(BaseModel):
    algorithm: str
    selected_count: int
    selected_tasks: List[ScheduledItem]

class LatenessSchedulingResponse(BaseModel):
    algorithm: str
    max_lateness_minutes: int
    scheduled_tasks: List[ScheduledItem]

class PartitioningResponse(BaseModel):
    algorithm: str
    rooms_used: int
    assignments: List[ScheduledItem]

class WorkweekSchedulingResponse(BaseModel):
    algorithm: str
    max_lateness_minutes: int
    scheduled_tasks: List[ScheduledItem]