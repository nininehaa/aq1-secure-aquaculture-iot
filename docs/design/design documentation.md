# Logical Network Design

## Design Overview

The AQ-1 logical network design presents the proposed secure and resilient IoT infrastructure for Coral Coast Aquaculture. The system collects simulated dissolved oxygen, temperature and pH readings from multiple pond networks. These readings are transferred through a segmented network to MQTT brokers, where they become available to the security monitoring, logging, dashboard and control components. The design aims to protect sensor identity, message integrity and system availability while preventing unreliable data from causing unsafe automated actions.

The architecture separates pond sensors, MQTT services, monitoring systems, management devices and security-testing equipment into different logical networks. This separation reduces unnecessary communication between components and allows firewall policies to control which devices and services can interact. The design also provides a foundation for implementing the system in GNS3, where the network paths, firewall rules and security controls can be demonstrated.

## Core Network Infrastructure

The WAN or Internet cloud represents connectivity outside the aquaculture network. External traffic first reaches the farm router, which connects the external network to the internal infrastructure and forwards traffic between the required network paths. Traffic then passes through the firewall before reaching the core switch.

The firewall protects the internal aquaculture environment by inspecting incoming and outgoing traffic. It should permit only approved communication and block unauthorised connection attempts. It can also restrict traffic between the Security/Test network and the operational networks. The core switch acts as the central distribution point and connects the pond, MQTT service, monitoring, management and security-testing networks.

## Pond Sensor Networks

The architecture contains three separate pond networks. Pond A uses the proposed `10.10.10.0/24` subnet, Pond B uses `10.10.20.0/24`, and Pond C uses `10.10.30.0/24`. Each pond is connected through its own access switch so that its sensor devices are logically separated from sensors located in other ponds.

Each pond contains dissolved oxygen, temperature and pH sensors. The dissolved oxygen sensors measure the oxygen concentration of the pond water, while the temperature sensors measure water temperature. The pH sensors measure whether the water is acidic, neutral or alkaline. These measurements are important because unsafe water conditions could negatively affect prawns and barramundi.

The sensors generate simulated readings and publish them through MQTT. Each message should include the sensor identity, pond identity, sensor type, measured value, timestamp and message-integrity information. HMAC-SHA256 is used to protect the relevant message fields so that the monitoring system can determine whether a reading has been modified after it was generated.

## MQTT Service Network

The MQTT service network contains the primary and backup MQTT brokers. The primary broker acts as the main communication service between the sensor producers and authorised subscribers. Sensors publish readings to their assigned MQTT topics, while the security monitor subscribes to those topics and receives the messages for validation.

The broker should require MQTT usernames and passwords so that anonymous clients cannot connect. Topic-level access-control rules should also restrict each sensor identity to its authorised topics. For example, a temperature sensor should not be allowed to publish messages as a dissolved oxygen sensor or send data to management topics.

The backup MQTT broker represents the resilience component of the proposed design. If the primary broker becomes unavailable, the backup broker could maintain the communication service or support a controlled recovery process. Broker failover is part of the target design and must be tested before it is described as fully implemented.

## Security Monitoring and Logging

The Monitoring network uses the proposed `10.10.60.0/24` subnet. It contains the security monitor and security log database. The security monitor receives messages from the MQTT service and validates them before treating the sensor data as trusted.

For every sensor message, the monitor reconstructs the protected message and calculates the expected HMAC using the appropriate shared secret. It compares the calculated HMAC with the signature included in the received message. A matching signature indicates that the protected fields have not been modified. A mismatched signature causes the message to be rejected and recorded as a security event.

The monitoring system also tracks the availability of every expected sensor independently. If a sensor stops providing valid readings for longer than the configured timeout, the system generates an outage alert. Invalid or tampered messages must not reset the availability timer because an attacker could otherwise use false traffic to hide a genuine sensor outage.

The security log database stores accepted readings, rejected messages, authentication failures, outage alerts and recovery events. These records provide evidence for testing and assist operators with understanding what happened during a security incident.

## Management Network and Dashboard

The Management network uses the proposed `10.10.50.0/24` subnet. It contains the Node-RED dashboard and an administrator workstation. The dashboard provides a visual interface through which authorised users can view current readings, sensor availability, security alerts and the state of the control system.

The administrator workstation is used to configure and manage authorised parts of the system. Access to this network should be restricted because an attacker who compromises a management device could change security settings or interfere with monitoring. Pond sensors and attacker devices should therefore not have unrestricted access to the Management network.

## Normal Trusted Data Flow

The blue dashed lines represent the normal trusted data flow. A sensor generates a reading and calculates its HMAC before publishing the message to the primary MQTT broker. The broker authenticates the MQTT client and forwards the message to authorised subscribers. The security monitor receives the message, verifies its structure, identity and HMAC, and then classifies the reading as trusted or rejected.

Trusted data can be sent to the Node-RED dashboard for display and to the SAFE/HOLD controller for operational decision-making. Raw sensor messages should not directly control equipment because they must first pass security and availability validation.

## Simulated Attack Flow

The attacker/test node is located in the isolated Security/Test network, which uses the proposed `10.10.70.0/24` subnet. The red path represents controlled attack traffic generated during project testing. This node can be used to attempt unauthorised MQTT connections, publish spoofed sensor messages, modify signed readings or replay previously valid messages.

The attacker should not be able to directly access operational or management systems. Its traffic must pass through the applicable network and security controls. An unauthenticated connection should be rejected by the MQTT broker, while a tampered message should fail HMAC verification at the security monitor. These attempts should also generate logs that can be preserved as project evidence.

## SAFE/HOLD Control Response

The SAFE/HOLD controller represents the safety-focused control component of the architecture. It consumes trusted status information from the monitoring system rather than accepting raw sensor readings directly. When the required sensor data is available and valid, the controller can maintain the normal operating state.

If a critical sensor becomes unavailable, a message fails verification or the system cannot confirm that its input is trustworthy, the controller enters or remains in the `SAFE/HOLD` state. In this state, potentially unsafe automatic actions are blocked. The controller may manage simulated equipment such as aerators, water pumps and feeders.

When trustworthy sensor readings recover, the controller should perform a controlled recovery instead of immediately resuming automatic operation. This behaviour ensures that temporary or malicious messages cannot cause repeated unsafe state changes.

## Network Security and Segmentation

The logical separation shown in the diagram enables the project to apply different security policies to different networks. Pond sensors should communicate with the MQTT service but should not have unrestricted access to the monitoring or management systems. The monitoring network should be able to subscribe to authorised MQTT topics, while the management network should be accessible only to approved administrative devices.

The Security/Test network should remain isolated from normal operations except for specifically authorised testing paths. Firewall rules, routing policies and MQTT access-control lists will be used to enforce these restrictions. Future TLS implementation can encrypt MQTT communication and reduce the risk of credentials or sensor readings being intercepted during transmission.

## Design Status

This diagram represents the complete target architecture rather than proof that every component has already been deployed. The current prototype includes sensor simulation, MQTT communication, HMAC-based integrity verification, tamper rejection and sensor outage monitoring. The complete GNS3 segmentation, pH sensors, backup-broker failover, Node-RED dashboard, topic ACLs, TLS and SAFE/HOLD integration must remain identified as planned or in progress until they have been implemented, tested and supported by evidence.
