import heapq
from typing import List, Dict, Any, Tuple
from models.task import Task

def interval_partitioning(tasks: List[Task]) -> Dict[str, Any]:
    valid_tasks = [
        task for task in tasks
        if task.task_type == "fixed" and task.fixed_start is not None and task.fixed_end is not None
    ]

    ordered = sorted(valid_tasks, key=lambda task: task.fixed_start)
    heap: List[Tuple] = []
    assignments = []
    next_room_id = 1

    for task in ordered:
        if heap and heap[0][0] <= task.fixed_start:
            room_end, room_id = heapq.heappop(heap)
        else:
            room_id = next_room_id
            next_room_id += 1

        heapq.heappush(heap, (task.fixed_end, room_id))

        assignments.append(
            {
                "task": task,
                "room_id": room_id,
            }
        )

    return {
        "algorithm": "interval_partitioning",
        "rooms_used": next_room_id - 1,
        "assignments": assignments,
    }