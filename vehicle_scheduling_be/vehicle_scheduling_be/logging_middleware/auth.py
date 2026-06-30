"""
One-time helper to obtain the Bearer token from the Authentication API
and store it in the environment so logger.Log() can use it automatically.

Call this once at application startup (e.g. in main.py / app factory),
right after registration, using your saved clientID and clientSecret.
"""

import os
import requests

AUTH_API_URL = "http://4.224.186.213/evaluation-service/auth"


def fetch_and_set_auth_token(email: str, name: str, roll_no: str,
                              access_code: str, client_id: str,
                              client_secret: str) -> str:
    """
    Calls the Authentication API and stores the access_token in the
    AFFORDMED_AUTH_TOKEN environment variable for use by Log().

    Returns the access token string.
    """
    payload = {
        "email": email,
        "name": name,
        "rollNo": roll_no,
        "accessCode": access_code,
        "clientID": client_id,
        "clientSecret": client_secret,
    }

    resp = requests.post(AUTH_API_URL, json=payload, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    token = data["access_token"]
    os.environ["AFFORDMED_AUTH_TOKEN"] = token
    return token
