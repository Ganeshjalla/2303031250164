"""
Example: wiring the Log() function into a FastAPI app.

1. At startup, authenticate once and store the token.
2. Add an HTTP middleware that logs every request lifecycle (start/success/error).
3. Call Log() inside handlers/services/db layer with specific, useful messages.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import time

from logging_middleware.logger import Log
from logging_middleware.auth import fetch_and_set_auth_token

app = FastAPI()


@app.on_event("startup")
def startup():
    # Replace with your real registered values / saved clientID & clientSecret
    fetch_and_set_auth_token(
        email="ramkrishna@abc.edu",
        name="ram krishna",
        roll_no="aa1bb",
        access_code="xgAsNC",
        client_id="d9cbb699-6a27-44a5-8d59-8b1befa816da",
        client_secret="tVJaaaRBSeXcRXeM",
    )
    Log("backend", "info", "config", "Application startup complete, auth token acquired.")


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    start = time.time()
    try:
        response = await call_next(request)
        duration_ms = round((time.time() - start) * 1000, 2)
        Log(
            "backend", "info", "middleware",
            f"{request.method} {request.url.path} completed with "
            f"status {response.status_code} in {duration_ms}ms"
        )
        return response
    except Exception as exc:
        Log(
            "backend", "fatal", "middleware",
            f"Unhandled exception on {request.method} {request.url.path}: {exc}"
        )
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.get("/example/{item_id}")
def get_item(item_id: int):
    if item_id <= 0:
        Log("backend", "warn", "handler", f"Received invalid item_id={item_id} in get_item")
        return JSONResponse(status_code=400, content={"detail": "item_id must be positive"})

    Log("backend", "debug", "service", f"Fetching item {item_id} from data source")
    # ... business logic / db call would go here ...
    return {"item_id": item_id, "name": "sample item"}
