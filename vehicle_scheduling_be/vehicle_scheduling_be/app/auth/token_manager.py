"""
Handles obtaining and caching the Bearer token from the Test Server's
Authentication API, and registers it with the logging_middleware package
so every Log() call is automatically authenticated.
"""

import requests

from app import config
from logging_middleware.logger import Log

_cached_token: str | None = None


def get_token() -> str:
    """
    Returns a cached bearer token, fetching a fresh one from the
    Authentication API on first call.
    """
    global _cached_token

    if _cached_token:
        return _cached_token

    payload = {
        "email": config.REG_EMAIL,
        "name": config.REG_NAME,
        "rollNo": config.REG_ROLL_NO,
        "accessCode": config.REG_ACCESS_CODE,
        "clientID": config.REG_CLIENT_ID,
        "clientSecret": config.REG_CLIENT_SECRET,
    }

    try:
        resp = requests.post(config.AUTH_ENDPOINT, json=payload, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        _cached_token = data["access_token"]

        # Make the token available to logging_middleware.Log() too,
        # since the Log API is also a protected route in some setups.
        import os
        os.environ["AFFORDMED_AUTH_TOKEN"] = _cached_token

        Log("backend", "info", "auth", "Successfully authenticated against Test Server and cached access token.")
        return _cached_token
    except requests.exceptions.RequestException as exc:
        Log("backend", "fatal", "auth", f"Authentication against Test Server failed: {exc}")
        raise


def auth_headers() -> dict:
    """Convenience helper returning the Authorization header dict."""
    return {"Authorization": f"Bearer {get_token()}"}
