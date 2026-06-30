"""
Domain models for the Vehicle Maintenance Scheduler.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class Depot:
    id: int
    mechanic_hours: int


@dataclass
class Task:
    task_id: str
    duration: int
    impact: int


@dataclass
class DepotSchedule:
    depot_id: int
    mechanic_hours_available: int
    mechanic_hours_used: int
    total_impact: int
    selected_task_ids: List[str]
