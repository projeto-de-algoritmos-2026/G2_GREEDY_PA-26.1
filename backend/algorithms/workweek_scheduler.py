from datetime import datetime, time
from typing import List, Dict, Any, Set
from models.task import Task
from utils.datetime_utils import (
    normalize_workdays,
    move_to_next_work_slot,
    add_work_minutes,
)

def workweek_scheduler(
    tasks: List[Task],
    start_time: datetime,
    work_start_time: time,
    work_end_time: time,
    workdays: List[int],
) -> Dict[str, Any]:
    valid_tasks = [task for task in tasks if task.task_type == "duration"]
    workdays_set: Set[int] = normalize_workdays(workdays)

    ordered = sorted(
        valid_tasks,
        key=lambda task: task.deadline if task.deadline is not None else datetime.max,
    )

    current_time = move_to_next_work_slot(
        start_time,
        work_start_time,
        work_end_time,
        workdays_set,
    )

    scheduled = []
    max_lateness_minutes = 0

    for task in ordered:
        current_time = move_to_next_work_slot(
            current_time,
            work_start_time,
            work_end_time,
            workdays_set,
        )

        task_start = current_time
        task_end = add_work_minutes(
            task_start,
            task.duration_minutes,
            work_start_time,
            work_end_time,
            workdays_set,
        )

        lateness_minutes = 0
        if task.deadline is not None:
            lateness_minutes = max(
                0,
                int((task_end - task.deadline).total_seconds() // 60),
            )

        max_lateness_minutes = max(max_lateness_minutes, lateness_minutes)

        scheduled.append(
            {
                "task": task,
                "start": task_start,
                "end": task_end,
                "lateness_minutes": lateness_minutes,
            }
        )

        current_time = task_end

    return {
        "algorithm": "workweek_scheduler",
        "max_lateness_minutes": max_lateness_minutes,
        "scheduled_tasks": scheduled,
    }