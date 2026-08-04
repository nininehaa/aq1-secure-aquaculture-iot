# Project Overview

## Project Title
Secure and Resilient IoT Sensor-Control System for Coral Coast Aquaculture

## Client
Coral Coast Aquaculture

## Team Members
- Neha Thanait
- Sahil Basnet

## Project Scenario
AQ-1 — IoT/Sensor Security for a Prawn and Barramundi Farm

## Business Problem
Coral Coast Aquaculture uses sensors to monitor dissolved oxygen, water
temperature, pH levels and feeder activity.

False, modified or missing sensor readings could cause harmful automated
actions and result in the loss of prawn or barramundi stock.

## Project Aim
The aim of this project is to build and test a secure simulated aquaculture
IoT system that protects device identity, message integrity and sensor
availability.

## Minimum Viable Product
The project will include:

- Simulated dissolved-oxygen, temperature and pH sensors
- A secure sensor gateway
- Device authentication
- Integrity-protected sensor readings
- Monitoring and alerting
- Rejection of spoofed readings
- Detection of sensor outages
- Fail-safe control behaviour

## Proposed System Flow

Sensor simulators → MQTT broker → Node-RED → Monitoring dashboard and alerts

## Stretch Goals
- Redundant sensors
- Anomaly detection
- Certificate-based device identity
- Advanced fail-safe control logic
