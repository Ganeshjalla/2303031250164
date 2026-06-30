"""
Reusable Logging Middleware.

Usage:
    from logging_middleware import Log

    Log("backend", "error", "handler", "received string, expected bool")
    Log("backend", "fatal", "db", "Critical database connection failure.")

The Log() function makes a POST request to the Test Server's Log API for
every call, matching the contract: Log(stack, level, package, message)

Configuration (auth token, base URL) is read from environment variables so
the package stays reusable across the codebase without hard-coded secrets:

    LOG_API_URL          (default: http://4.224.186.213/evaluation-service/logs)
    LOG_API_AUTH_TOKEN    Bearer token obtained from the Auth API (required)
"""

import os
import sys
import requests

from .constants import VALID_STACKS, VALID_LEVELS, ALL_PACKAGES, \
    BACKEND_ONLY_PACKAGES, FRONTEND_ONLY_PACKAGES

DEFAULT_LOG_API_URL = "http://4.224.186.213/evaluation-service/logs"


class LogValidationError(ValueError):
    """Raised when Log() is called with an invalid stack/level/package value."""
    pass


def _validate(stack: str, level: str, package: str) -> None:
    if stack not in VALID_STACKS:
        raise LogValidationError(
            f"Invalid stack '{stack}'. Must be one of {sorted(VALID_STACKS)}"
        )

    if level not in VALID_LEVELS:
        raise LogValidationError(
            f"Invalid level '{level}'. Must be one of {sorted(VALID_LEVELS)}"
        )

    if package not in ALL_PACKAGES:
        raise LogValidationError(
            f"Invalid package '{package}'. Must be one of {sorted(ALL_PACKAGES)}"
        )

    if stack == "backend" and package in FRONTEND_ONLY_PACKAGES:
        raise LogValidationError(
            f"Package '{package}' is frontend-only and cannot be used with stack 'backend'"
        )

    if stack == "frontend" and package in BACKEND_ONLY_PACKAGES:
        raise LogValidationError(
            f"Package '{package}' is backend-only and cannot be used with stack 'frontend'"
        )


def Log(stack: str, level: str, package: str, message: str) -> dict | None:
    """
    Send a log entry to the Test Server's Log API.

    Args:
        stack:   "backend" | "frontend"
        level:   "debug" | "info" | "warn" | "error" | "fatal"
        package: see constants.py for the allowed list per stack
        message: a specific, descriptive message about the event being logged

    Returns:
        The parsed JSON response (e.g. {"logID": ..., "message": "log created successfully"})
        on success, or None if the call failed (failure is logged to stderr but never raises,
        so a logging failure never crashes the calling application).
    """
    stack = stack.lower()
    level = level.lower()
    package = package.lower()

    try:
        _validate(stack, level, package)
    except LogValidationError as exc:
        # Fail loudly in dev so misuse of the logging contract is caught early,
        # but never let a bad log call take down the app.
        sys.stderr.write(f"[Log] validation error: {exc}\n")
        return None

    url = os.environ.get("LOG_API_URL", DEFAULT_LOG_API_URL)
    token = os.environ.get("LOG_API_AUTH_TOKEN")

    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    payload = {
        "stack": stack,
        "level": level,
        "package": package,
        "message": message,
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        # Never raise from a logging call - a logging outage should not break the app.
        sys.stderr.write(f"[Log] failed to send log: {exc}\n")
        return None
