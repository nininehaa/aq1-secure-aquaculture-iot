# Secure and Resilient IoT Sensor-Control System

## Client
Coral Coast Aquaculture

## Team Members
- Neha Thanait
- Sahil Basnet
- Md Monirul Haque Arnob

## Project Scenario
AQ-1 — IoT/Sensor Security for a Prawn and Barramundi Farm

## Project Overview
This project will build a simulated secure aquaculture IoT system. 
The system will monitor dissolved oxygen, temperature and pH readings.

The prototype will authenticate sensor devices, protect message integrity,
monitor sensor availability, reject spoofed readings and maintain a safe
control state when reliable sensor information is unavailable.

## Proposed Technologies

- Python sensor simulators
- Eclipse Mosquitto MQTT broker
- Python gateway and monitoring scripts
- HMAC-based message integrity
- GitHub and GitHub Projects
- Microsoft Teams
- Wireshark
- Docker/virtualisation if required

## Minimum Demonstration
1. An authorised sensor sends a valid reading.
2. The reading is accepted and displayed.
3. A spoofed reading is rejected.
4. A sensor outage is detected.
5. The control system remains in a safe state.
