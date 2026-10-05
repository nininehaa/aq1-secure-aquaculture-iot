# AQ-1 Azure Remote Dashboard

Architecture: Sensor/Emulator -> Pond Gateway -> MQTT -> Security Monitor -> local SAFE/HOLD; verified telemetry is forwarded over HTTPS to this Azure dashboard.

App Service settings:
- AQ1_DASHBOARD_TOKEN = random secret
- AQ1_OFFLINE_SECONDS = 12

Startup command if needed: `gunicorn --bind=0.0.0.0:8000 --timeout 120 app:app`

Test: set AQ1_AZURE_DASHBOARD_URL and AQ1_DASHBOARD_TOKEN locally, then run `python demo_injector.py`.

Integration: copy `azure_sender.py` beside the local security monitor. Only call `send_verified_telemetry(payload)` after the monitor has accepted a reading. Send controller state and security events with the other helper functions.
