# AQ-1 Team Roles and Technical Collaboration

**Project:** AQ-1 Secure and Resilient IoT Sensor-Control System  
**Client:** Coral Coast Aquaculture  
**Course:** COIT13236 Cyber Security Project  
**Team Members:** Sahil Basnet, Neha Thanait and Md Monirul Haque Arnob

## 1. Purpose

This document outlines the technical involvement, responsibilities and collaborative work of the AQ-1 project team.

The project was developed jointly by all three members, who contributed to different aspects of planning, implementation, configuration, troubleshooting, testing and integration.

Although the team members had particular areas of technical focus, the project was not developed as three isolated components. The team worked together to integrate the sensor systems, GNS3 environment, security gateway and Node-RED dashboard into a functioning cybersecurity demonstration.

## 2. Project Overview

AQ-1 demonstrates how cybersecurity controls can protect IoT sensor data used in aquaculture monitoring.

The final system integrates:

- Simulated dissolved oxygen (DO) sensor readings in GNS3.
- Simulated pH sensor readings in GNS3.
- A physical DS18B20 temperature sensor connected to an ESP32-C3.
- HiveMQ for transmitting physical temperature readings.
- A GNS3 network environment and Python security gateway.
- HMAC-SHA256 message verification and replay protection.
- Controlled spoofing, tampering and replay attack demonstrations.
- A Node-RED dashboard for monitoring and visualisation.
- Logical NORMAL and SAFE/HOLD control states.

The project demonstrates cybersecurity monitoring and software-based control responses. Physical pump, aerator or relay operation was not implemented.

## 3. Sahil Basnet — Sensor Communication, Network Security and Integration

Sahil's technical focus included sensor communication, MQTT, network security, hardware integration and GNS3 development.

His areas of involvement included:

- Developing and testing sensor-message communication.
- Configuring and troubleshooting MQTT communication.
- Working with HMAC-SHA256 message generation and validation.
- Participating in GNS3 setup, network configuration and connectivity testing.
- Working on sensor-to-gateway communication.
- Developing and testing the physical ESP32-C3 temperature-sensing component with Neha.
- Configuring Arduino IDE and testing physical sensor measurements.
- Integrating HiveMQ communication with the GNS3 environment.
- Supporting cybersecurity attack testing and gateway integration.
- Participating in final system troubleshooting and demonstration preparation.

Sahil's work contributed to establishing reliable communication between sensor components and the security gateway, as well as integrating physical IoT hardware with the virtual environment.

## 4. Neha Thanait — Security Monitoring, Sensor Integration and Testing

Neha's technical focus included sensor-data security, monitoring, HMAC verification, availability checking, physical IoT integration and GNS3 development.

Her areas of involvement included:

- Developing and testing sensor-monitoring functionality.
- Working with HMAC-SHA256 message verification.
- Testing acceptance and rejection of sensor readings.
- Implementing and evaluating sensor outage and recovery detection.
- Working on security logging and alert generation.
- Participating in GNS3 configuration and virtual network troubleshooting.
- Working on gateway communication and system integration.
- Developing and testing the physical ESP32-C3 temperature-sensing component with Sahil.
- Testing physical temperature communication through HiveMQ.
- Participating in spoofing, tampering and replay demonstrations.
- Supporting Node-RED integration, testing and project documentation.

Neha's work contributed to the security-validation and monitoring aspects of the project and helped connect the physical sensor implementation with the broader GNS3 system.

## 5. Md Monirul Haque Arnob — GNS3 Development, Dashboard and Control Integration

Arnob's technical focus included GNS3 network development, system integration, cybersecurity monitoring, Node-RED dashboard development and logical control behaviour.

His areas of involvement included:

- Developing and configuring the GNS3 virtual environment.
- Working on virtual nodes, network connectivity and service communication.
- Troubleshooting GNS3 virtual machine and networking issues.
- Participating in sensor and security-gateway integration.
- Working with MQTT communication and sensor-data processing.
- Developing and configuring the Node-RED dashboard.
- Integrating monitoring information and security events into the dashboard.
- Working on logical NORMAL and SAFE/HOLD control states.
- Participating in cybersecurity verification and attack demonstrations.
- Collaborating on system testing, troubleshooting and showcase preparation.

Arnob's work contributed to the GNS3 infrastructure, dashboard visualisation and logical supervisory control components of the integrated project.

### Individual Contribution Summary

| Team member | Contribution | Main technical responsibilities |
|---|---|---|
| Sahil Basnet | 33.33% | Sensor development, MQTT communication, network configuration and physical ESP32-C3 temperature sensor integration |
| Neha Thanait | 33.33% | Security monitoring, HMAC verification testing, sensor outage detection, logging and integration testing |
| Md Monirul Haque Arnob | 33.34% | GNS3 environment, gateway verification, Node-RED dashboard, security testing and logical SAFE/HOLD integration |

The contribution percentages follow the submitted final report. Sensor integration, troubleshooting and final demonstration preparation also involved collaboration between team members.

## 6. Team Responsibilities and Collaboration

AQ-1 was developed collaboratively by Sahil Basnet, Neha Thanait and Md Monirul Haque Arnob.

Each member had areas of technical focus, but the implementation required regular collaboration, shared troubleshooting, testing and integration.

| Technical area | Team involvement |
|---|---|
| Project planning and architecture | All three members |
| Sensor development and MQTT communication | Collaborative development and integration |
| Physical ESP32-C3 temperature sensor | Sahil and Neha, with team integration |
| GNS3 network environment | All three members, with significant development and integration by Arnob |
| Security gateway and message verification | Collaborative development, troubleshooting and validation |
| HMAC-SHA256 and replay protection | Shared security development and testing |
| Spoofing, tampering and replay demonstrations | All three members |
| Sensor monitoring and security alerts | Collaborative development and integration |
| Node-RED dashboard | Arnob's main focus, with team integration and testing |
| Logical NORMAL and SAFE/HOLD states | Shared control integration and validation |
| System testing and troubleshooting | All three members |
| Documentation and project management | Shared team responsibility |
| Final presentation and demonstration | Collaborative preparation and delivery |

The team's GitHub repository was used as a shared development workspace. Files and commits represent project activity and do not necessarily indicate exclusive ownership of the work by the person who uploaded them.

Throughout development, members contributed through programming, configuration, debugging, testing, research, integration and documentation.

## 7. Integrated System Architecture

The team's work was combined into a single cybersecurity demonstration environment.

```text
       Physical DS18B20 Temperature Sensor
                       |
                    ESP32-C3
                       |
                       v
                 HiveMQ Broker
                       |
                       v
                GNS3 Gateway <--- Simulated DO Sensor
                       ^      <--- Simulated pH Sensor
                       |
                 Attacker Node
                       |
                       v
               Security Verification
               - HMAC validation
               - Sensor identity checks
               - Replay detection
               - Availability monitoring
                       |
                       v
              Verified Sensor Data
               and Security Events
                       |
                       v
                Node-RED Dashboard
                       |
                       v
             Logical NORMAL / SAFE/HOLD
```

The physical ESP32-C3 temperature sensor sends real measurements through HiveMQ to the security gateway in the GNS3 environment.

Simulated dissolved oxygen and pH sensors provide additional data within the virtual network.

The attacker node is used to demonstrate spoofing, tampering and replay attacks.

The gateway processes incoming messages and applies security checks before the information is treated as trusted.

The Node-RED dashboard displays relevant monitoring and security information.

## 8. Collaborative Development Process

The team worked together throughout the development and integration process.

### Planning and Design

The team reviewed project requirements, discussed technical approaches and developed the architecture.

The implementation evolved from an initial Python and MQTT prototype into a larger GNS3 environment with physical sensor integration.

### System Implementation

Team members worked across different technical components, including Python scripts, MQTT communication, GNS3 nodes, security verification, ESP32-C3 hardware and Node-RED.

### Integration and Troubleshooting

Integration required resolving issues involving virtual machines, network adapters, MQTT connections, sensor-message formats, physical device communication and dashboard integration.

Members assisted one another when technical challenges affected the overall system.

### Security Testing

The team tested legitimate communication and controlled spoofing, tampering and replay scenarios.

The tests helped demonstrate how the gateway responds to invalid or previously processed sensor information.

### Final Demonstration

The team brought the project components together to demonstrate the virtual aquaculture environment, physical sensor readings, security gateway, attacks and monitoring dashboard.

The final showcase represented the combined technical work of the team.

## 9. Challenges and Learning Outcomes

### Networking and Virtualisation

Working with GNS3 provided experience in configuring virtual networks, troubleshooting connectivity and integrating communication services.

### IoT Hardware Integration

Using the ESP32-C3 and DS18B20 sensor provided practical experience in programming a physical IoT device and transmitting measurements through MQTT.

### Cybersecurity Implementation

Implementing HMAC verification and testing spoofing, tampering and replay attacks helped the team understand the need for trustworthy sensor information.

### Dashboard and Control Integration

Integrating Node-RED and logical SAFE/HOLD states demonstrated how security decisions and monitoring events can be presented to users.

### Teamwork and Problem-Solving

The team learned that successful integration requires communication, shared troubleshooting and testing across different technical areas.

## 10. Team Outcome

The AQ-1 project demonstrates the integration of network simulation, physical IoT hardware, secure sensor communication, cybersecurity verification and monitoring visualisation.

All three team members contributed to the project's technical development and integration through their respective areas of focus and collaborative work.

The final system demonstrates how HMAC verification, replay protection, sensor availability monitoring and logical control responses can help reduce the risks associated with unreliable sensor information in an aquaculture environment.

The project reflects a collaborative approach in which different technical components were developed, tested and integrated into a shared cybersecurity solution.
