from datetime import datetime
from typing import List

from algorithms.interval_partitioning import interval_partitioning
from algorithms.interval_scheduling import interval_scheduling
from algorithms.minimize_lateness import minimize_lateness
from algorithms.workweek_scheduler import workweek_scheduler
from models.task import Task
from repositories.task_repository import TaskRepository
from schemas.task import TaskDurationCreate, TaskFixedCreate, TaskRead
from schemas.schedule import ScheduledItem

class SchedulerService:
    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    def _to_task_read(self, task: Task) -> TaskRead:
        return TaskRead(
            id=task.id,
            title=task.title,
            task_type=task.task_type,
            duration_minutes=task.duration_minutes,
            deadline=task.deadline,
            fixed_start=task.fixed_start,
            fixed_end=task.fixed_end,
            priority=task.priority,
            notes=task.notes,
            created_at=task.created_at,
        )

    def create_duration_task(self, payload: TaskDurationCreate) -> TaskRead:
        task = Task(
            id=Task.new_id(),
            title=payload.title,
            task_type="duration",
            duration_minutes=payload.duration_minutes,
            deadline=payload.deadline,
            priority=payload.priority,
            notes=payload.notes,
        )
        self.repository.add(task)
        return self._to_task_read(task)

    def create_fixed_task(self, payload: TaskFixedCreate) -> TaskRead:
        if payload.end <= payload.start:
            raise ValueError("end must be after start")

        duration_minutes = int((payload.end - payload.start).total_seconds() // 60)
        if duration_minutes <= 0:
            raise ValueError("fixed task duration must be greater than zero minutes")

        task = Task(
            id=Task.new_id(),
            title=payload.title,
            task_type="fixed",
            duration_minutes=duration_minutes,
            deadline=payload.deadline,
            fixed_start=payload.start,
            fixed_end=payload.end,
            priority=payload.priority,
            notes=payload.notes,
        )
        self.repository.add(task)
        return self._to_task_read(task)

    def list_tasks(self) -> List[TaskRead]:
        return [self._to_task_read(task) for task in self.repository.list_all()]

    def clear_tasks(self) -> None:
        self.repository.clear()

    def schedule_interval_scheduling(self) -> dict:
        result = interval_scheduling(self.repository.list_all())
        selected = [
            ScheduledItem(
                task_id=task.id,
                title=task.title,
                start=task.fixed_start,
                end=task.fixed_end,
            )
            for task in result["selected_tasks"]
        ]
        return {
            "algorithm": result["algorithm"],
            "selected_count": result["selected_count"],
            "selected_tasks": selected,
        }

    def schedule_minimize_lateness(self, start_time: datetime) -> dict:
        result = minimize_lateness(self.repository.list_all(), start_time=start_time)
        scheduled = [
            ScheduledItem(
                task_id=item["task"].id,
                title=item["task"].title,
                start=item["start"],
                end=item["end"],
                lateness_minutes=item["lateness_minutes"],
            )
            for item in result["scheduled_tasks"]
        ]
        return {
            "algorithm": result["algorithm"],
            "max_lateness_minutes": result["max_lateness_minutes"],
            "scheduled_tasks": scheduled,
        }

    def schedule_interval_partitioning(self) -> dict:
        result = interval_partitioning(self.repository.list_all())
        assignments = [
            ScheduledItem(
                task_id=item["task"].id,
                title=item["task"].title,
                start=item["task"].fixed_start,
                end=item["task"].fixed_end,
                room_id=item["room_id"],
            )
            for item in result["assignments"]
        ]
        return {
            "algorithm": result["algorithm"],
            "rooms_used": result["rooms_used"],
            "assignments": assignments,
        }

    def schedule_workweek(
        self,
        start_time: datetime,
        work_start_time,
        work_end_time,
        workdays,
    ) -> dict:
        result = workweek_scheduler(
            self.repository.list_all(),
            start_time=start_time,
            work_start_time=work_start_time,
            work_end_time=work_end_time,
            workdays=workdays,
        )
        scheduled = [
            ScheduledItem(
                task_id=item["task"].id,
                title=item["task"].title,
                start=item["start"],
                end=item["end"],
                lateness_minutes=item["lateness_minutes"],
            )
            for item in result["scheduled_tasks"]
        ]
        return {
            "algorithm": result["algorithm"],
            "max_lateness_minutes": result["max_lateness_minutes"],
            "scheduled_tasks": scheduled,
        }