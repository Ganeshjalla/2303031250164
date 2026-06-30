"""
Application entrypoint.

Run with:
    uvicorn app.main:app --reload --port 8000
"""

import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.route.scheduler_routes import router as scheduler_router
from logging_middleware.logger import Log

app = FastAPI(title="Vehicle Maintenance Scheduler Microservice")
app.include_router(scheduler_router)


@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    start = time.time()
    try:
        response = await call_next(request)
        duration_ms = round((time.time() - start) * 1000, 2)
        Log(
            "backend", "info", "middleware",
            f"{request.method} {request.url.path} -> {response.status_code} "
            f"in {duration_ms}ms"
        )
        return response
    except Exception as exc:
        Log(
            "backend", "fatal", "middleware",
            f"Unhandled exception on {request.method} {request.url.path}: {exc}"
        )
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.get("/health")
def health():
    return {"status": "ok"}


@app.on_event("startup")
def on_startup():
    Log("backend", "info", "config", "Vehicle Maintenance Scheduler microservice started.")
