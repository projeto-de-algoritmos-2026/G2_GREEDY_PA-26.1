from typing import List, Optional
from models.task import Task

class TaskRepository:
    def __init__(self) -> None:
        self._tasks: List[Task] = []

    def add(self, task: Task) -> Task:
        self._tasks.append(task)
        return task

    def list_all(self) -> List[Task]:
        return list(self._tasks)

    def list_by_type(self, task_type: str) -> List[Task]:
        return [task for task in self._tasks if task.task_type == task_type]

    def get_by_id(self, task_id: str) -> Optional[Task]:
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def delete_by_id(self, task_id: str) -> bool:
        for index, task in enumerate(self._tasks):
            if task.id == task_id:
                del self._tasks[index]
                return True
        return False

    def update(self, task: Task) -> Optional[Task]:
        for index, t in enumerate(self._tasks):
            if t.id == task.id:
                self._tasks[index] = task
                return task
        return None

    def clear(self) -> None:
        self._tasks.clear()