from fastapi import APIRouter, HTTPException
from schemas.task import TaskDurationCreate, TaskFixedCreate, TaskRead
from services.scheduler_service import SchedulerService

router = APIRouter()

def _get_service() -> SchedulerService:
    from main import scheduler_service
    return scheduler_service

@router.post("/duration", response_model=TaskRead)
def create_duration_task(payload: TaskDurationCreate):
    try:
        return _get_service().create_duration_task(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@router.post("/fixed", response_model=TaskRead)
def create_fixed_task(payload: TaskFixedCreate):
    try:
        return _get_service().create_fixed_task(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@router.get("", response_model=list[TaskRead])
def list_tasks():
    return _get_service().list_tasks()

@router.delete("/{task_id}")
def delete_task(task_id: str):
    deleted = _get_service().delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "task removed"}

@router.put("/{task_id}", response_model=TaskRead)
def update_task(task_id: str, payload: TaskDurationCreate):
    try:
        return _get_service().update_duration_task(task_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@router.delete("")
def clear_tasks():
    _get_service().clear_tasks()
    return {"message": "all tasks removed"}