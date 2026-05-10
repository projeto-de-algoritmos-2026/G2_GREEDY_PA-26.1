from datetime import datetime, timedelta
from typing import List, Dict, Any
from models.task import Task

def minimize_lateness(tasks: List[Task], start_time: datetime) -> Dict[str, Any]:
    valid_tasks = [task for task in tasks if task.task_type == "duration"]

    ordered = sorted(
        valid_tasks,
        key=lambda task: task.deadline if task.deadline is not None else datetime.max,
    )

    current_time = start_time
    scheduled = []
    max_lateness_minutes = 0

    for task in ordered:
        task_start = current_time
        task_end = current_time + timedelta(minutes=task.duration_minutes)

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
        "algorithm": "minimize_lateness",
        "max_lateness_minutes": max_lateness_minutes,
        "scheduled_tasks": scheduled,
    }