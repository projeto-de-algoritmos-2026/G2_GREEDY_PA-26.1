from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import schedules, tasks
from repositories.task_repository import TaskRepository
from services.scheduler_service import SchedulerService

app = FastAPI(title="Greedy Task Scheduler", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

task_repository = TaskRepository()
scheduler_service = SchedulerService(task_repository)

app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
app.include_router(schedules.router, prefix="/schedule", tags=["Schedules"])


@app.get("/")
def root():
    return {
        "message": "Greedy Task Scheduler API",
        "endpoints": [
            "/tasks/duration",
            "/tasks/fixed",
            "/tasks",
            "/schedule/interval",
            "/schedule/lateness",
            "/schedule/partitioning",
            "/schedule/workweek",
        ],
    }