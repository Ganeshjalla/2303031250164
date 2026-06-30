# Logging Middleware

A reusable Python package that sends structured logs to the Test Server's Log API.

## Install (within this repo, in editable mode)

```bash
pip install -e ./logging_middleware
```

## Configuration

Set these environment variables before your app starts (e.g. in a `.env` file
loaded by `python-dotenv`, or exported in your shell):

```bash
export LOG_API_URL="http://4.224.186.213/evaluation-service/logs"
export LOG_API_AUTH_TOKEN="<bearer token from the Auth API>"
```

## Usage

```python
from logging_middleware import Log

# Successful operation
Log("backend", "info", "service", "Vehicle scheduling computed for depot 3, 12 tasks selected")

# Error in a handler due to a data type mismatch
Log("backend", "error", "handler", "received string, expected bool")

# Fatal DB failure
Log("backend", "fatal", "db", "Critical database connection failure.")
```

`Log()` validates `stack`, `level`, and `package` against the values allowed
by the API contract (including which packages are backend-only vs.
frontend-only) before sending the request, and never raises on a network or
API failure — failures are written to stderr so a logging outage can't take
down the calling application.

## Files

- `logging_middleware/constants.py` — allowed values for stack/level/package
- `logging_middleware/logger.py` — the `Log()` function and validation logic
- `logging_middleware/__init__.py` — public package API
