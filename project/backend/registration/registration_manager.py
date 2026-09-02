"""
Registration Manager

Handles persistence of confirmed registrations to a JSON file.
Creates the file automatically if it does not exist.
"""
import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRATIONS_PATH = os.path.join(BASE_DIR, "data", "registrations.json")


def _ensure_file():
    """Create the registrations JSON file if it does not exist."""
    os.makedirs(os.path.dirname(REGISTRATIONS_PATH), exist_ok=True)
    if not os.path.exists(REGISTRATIONS_PATH):
        with open(REGISTRATIONS_PATH, "w", encoding="utf-8") as f:
            json.dump([], f)


def load_registrations() -> list:
    """Load all registrations from the JSON file."""
    _ensure_file()
    try:
        with open(REGISTRATIONS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, OSError):
        return []


def save_registration(registration: dict) -> dict:
    """
    Save a confirmed registration. Assigns an auto-incremented id and a timestamp.
    Returns the saved record.
    """
    _ensure_file()
    registrations = load_registrations()

    next_id = 1
    if registrations:
        next_id = max(r.get("id", 0) for r in registrations) + 1

    record = {
        "id": next_id,
        "name": registration.get("name", ""),
        "email": registration.get("email", ""),
        "field": registration.get("field", ""),
        "experience": registration.get("experience", ""),
        "registered_at": datetime.utcnow().isoformat() + "Z",
    }

    registrations.append(record)

    try:
        with open(REGISTRATIONS_PATH, "w", encoding="utf-8") as f:
            json.dump(registrations, f, indent=2)
    except OSError as e:
        raise RuntimeError(f"Could not save registration: {e}")

    return record


def find_by_email(email: str) -> dict | None:
    """Find a registration by email address (case-insensitive)."""
    if not email:
        return None
    registrations = load_registrations()
    for r in registrations:
        if r.get("email", "").lower() == email.lower():
            return r
    return None
