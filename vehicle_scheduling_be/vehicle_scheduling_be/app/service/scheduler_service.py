"""
Core business logic: for each depot, choose the subset of tasks that
maximises total Impact without exceeding the depot's MechanicHours budget.

This is the classic 0/1 Knapsack problem:
    weight(task) = Duration
    value(task)  = Impact
    capacity     = depot.mechanic_hours

DP approach (bottom-up, O(n * capacity) time and space) is used because:
  - it's optimal (unlike a greedy ratio-based heuristic, which is *not*
    guaranteed optimal for 0/1 knapsack),
  - capacity (mechanic-hours per depot) is a bounded, modest integer in
    this domain, making the O(n * capacity) DP both correct and fast
    enough for real-world scale here.
"""

from typing import List

from app.clients.evaluation_api_client import fetch_depots, fetch_tasks
from app.domain.models import Depot, Task, DepotSchedule
from logging_middleware.logger import Log


def solve_knapsack(tasks: List[Task], capacity: int) -> tuple[int, List[Task]]:
    """
    Returns (max_total_impact, selected_tasks) for a single depot using
    0/1 knapsack DP.
    """
    n = len(tasks)
    # dp[c] = best impact achievable with c mechanic-hours used so far
    dp = [0] * (capacity + 1)
    # keep[i][c] = True if task i was taken to achieve dp[c] at step i
    keep = [[False] * (capacity + 1) for _ in range(n)]

    for i, task in enumerate(tasks):
        # iterate capacity backwards so each task is only used once (0/1, not unbounded)
        for c in range(capacity, task.duration - 1, -1):
            candidate = dp[c - task.duration] + task.impact
            if candidate > dp[c]:
                dp[c] = candidate
                keep[i][c] = True

    # backtrack to find which tasks were selected
    selected = []
    c = capacity
    for i in range(n - 1, -1, -1):
        if keep[i][c]:
            selected.append(tasks[i])
            c -= tasks[i].duration

    return dp[capacity], selected


def schedule_all_depots() -> List[DepotSchedule]:
    """
    Fetches all depots and tasks, then computes the optimal maintenance
    schedule (max total Impact within MechanicHours budget) per depot.
    """
    depots = fetch_depots()
    all_tasks = fetch_tasks()

    schedules: List[DepotSchedule] = []
    for depot in depots:
        Log("backend", "debug", "service",
            f"Solving knapsack for depot {depot.id} with capacity={depot.mechanic_hours} "
            f"and {len(all_tasks)} candidate tasks")

        total_impact, selected = solve_knapsack(all_tasks, depot.mechanic_hours)
        used_hours = sum(t.duration for t in selected)

        schedules.append(
            DepotSchedule(
                depot_id=depot.id,
                mechanic_hours_available=depot.mechanic_hours,
                mechanic_hours_used=used_hours,
                total_impact=total_impact,
                selected_task_ids=[t.task_id for t in selected],
            )
        )

        Log("backend", "info", "service",
            f"Depot {depot.id}: selected {len(selected)} tasks, used {used_hours}/"
            f"{depot.mechanic_hours} mechanic-hours, total impact={total_impact}")

    return schedules


def schedule_single_depot(depot_id: int) -> DepotSchedule:
    """Computes the optimal schedule for one specific depot."""
    depots = {d.id: d for d in fetch_depots()}
    if depot_id not in depots:
        Log("backend", "warn", "service", f"Requested unknown depot_id={depot_id}")
        raise ValueError(f"Depot {depot_id} not found")

    depot = depots[depot_id]
    all_tasks = fetch_tasks()

    total_impact, selected = solve_knapsack(all_tasks, depot.mechanic_hours)
    used_hours = sum(t.duration for t in selected)

    Log("backend", "info", "service",
        f"Depot {depot.id}: selected {len(selected)} tasks, used {used_hours}/"
        f"{depot.mechanic_hours} mechanic-hours, total impact={total_impact}")

    return DepotSchedule(
        depot_id=depot.id,
        mechanic_hours_available=depot.mechanic_hours,
        mechanic_hours_used=used_hours,
        total_impact=total_impact,
        selected_task_ids=[t.task_id for t in selected],
    )
