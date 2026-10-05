import json
import os
import urllib.error
import urllib.request

BASE_URL = os.getenv("AQ1_AZURE_DASHBOARD_URL", "").rstrip("/")
TOKEN = os.getenv("AQ1_DASHBOARD_TOKEN", "")


def configured():
    return bool(BASE_URL and TOKEN)


def _post(path, payload, timeout=3):
    if not configured():
        return False

    headers = {
        "Content-Type": "application/json",
        "X-AQ1-Token": TOKEN,
    }
    request = urllib.request.Request(
        BASE_URL + path,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return 200 <= response.status < 300
    except (urllib.error.URLError, TimeoutError, OSError):
        return False


def send_physical_verified(payload):
    data = dict(payload)
    data["verified"] = True
    return _post("/api/physical-telemetry", data)


def send_controller_state(state, reason, timestamp=None):
    return _post(
        "/api/controller",
        {
            "state": state,
            "reason": reason,
            "timestamp": timestamp,
        },
    )


def send_security_event(event, sensor_id=None, reason=None, source="PHYSICAL"):
    return _post(
        "/api/security-event",
        {
            "event": event,
            "sensor_id": sensor_id,
            "reason": reason,
            "source": source,
        },
    )
