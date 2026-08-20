# Local Demo Setup Guide

## Purpose

This guide explains how to reproduce the current local AQ-1 MQTT security demonstration.

It covers the working temperature-sensor path only. GNS3 deployment will be documented separately when implemented.

## Required Software

- Python 3
- `paho-mqtt` Python package
- Eclipse Mosquitto MQTT broker and client tools
- PowerShell
- Git

## Repository

Clone or update the project repository, then work from the repository root.

The main files used in the current demo are:

- `scripts/sensors/temperature_sensor.py`
- `scripts/security/temperature_tamper_test.py`
- `scripts/monitoring/monitor.py`
- `configs/mosquitto/mosquitto.conf`

## Secrets and Credentials

Do not store the MQTT password or HMAC secret in GitHub.

The temperature sensor expects these environment variables:

- `AQ1_MQTT_USERNAME`
- `AQ1_MQTT_PASSWORD`
- `AQ1_TEMP_HMAC_KEY`

Use the MQTT account configured locally for `TEMP-001` and the agreed project HMAC secret.

## Step 1 — Confirm Broker Status

The current local broker uses MQTT port `1883`.

Check whether something is already listening:

```powershell
Get-NetTCPConnection -LocalPort 1883 -State Listen
```

If Mosquitto is already running, do not start a second instance on the same port.

## Step 2 — Configure the Temperature Sensor Terminal

In the same PowerShell terminal that will run the sensor, set the username:

```powershell
$env:AQ1_MQTT_USERNAME="TEMP-001"
```

Enter the MQTT password without printing it:

```powershell
$secure = Read-Host "Enter TEMP-001 MQTT password" -AsSecureString
$bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
$env:AQ1_MQTT_PASSWORD = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)
[Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)
```

Set the project HMAC key locally:

```powershell
$env:AQ1_TEMP_HMAC_KEY="<agreed-project-hmac-secret>"
```

Confirm variables are present without displaying the secrets:

```powershell
Write-Host "Username:" $env:AQ1_MQTT_USERNAME
Write-Host "Password loaded:" (-not [string]::IsNullOrEmpty($env:AQ1_MQTT_PASSWORD))
Write-Host "HMAC loaded:" (-not [string]::IsNullOrEmpty($env:AQ1_TEMP_HMAC_KEY))
```

## Step 3 — Run the Temperature Sensor

From the repository root:

```powershell
python .\scripts\sensors\temperature_sensor.py
```

Expected behaviour:

- MQTT authentication succeeds
- the client connects to Mosquitto
- a temperature reading is generated approximately every five seconds
- an HMAC-SHA256 value is shown
- `SECURE READING PUBLISHED` is displayed

## Step 4 — Run an Authorised Subscriber

Open a separate PowerShell terminal and configure the MQTT username/password again for that terminal.

Subscribe to the current temperature topic:

```powershell
& "C:\Program Files\mosquitto\mosquitto_sub.exe" `
-h localhost `
-p 1883 `
-t "aq1/pond1/temperature" `
-u $env:AQ1_MQTT_USERNAME `
-P $env:AQ1_MQTT_PASSWORD `
-v
```

Expected result:

Live JSON temperature messages are received.

## Step 5 — Test Unauthorised Access

Open another terminal and deliberately connect without MQTT credentials:

```powershell
& "C:\Program Files\mosquitto\mosquitto_sub.exe" `
-h localhost `
-p 1883 `
-t "aq1/pond1/temperature" `
-v
```

Expected result:

`Connection Refused: not authorised`

This is the evidence for the negative MQTT authentication test.

## Step 6 — Controlled Temperature Tamper Test

The tamper test uses the same local MQTT credentials and HMAC key as the legitimate temperature producer.

Run:

```powershell
python .\scripts\security\temperature_tamper_test.py
```

The script signs an original temperature reading, changes the value and status after signing, and publishes the modified payload with the old HMAC.

Expected monitoring result:

The verifier rejects the message because HMAC verification fails.

## Demo Terminal Meaning

- Terminal 1 — temperature sensor: generates and publishes readings.
- Terminal 2 — authorised subscriber: proves readings were received.
- Terminal 3 — broker/status: proves Mosquitto is listening on port 1883.
- Terminal 4 — unauthorised test: proves a no-credential client is rejected.

## Known Integration Note

The current monitoring script still needs dedicated MQTT credentials for the fully authenticated broker configuration. This is documented as remaining integration work rather than treated as complete.
