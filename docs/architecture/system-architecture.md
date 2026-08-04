# Initial System Architecture

## Project
Secure and Resilient IoT Sensor-Control System for Coral Coast Aquaculture

## Purpose
The proposed system will securely collect and monitor simulated aquaculture
sensor readings. It will protect sensor identity, message integrity and
service availability.

## Main Components

### 1. Sensor Simulators
Python programs will simulate:

- Dissolved-oxygen sensor
- Temperature sensor
- pH sensor

Each sensor will periodically generate and publish a reading.

### 2. MQTT Broker
The Mosquitto MQTT broker will act as the communication gateway between the
sensor simulators and the monitoring system.

The broker will later be configured to:

- Authenticate authorised sensors
- Reject unauthorised connections
- Apply topic access-control rules
- Record connection and security events

### 3. Node-RED
Node-RED will receive sensor readings from the MQTT broker.

It will provide:

- Sensor-data processing
- Monitoring logic
- Sensor-outage detection
- Alerts
- Fail-safe control behaviour

### 4. Monitoring Dashboard
The dashboard will display:

- Current sensor readings
- Sensor online or offline status
- Security alerts
- Outage alerts
- Fail-safe system status

## Proposed Data Flow

Authorised Python sensor  
→ MQTT message  
→ Mosquitto broker  
→ Node-RED processing  
→ Dashboard, logs and alerts

## Security Flow

1. A sensor attempts to connect to the MQTT broker.
2. The broker checks the sensor credentials.
3. An authorised sensor is permitted to publish.
4. An unauthorised sensor is rejected.
5. Node-RED verifies and processes accepted readings.
6. Suspicious or missing readings generate alerts.
7. The control process remains in a safe state when data is unreliable.

## Initial Technology Stack

- Python
- Eclipse Mosquitto MQTT
- Node-RED
- GitHub
- GitHub Projects
- Microsoft Teams
- Wireshark
