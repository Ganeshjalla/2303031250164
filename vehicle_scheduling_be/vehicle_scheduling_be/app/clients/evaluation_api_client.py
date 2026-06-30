"""
Thin HTTP client for the Test Server's Depot and Vehicle/Task APIs.
No caching/hard-coding of data - every call hits the live protected APIs.
"""

from typing import List

import requests

from app import config
from app.auth.token_manager import auth_headers
from app.domain.models import Depot, Task
from logging_middleware.logger import Log


def fetch_depots() -> List[Depot]:
    Log("backend", "info", "repository", "Fetching depot list from Depot API")
    try:
        resp = requests.get(config.DEPOTS_ENDPOINT, headers=auth_headers(), timeout=10)
        resp.raise_for_status()
        raw = resp.json().get("depots", [])
        depots = [Depot(id=d["ID"], mechanic_hours=d["MechanicHours"]) for d in raw]
        Log("backend", "info", "repository", f"Fetched {len(depots)} depots successfully")
        return depots
    except requests.exceptions.RequestException as exc:
        Log("backend", "error", "repository", f"Failed to fetch depots: {exc}")
        raise


def fetch_tasks(depot_id: int | None = None) -> List[Task]:
    """
    Fetches maintenance tasks from the Vehicles API. If the API supports
    filtering by depot (e.g. ?depotId=), it is passed through; otherwise
    the full task list is returned and the caller can partition it.
    """
    params = {"depotId": depot_id} if depot_id is not None else None
    Log("backend", "info", "repository",
        f"Fetching tasks from Vehicles API"
        + (f" for depotId={depot_id}" if depot_id is not None else " (all depots)"))
    try:
        resp = requests.get(
            config.VEHICLES_ENDPOINT, headers=auth_headers(), params=params, timeout=10
        )
        resp.raise_for_status()
        raw = resp.json().get("vehicles", [])
        tasks = [
            Task(task_id=t["TaskID"], duration=t["Duration"], impact=t["Impact"])
            for t in raw
        ]
        Log("backend", "info", "repository", f"Fetched {len(tasks)} tasks successfully")
        return tasks
    except requests.exceptions.RequestException as exc:
        Log("backend", "error", "repository", f"Failed to fetch tasks: {exc}")
        raise
