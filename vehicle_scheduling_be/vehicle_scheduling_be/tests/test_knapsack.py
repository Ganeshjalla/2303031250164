"""
Standalone test for the knapsack solver using sample data (mirrors the
shape of real Depot/Task API responses), without hitting the network.
Run with: python tests/test_knapsack.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.domain.models import Task
from app.service.scheduler_service import solve_knapsack


def main():
    tasks = [
        Task(task_id="t1", duration=2, impact=5),
        Task(task_id="t2", duration=1, impact=5),
        Task(task_id="t3", duration=3, impact=10),
        Task(task_id="t4", duration=6, impact=2),
        Task(task_id="t5", duration=4, impact=9),
    ]
    capacity = 7

    total_impact, selected = solve_knapsack(tasks, capacity)

    print(f"Capacity: {capacity}")
    print(f"Max total impact: {total_impact}")
    print("Selected tasks:")
    for t in selected:
        print(f"  - {t.task_id}: duration={t.duration}, impact={t.impact}")
    print(f"Total duration used: {sum(t.duration for t in selected)}")


if __name__ == "__main__":
    main()
