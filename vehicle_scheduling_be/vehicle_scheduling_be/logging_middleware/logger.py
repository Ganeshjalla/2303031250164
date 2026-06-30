"""
Reusable Logging Middleware for the Campus Hiring Evaluation - Backend track.

Usage:
    from logging_middleware.logger import Log

    Log("backend", "error", "handler", "received string, expected bool")
    Log("backend", "fatal", "db", "Critical database connection failure.")
"""

import os
import requests

LOG_API_URL = "http://4.224.186.213/evaluation-service/logs"

VALID_STACKS = {"backend", "frontend"}
VALID_LEVELS = {"debug", "info", "warn", "error", "fatal"}
VALID_PACKAGES = {
    # backend-only
    "cache", "controller", "cron_job", "db", "domain",
    "handler", "repository", "route", "service",
    # frontend-only
    "api", "component", "hook", "page", "state", "style",
    # shared (backend + frontend)
    "auth", "config", "middleware", "utils",
}

# Set after calling the Authentication API, e.g.:
#   os.environ["AFFORDMED_AUTH_TOKEN"] = "<access_token>"
_AUTH_TOKEN_ENV_VAR = "AFFORDMED_AUTH_TOKEN"


def Log(stack: str, level: str, package: str, message: str) -> dict | None:
    """
    Sends a structured log entry to the Test Server's Log API.

    Args:
        stack:   "backend" | "frontend"
        level:   "debug" | "info" | "warn" | "error" | "fatal"
        package: one of the allowed package values (see VALID_PACKAGES)
        message: clear, specific, human-readable description of the event/state

    Returns:
        Parsed JSON response (e.g. {"logID": ..., "message": "log created successfully"})
        on success, or None if validation/the request failed. Never raises -
        a logging call must never crash the calling application.
    """
    stack = stack.lower()
    level = level.lower()
    package = package.lower()

    if stack not in VALID_STACKS:
        print(f"[Log] Invalid stack '{stack}', must be one of {sorted(VALID_STACKS)}")
        return None
    if level not in VALID_LEVELS:
        print(f"[Log] Invalid level '{level}', must be one of {sorted(VALID_LEVELS)}")
        return None
    if package not in VALID_PACKAGES:
        print(f"[Log] Invalid package '{package}', must be one of {sorted(VALID_PACKAGES)}")
        return None

    payload = {
        "stack": stack,
        "level": level,
        "package": package,
        "message": message,
    }

    headers = {"Content-Type": "application/json"}
    token = os.environ.get(_AUTH_TOKEN_ENV_VAR)
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        resp = requests.post(LOG_API_URL, json=payload, headers=headers, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as exc:
        # Fail silently to console so a logging failure never breaks app flow.
        print(f"[Log] Failed to send log to Test Server: {exc}")
        return None
