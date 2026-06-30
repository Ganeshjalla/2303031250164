"""
Allowed values for the Test Server's Log API.
All values are lower case only, per the API contract.
"""

VALID_STACKS = {"backend", "frontend"}

VALID_LEVELS = {"debug", "info", "warn", "error", "fatal"}

# Packages restricted to backend applications
BACKEND_ONLY_PACKAGES = {
    "cache",
    "controller",
    "cron_job",
    "db",
    "domain",
    "handler",
    "repository",
    "route",
    "service",
}

# Packages restricted to frontend applications
FRONTEND_ONLY_PACKAGES = {
    "api",
    "component",
    "hook",
    "page",
    "state",
    "style",
}

# Packages usable in either stack
SHARED_PACKAGES = {
    "auth",
    "config",
    "middleware",
    "utils",
}

ALL_PACKAGES = BACKEND_ONLY_PACKAGES | FRONTEND_ONLY_PACKAGES | SHARED_PACKAGES
