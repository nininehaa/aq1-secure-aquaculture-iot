# Troubleshooting Log

This document records problems found during implementation, how they were investigated, and how they were resolved. It is intended to show the practical development process rather than only the final working result.

## T01 — Mosquitto port 1883 already in use

**Problem**

Starting Mosquitto manually produced a socket error indicating that the address/port was already in use.

**Investigation**

The team checked the MQTT listener with:

```powershell
Get-NetTCPConnection -LocalPort 1883 -State Listen
```

**Finding**

A Mosquitto process was already listening on port `1883`. The error occurred because a second broker instance was being started on the same port.

**Resolution**

The existing broker was used instead of launching another instance.

**Lesson**

Check the active process/listener before restarting network services.

---

## T02 — Temperature sensor reported missing MQTT username

**Problem**

The secure temperature sensor stopped at startup because `AQ1_MQTT_USERNAME` was not configured.

**Cause**

The MQTT credentials are intentionally loaded from environment variables. A new PowerShell terminal did not contain the variables from the previous terminal session.

**Resolution**

The MQTT username and password were loaded in the same PowerShell terminal before starting the sensor.

**Lesson**

Environment variables used for the current demo must be configured in each new terminal session unless a persistent configuration method is introduced later.

---

## T03 — MQTT password variable was empty

**Problem**

A configuration check displayed:

`Password loaded: False`

**Cause**

The secure password had been requested but had not been converted and assigned to `AQ1_MQTT_PASSWORD` in that PowerShell session.

**Resolution**

The password was re-entered with `Read-Host -AsSecureString`, converted for the process environment, and the variable was checked without printing the password value.

**Lesson**

Verify that a secret is present without exposing the secret itself.

---

## T04 — Sensor lost connection to MQTT broker

**Problem**

The temperature sensor later reported that message publishing failed because the MQTT client was not currently connected.

**Investigation**

The broker process and listener state were checked first rather than changing the Python code.

**Resolution approach**

1. Stop the disconnected sensor process.
2. Confirm Mosquitto is listening on port `1883`.
3. Reload the required environment variables in a clean terminal.
4. Restart the sensor and confirm authenticated connection and repeated publishes.

**Lesson**

A runtime connection failure does not automatically mean the sensor code is wrong. Check the broker and connection state first.

---

## T05 — Secure broker and monitor authentication dependency

**Problem**

The current monitoring script verifies HMAC values, but its MQTT client does not yet supply username/password credentials when connecting.

**Impact**

With anonymous access disabled on the secure broker, the monitor needs its own authenticated connection before the complete secure end-to-end path is fully clean.

**Current status**

Documented as an integration task rather than hidden as a completed feature.

**Planned resolution**

Add dedicated monitor credentials and later topic-level permissions so the monitor can subscribe only to the topics it requires.

---

## T06 — Localhost design is too small for final project scale

**Problem**

The original implementation placed the sensor, broker and monitoring services mainly on one computer using localhost.

**Feedback/Impact**

This is useful for proving individual security functions but does not represent a realistic multi-site farm network.

**Resolution direction**

The team selected GNS3 as the next deployment layer. The working localhost prototype will be moved onto separate virtual nodes and network segments rather than discarded.

**First GNS3 milestone**

```text
TEMP-001 -> Pond A network -> Router/Firewall -> Mosquitto -> Monitoring
```
