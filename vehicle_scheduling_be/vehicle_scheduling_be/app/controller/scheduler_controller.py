"""
Controller layer: translates HTTP requests into service calls and
shapes the JSON response. Keeps route definitions thin.
"""

from dataclasses import asdict
from fastapi import HTTPException

from app.service.scheduler_service import schedule_all_depots, schedule_single_depot
from logging_middleware.logger import Log


def get_all_schedules():
    Log("backend", "info", "controller", "Handling request: GET /schedule (all depots)")
    schedules = schedule_all_depots()
    return {"schedules": [asdict(s) for s in schedules]}


def get_depot_schedule(depot_id: int):
    Log("backend", "info", "controller", f"Handling request: GET /schedule/{depot_id}")
    try:
        schedule = schedule_single_depot(depot_id)
        return asdict(schedule)
    except ValueError as exc:
        Log("backend", "warn", "controller", f"Depot {depot_id} not found")
        raise HTTPException(status_code=404, detail=str(exc))
