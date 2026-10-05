from flask import Flask, jsonify, render_template, request
from datetime import datetime, timezone
import os
import time
import threading

app = Flask(__name__)

TOKEN = os.getenv("AQ1_DASHBOARD_TOKEN", "")
OFFLINE = int(os.getenv("AQ1_OFFLINE_SECONDS", "12"))
LOCK = threading.Lock()
EVENTS = []
CONTROLLER = {
    "state": "NORMAL",
    "reason": "Waiting for verified telemetry",
    "timestamp": None,
}

# Farm-scale GNS3 model: 3 ponds x 2 stations x 3 measurements = 18 streams.
SENSORS = {}
for pond in "ABC":
    for station in (1, 2):
        for prefix, stype, unit in (
            ("TEMP", "temperature", "C"),
            ("DO", "dissolved_oxygen", "mg/L"),
            ("PH", "ph", "pH"),
        ):
            sid = f"{prefix}-{pond}{station}"
            SENSORS[sid] = {
                "sensor_id": sid,
                "pond": pond,
                "station": f"{pond}{station}",
                "sensor_type": stype,
                "value": None,
                "unit": unit,
                "verified": False,
                "last": None,
                "last_iso": None,
            }

# Physical validation bench is deliberately separate from the 18 GNS3 streams.
PHYSICAL = {
    "TEMP-001": {
        "sensor_id": "TEMP-001",
        "device_id": "POND-A-ESP32-01",
        "source": "ESP32-C3 + DS18B20",
        "sensor_type": "temperature",
        "value": None,
        "unit": "C",
        "verified": False,
        "last": None,
        "last_iso": None,
    }
}


def now():
    return datetime.now(timezone.utc).isoformat()


def auth():
    return (not TOKEN) or request.headers.get("X-AQ1-Token", "") == TOKEN


def event(kind, **kw):
    with LOCK:
        EVENTS.insert(0, {"kind": kind, "time": now(), **kw})
        del EVENTS[100:]


def with_availability(item, current_time):
    x = dict(item)
    x["availability"] = (
        "ONLINE"
        if x.get("last") and current_time - x["last"] <= OFFLINE
        else "OFFLINE"
    )
    return x


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/api/state")
def state():
    current_time = time.time()
    with LOCK:
        sensors = [with_availability(s, current_time) for s in SENSORS.values()]
        physical = [with_availability(s, current_time) for s in PHYSICAL.values()]
        return jsonify(
            sensors=sensors,
            physical=physical,
            controller=dict(CONTROLLER),
            events=list(EVENTS[:30]),
            offline_seconds=OFFLINE,
        )


@app.post("/api/telemetry")
def telemetry():
    if not auth():
        return jsonify(error="unauthorised"), 401

    p = request.get_json(silent=True) or {}
    sid = str(p.get("sensor_id", "")).upper()

    if sid not in SENSORS:
        return jsonify(error="unknown farm sensor"), 400
    if p.get("verified") is not True:
        return jsonify(error="verified telemetry only"), 400

    s = SENSORS[sid]
    if p.get("sensor_type", s["sensor_type"]) != s["sensor_type"]:
        return jsonify(error="type mismatch"), 400

    with LOCK:
        s.update(
            value=p.get("value"),
            unit=p.get("unit", s["unit"]),
            verified=True,
            last=time.time(),
            last_iso=now(),
            message_status=p.get("status", "VERIFIED"),
            timestamp=p.get("timestamp"),
        )

    event(
        "VERIFIED_TELEMETRY",
        sensor_id=sid,
        source="GNS3",
        value=p.get("value"),
        unit=p.get("unit", s["unit"]),
    )
    return jsonify(accepted=True, sensor_id=sid)


@app.post("/api/physical-telemetry")
def physical_telemetry():
    if not auth():
        return jsonify(error="unauthorised"), 401

    p = request.get_json(silent=True) or {}
    sid = str(p.get("sensor_id", "")).upper()

    if sid not in PHYSICAL:
        return jsonify(error="unknown physical sensor"), 400
    if p.get("verified") is not True:
        return jsonify(error="verified telemetry only"), 400

    s = PHYSICAL[sid]
    if p.get("sensor_type", s["sensor_type"]) != s["sensor_type"]:
        return jsonify(error="type mismatch"), 400

    with LOCK:
        s.update(
            value=p.get("value"),
            unit=p.get("unit", s["unit"]),
            verified=True,
            last=time.time(),
            last_iso=now(),
            message_status=p.get("status", "VERIFIED"),
            timestamp=p.get("timestamp"),
            pond_id=p.get("pond_id"),
        )

    event(
        "PHYSICAL_VERIFIED",
        sensor_id=sid,
        source="ESP32-C3",
        value=p.get("value"),
        unit=p.get("unit", s["unit"]),
    )
    return jsonify(accepted=True, sensor_id=sid)


@app.post("/api/controller")
def controller():
    if not auth():
        return jsonify(error="unauthorised"), 401

    p = request.get_json(silent=True) or {}
    with LOCK:
        CONTROLLER.update(
            state=str(p.get("state", "UNKNOWN")).upper(),
            reason=str(p.get("reason", "")),
            timestamp=p.get("timestamp") or now(),
        )
    event(
        "CONTROLLER",
        state=CONTROLLER["state"],
        reason=CONTROLLER["reason"],
    )
    return jsonify(accepted=True)


@app.post("/api/security-event")
def security_event():
    if not auth():
        return jsonify(error="unauthorised"), 401

    p = request.get_json(silent=True) or {}
    event(
        "SECURITY_EVENT",
        sensor_id=p.get("sensor_id"),
        event=p.get("event"),
        reason=p.get("reason"),
        source=p.get("source"),
    )
    return jsonify(accepted=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
