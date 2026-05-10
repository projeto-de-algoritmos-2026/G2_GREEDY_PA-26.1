from fastapi import APIRouter, HTTPException
from schemas.schedule import WorkweekScheduleRequest
from services.scheduler_service import SchedulerService

router = APIRouter()

def _get_service() -> SchedulerService:
    from main import scheduler_service
    return scheduler_service

@router.post("/interval")
def schedule_interval():
    return _get_service().schedule_interval_scheduling()

@router.post("/lateness")
def schedule_lateness(payload: WorkweekScheduleRequest):
    try:
        return _get_service().schedule_minimize_lateness(payload.start_time)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@router.post("/partitioning")
def schedule_partitioning():
    return _get_service().schedule_interval_partitioning()

@router.post("/workweek")
def schedule_workweek(payload: WorkweekScheduleRequest):
    try:
        return _get_service().schedule_workweek(
            start_time=payload.start_time,
            work_start_time=payload.work_start_time,
            work_end_time=payload.work_end_time,
            workdays=payload.workdays,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))