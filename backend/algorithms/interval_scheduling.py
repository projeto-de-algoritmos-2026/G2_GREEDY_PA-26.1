from datetime import datetime
from typing import List, Dict, Any
from models.task import Task

def interval_scheduling(tasks: List[Task]) -> Dict[str, Any]:
    valid_tasks = [
        task for task in tasks
        if task.task_type == "fixed" and task.fixed_start is not None and task.fixed_end is not None
    ]

    ordered = sorted(valid_tasks, key=lambda task: task.fixed_end)
    selected = []
    current_end = None

    for task in ordered:
        if current_end is None or task.fixed_start >= current_end:
            selected.append(task)
            current_end = task.fixed_end

    return {
        "algorithm": "interval_scheduling",
        "selected_tasks": selected,
        "selected_count": len(selected),
    }