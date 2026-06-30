"""
Centralized configuration. All values are read from environment variables
so no secrets are hard-coded in source.
"""

import os

EVALUATION_BASE_URL = os.environ.get(
    "EVALUATION_BASE_URL", "http://4.224.186.213/evaluation-service"
)

DEPOTS_ENDPOINT = f"{EVALUATION_BASE_URL}/depots"
VEHICLES_ENDPOINT = f"{EVALUATION_BASE_URL}/vehicles"
AUTH_ENDPOINT = f"{EVALUATION_BASE_URL}/auth"
LOGS_ENDPOINT = f"{EVALUATION_BASE_URL}/logs"

# Registration credentials - set these via environment variables, never commit them.
REG_EMAIL = os.environ.get("REG_EMAIL", "")
REG_NAME = os.environ.get("REG_NAME", "")
REG_ROLL_NO = os.environ.get("REG_ROLL_NO", "")
REG_ACCESS_CODE = os.environ.get("REG_ACCESS_CODE", "")
REG_CLIENT_ID = os.environ.get("REG_CLIENT_ID", "")
REG_CLIENT_SECRET = os.environ.get("REG_CLIENT_SECRET", "")

APP_HOST = os.environ.get("APP_HOST", "0.0.0.0")
APP_PORT = int(os.environ.get("APP_PORT", "8000"))
