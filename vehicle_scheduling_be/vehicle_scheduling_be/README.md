# Vehicle Maintenance Scheduler Microservice

A backend microservice that determines the optimal subset of vehicle
maintenance tasks to perform at each depot, maximizing total operational
impact without exceeding the depot's daily mechanic-hour budget.

## Problem

This is a 0/1 Knapsack problem:
- **weight** = task `Duration` (hours)
- **value** = task `Impact` score
- **capacity** = depot's `MechanicHours`

Solved via bottom-up dynamic programming in `O(n * capacity)` time, which
guarantees the true optimum (unlike a greedy value/weight-ratio heuristic,
which can be suboptimal for 0/1 knapsack) and scales comfortably for
realistic mechanic-hour budgets.

## Project Structure

```
vehicle_scheduling_be/
├── app/
│   ├── main.py                       # FastAPI entrypoint + request logging middleware
│   ├── config.py                     # env-driven configuration
│   ├── auth/
│   │   └── token_manager.py          # fetches & caches the Bearer token
│   ├── clients/
│   │   └── evaluation_api_client.py  # calls Depot API & Vehicles(Task) API
│   ├── controller/
│   │   └── scheduler_controller.py   # HTTP <-> service translation
│   ├── service/
│   │   └── scheduler_service.py      # knapsack DP + orchestration
│   ├── domain/
│   │   └── models.py                 # Depot, Task, DepotSchedule dataclasses
│   └── route/
│       └── scheduler_routes.py       # FastAPI router
├── logging_middleware/               # reusable Log(stack, level, package, message) package
│   ├── logger.py
│   └── auth.py
├── tests/
│   └── test_knapsack.py              # offline solver test with sample data
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in your registered credentials
```

## Run

```bash
uvicorn app.main:app --reload --port 8000
```

## Endpoints

| Method | Path                 | Description                                  |
|--------|----------------------|-----------------------------------------------|
| GET    | `/schedule`          | Optimal schedule for every depot              |
| GET    | `/schedule/{depotId}`| Optimal schedule for a single depot           |
| GET    | `/health`            | Liveness check                                |

### Sample response — `GET /schedule/1`

```json
{
  "depot_id": 1,
  "mechanic_hours_available": 60,
  "mechanic_hours_used": 58,
  "total_impact": 142,
  "selected_task_ids": ["264e638f-1c7a-4d67-9f9c-53f3d1766d37", "..."]
}
```

## Notes

- No data is hard-coded or persisted to a database; depots and tasks are
  fetched live from the protected Test Server APIs on every request.
- Logging is integrated throughout the request lifecycle (middleware),
  the repository/client layer, and the service layer using the reusable
  `logging_middleware` package.
