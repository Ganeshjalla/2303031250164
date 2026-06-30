"""
FastAPI route definitions for the scheduler endpoints.
"""

from fastapi import APIRouter

from app.controller.scheduler_controller import get_all_schedules, get_depot_schedule

router = APIRouter(prefix="/schedule", tags=["scheduler"])


@router.get("")
def schedule_all():
    """Returns the optimal maintenance schedule for every depot."""
    return get_all_schedules()


@router.get("/{depot_id}")
def schedule_one(depot_id: int):
    """Returns the optimal maintenance schedule for a single depot."""
    return get_depot_schedule(depot_id)
