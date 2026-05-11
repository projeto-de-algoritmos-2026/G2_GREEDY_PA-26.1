from datetime import datetime, time, timedelta, date
from typing import Iterable, Set

def normalize_workdays(workdays: Iterable[int]) -> Set[int]:
    return {int(day) for day in workdays}

def is_workday(dt: datetime, workdays: Set[int]) -> bool:
    return dt.weekday() in workdays

def combine_date_and_time(d: date, t: time) -> datetime:
    return datetime.combine(d, t)

def next_workday_date(current_date: date, workdays: Set[int]) -> date:
    candidate = current_date
    while True:
        if candidate.weekday() in workdays:
            return candidate
        candidate = candidate + timedelta(days=1)

def move_to_next_work_slot(
    dt: datetime,
    work_start_time: time,
    work_end_time: time,
    workdays: Set[int],
) -> datetime:
    current = dt.replace(tzinfo=None) if dt.tzinfo is not None else dt

    while not is_workday(current, workdays):
        current = combine_date_and_time(current.date() + timedelta(days=1), work_start_time)

    day_start = combine_date_and_time(current.date(), work_start_time)
    day_end = combine_date_and_time(current.date(), work_end_time)

    if current < day_start:
        return day_start

    if current >= day_end:
        next_day = next_workday_date(current.date() + timedelta(days=1), workdays)
        return combine_date_and_time(next_day, work_start_time)

    return current

def add_work_minutes(
    start_dt: datetime,
    minutes: int,
    work_start_time: time,
    work_end_time: time,
    workdays: Set[int],
) -> datetime:
    if minutes < 0:
        raise ValueError("minutes must be non-negative")

    current = move_to_next_work_slot(start_dt, work_start_time, work_end_time, workdays)
    remaining = minutes

    while remaining > 0:
        current = move_to_next_work_slot(current, work_start_time, work_end_time, workdays)
        day_end = combine_date_and_time(current.date(), work_end_time)
        available_today = int((day_end - current).total_seconds() // 60)

        if available_today <= 0:
            next_day = next_workday_date(current.date() + timedelta(days=1), workdays)
            current = combine_date_and_time(next_day, work_start_time)
            continue

        consumed = min(available_today, remaining)
        current = current + timedelta(minutes=consumed)
        remaining -= consumed

        if remaining > 0:
            next_day = next_workday_date(current.date() + timedelta(days=1), workdays)
            current = combine_date_and_time(next_day, work_start_time)

    return current