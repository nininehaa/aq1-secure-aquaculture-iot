# Stage 1: System Requirements and Assumptions 

## 1.1 System purpose 

‑ AQ 1 will be designed as a secure aquaculture monitoring and control system for Coral Coast Aquaculture. It will continuously monitor water temperature, dissolved oxygen and pH across three outdoor ponds. Verified readings will be displayed to farm personnel and used to support safe operation of aerators, pumps and feeding equipment. 

The university implementation will remain a simulated proof-of-concept. However, the proposed design will specify realistic commercial devices, network equipment, software, security controls and deployment arrangements. 

## 1.2 Operational environment 

The proposed system will operate across three outdoor ponds identified as Pond A, Pond B and Pond C. Each pond will have its own water-quality sensors and field equipment. A central control room will contain the MQTT, monitoring, dashboard and management systems. 

The equipment must tolerate outdoor conditions, moisture, dust, temperature changes, water exposure and possible corrosion. Pond-side equipment must therefore use weatherproof enclosures, suitable cabling and protected power connections. 

## 1.3 Functional requirements 

**FR-01:** The system shall measure water temperature in all three ponds. 

**FR-02:** The system shall measure dissolved oxygen in all three ponds. 

**FR-03:** The system shall measure pH in all three ponds. 

**FR-04:** Each reading shall identify its sensor, pond, measurement type, value, unit, status and timestamp. 

**FR-05:** Sensor readings shall be transmitted to a central MQTT service. 

**FR-06:** The monitoring system shall verify each reading before accepting it as trusted. 

**FR-07:** Valid readings shall be recorded and displayed on a central dashboard. 

**FR-08:** Invalid, malformed, tampered or unauthorised readings shall be rejected and logged. 

**FR-09:** The system shall alert operators when measurements leave approved operating ranges. 

**FR-10:** The system shall detect sensor, gateway and communication outages. 

**FR-11:** The system shall support the automatic control of equipment such as aerators, pumps and feeders. 

**FR-12:** The system shall enter SAFE/HOLD mode when trustworthy sensor information is unavailable. 

**FR-13:** Authorised farm personnel shall be able to review current readings, historical data, alerts and equipment status. 

**FR-14:** The system shall provide an administrator website displaying current and historical readings, sensor availability, alerts, rejected messages, MQTT service status, equipment status and the current control state. 

**FR-15:** Authorised administrators shall be able to acknowledge alerts and manually activate SAFE/HOLD through the website. 

**FR-16:** The system shall record administrative actions, including the user identity, performed action, affected component and timestamp. 

**FR-17:** The university prototype shall simulate the three pond networks, sensors, gateways, MQTT services, monitoring system, controller and farm equipment within GNS3. 

**FR-18:** Simulated sensors shall normally generate and publish water-quality readings every 30 seconds. 

**FR-19:** The system shall maintain an independent last-valid-reading time for every expected sensor. 

**FR-20:** Invalid, tampered or replayed messages shall not update a sensor’s last-validreading time or prevent outage detection. 

**FR-21:** The system shall support the controlled simulation of unauthorised MQTT access, sensor spoofing, message tampering, replay attacks and sensor outages. 

**FR-22:** Following an outage or security event, the controller shall return from SAFE/HOLD only after the defined recovery conditions have been satisfied. 

**FR-23:** Loss of internet access, Azure connectivity or the administrator website shall not prevent local monitoring, outage detection or SAFE/HOLD operation. 

**FR-24:** Where Azure is included in the prototype, selected readings, alerts and systemstatus information shall be securely forwarded from the local system for remote viewing. 

## 1.4 Security requirements 

**SR-01:** Every sensor, gateway and authorised system component shall have a unique identity. 

**SR-02:** MQTT clients shall authenticate before connecting to the broker. 

**SR-03:** Sensor messages shall be protected against unauthorised modification. 

**SR-04:** AQ-1 shall use HMAC-SHA256 verification to identify tampered or spoofed readings. 

**SR-05:** MQTT and web communication shall use TLS encryption where supported by the selected prototype components. 

**SR-06:** MQTT access-control rules shall restrict each device to its approved topics and actions. 

**SR-07:** The system shall prevent old valid messages from being replayed as new readings. 

**SR-08:** Failed authentication attempts, rejected messages, detected outages and recovery events shall be logged. 

**SR-09:** The pond sensor, MQTT service, monitoring, management and Security/Test networks shall be logically separated. 

**SR-10:** The attacker/test system shall remain isolated from normal operational devices except through specifically authorised testing paths. 

**SR-11:** The administrator website shall require authenticated user access. 

**SR-12:** Administrative permissions shall be separated from sensor-publishing and routine monitoring permissions. 

**SR-13:** Passwords, MQTT credentials, HMAC secrets and private cryptographic keys shall not be hard-coded in publicly accessible source code. 

**SR-14:** Sensor messages shall contain a timestamp, sequence number or equivalent freshness value to support replay detection. 

**SR-15:** Before accepting a message, the security monitor shall validate its structure, sensor identity, authorised MQTT topic, freshness and HMAC. 

**SR-16:** Administrative actions and security-relevant events shall be stored in an audit log. 

**SR-17:** Where Azure is included, communication between the local system and Azure shall use an authenticated and encrypted connection. 

**SR-18:** The Azure-hosted component shall not directly control safety-critical farm equipment in the initial design. 

**SR-19:** Firewall rules shall restrict communication between the pond, MQTT service, monitoring, management and Security/Test networks. 

**SR-20:** Security testing shall be performed only against the team’s authorised and isolated GNS3 environment. 

## 1.5 Safety and availability requirements 

‑ AQ 1 must not continue normal automatic operation using missing, outdated or unverified data. If an essential sensor becomes unavailable, the monitoring system shall raise an alert and instruct the controller to enter a predefined SAFE/HOLD state. 

<mark>One abnormal reading should not immediately cause unsafe equipment activity.</mark> Important control decisions should consider <mark>validation, appropriate thresholds and consecutive readings</mark> . Manual operator control must remain available for authorised farm personnel. 

The design shall also consider backup power, local operation during internet failure, MQTT service recovery and safe reboot behaviour. 

## 1.6 Design assumptions 

The initial design assumes that each pond requires temperature, dissolved oxygen and pH monitoring. All ponds will use the same standard sensor-node design unless different species or pond conditions require different equipment. 

The control room is assumed to be located within the farm and connected to pond-side equipment through a private farm network. Internet access may support remote monitoring, but essential local monitoring and safe control should not depend entirely on an external cloud service. 

Commercially suitable equipment will be selected using a realistic mid-range budget. Devices must be available products with published specifications and environmental rating <mark>s. Hobby components may be used in the university demonstration but will not automatically be recommended for permanent deployment.</mark> 

## 1.7 Current project boundaries 

‑ AQ 1 will design and demonstrate monitoring, message verification, security alerts, outage detection and safe-state logic. The project will not physically construct three commercial ponds, install industrial electrical systems or directly operate real farm machinery. 

The final design will include proposed devices, quantities, connections, network architecture, software architecture, security controls, control behaviour, estimated costs and supporting documentation. 

## 1.8 Reference farm layout and measurements 

For design purposes, Coral Coast Aquaculture will be represented as a fictional medium-sized pilot farm containing three outdoor production ponds. The dimensions and distances used in this document are design assumptions rather than measurements taken from an existing farm. Figure 1 presents a simplified bird’s-eye view of the proposed reference farm, including the ponds, monitoring stations, gateways, control room and assumed distances. 

Pond A and Pond B will be used for prawn production, while Pond C will be used for barramundi production. All three ponds will measure approximately 50 metres by 30 metres, with an average water depth of 1.5 metres. Using identical pond dimensions provides a consistent basis for designing and comparing the monitoring equipment required for each pond. 

The maximum distance between pond infrastructure and the central control room is assumed to be approximately 200 metres. The greatest separation between individual pond areas is assumed to be approximately 150 metres. These distances will guide the later selection of cabling, wireless communication technologies, gateways and network equipment. 

Each pond will contain two water-quality monitoring stations. One station will be positioned near the water inlet or pond boundary, while the second will be positioned closer to the centre or aeration area. <mark>This arrangement will provide more representative measurements than relying on a single monitoring location.</mark> 

Each monitoring station will measure temperature, dissolved oxygen and pH. The complete reference farm will therefore contain six temperature measurement points, six dissolved-oxygen measurement points and six pH measurement points <mark>. Each pond will also have a dedicated pond gateway responsible for collecting or forwarding its sensor data to the central system.</mark> 



<!-- Start of picture text -->
AQ-1 REFERENCE AQUACULTURE FARM<br>Simplified bird's-eye site plan — all dimensions are design assumptions<br>O-~0=|ER~0——~0= EE =0=—o= 5<br>LAYOUT KEY CENTRAL CONTROL ROOM<br>@ Monitoring station: temperature + DO + pH [|<br>tu Dedicated pond gateway Q onitoring» Database<br>--Total: 6Privatestations +farm18 measurement communication points path+ 3 gateways<br><!-- End of picture text -->

The attacker/test node will be used only within the isolated GNS3 environment. It will generate controlled test conditions such as unauthorised MQTT connections, spoofed sensor identities, tampered readings, replayed messages and attempted access to restricted networks. These activities will demonstrate whether the proposed security controls behave as intended. 

GNS3 will simulate the system’s network and software behaviour rather than the physical chemistry of the pond or the electrical operation of real farm equipment. Aerators, pumps and feeders will therefore be represented through virtual states, messages or simple software indicators. 

## 1.10 Administrative website 

‑ AQ 1 will include a simple web-based interface through which authorised administrators can access essential monitoring and security information. The website will initially be developed as a prototype and hosted locally within the simulated farm management network. 

The website will display the latest temperature, dissolved-oxygen and pH readings for each pond. It will also show sensor availability, last valid reading time, pond condition, active alerts, rejected messages, MQTT service status and the current state of the SAFE/HOLD controller. 

Authorised administrators may be allowed to acknowledge alerts, review historical data, modify approved operating thresholds and manually place the system into SAFE/HOLD. Administrative actions that could affect system behaviour must require authentication and must be recorded in an audit log. 

The website must not accept raw sensor readings as trustworthy without verification. Information displayed as valid must first pass the system’s identity, structure, freshness and HMAC checks. 

## 1.11 Local and Azure deployment 

The primary prototype will operate locally so that monitoring and safe-state decisions remain available without an internet connection. The MQTT broker, security monitor, database, controller and administrator website may run on separate GNS3 nodes or on logically separated services within the simulated network. 

Microsoft Azure may be used later to demonstrate optional remote access or cloudbased monitoring. Selected readings, alerts and system status information may be forwarded securely from the local system to an Azure-hosted website or service. 

The cloud service will not be responsible for immediate safety-critical control decisions. Loss of Azure connectivity or farm internet access must not prevent local outage detection or SAFE/HOLD operation. Direct control of pumps, aerators or feeders 

from the public internet will remain outside the initial prototype unless an appropriately secured design is developed and authorised. 

## 1.12 System users and access 

‑ The primary users of AQ 1 will be farm operators and system administrators. Farm operators will require access to current pond conditions, alerts and equipment status. System administrators will require additional access to device status, security events, system configuration, user management and diagnostic information. 

<mark>The attacker/test user will represent an unauthorised or potentially malicious device during controlled security testing. This user must not receive normal administrative access and must remain confned to the designated Security/Test network.</mark> 

Access permissions will follow the principle of least privilege. Users and devices will receive only the permissions required for their assigned functions. Administrative access must be separated from sensor publishing permissions and routine monitoring access. 

## 1.13 Design constraints 

The project is limited by the absence of a physical farm, industrial sensors and real control equipment. Consequently, sensor values, equipment states, environmental events and failures will be simulated. The resulting prototype can demonstrate network communication and security logic, but it cannot confirm the long-term reliability of physical probes or machinery in an operating aquaculture environment. 

The design must remain achievable within the available project duration, team capacity and university computing resources. GNS3 performance may limit the number and complexity of virtual nodes that can operate simultaneously. Where necessary, one node may represent multiple closely related software services, provided that their logical roles remain clearly documented. 

The project must use legally and ethically controlled security testing. Simulated attacks will target only the team’s authorised GNS3 environment. No testing will be conducted against public systems, commercial farms or infrastructure belonging to other parties. 

Equipment prices and cloud-service costs may change over time. All estimated costs will therefore include the source, currency and date on which the estimate was recorded. 

## 1.14 Stage 1 completion statement 

Stage 1 establishes the purpose, operating environment, requirements, assumptions, reference farm dimensions, project boundaries and prototype approach for AQ‑1. The project will design a realistic system for three ponds while demonstrating its core 

networking, monitoring, cybersecurity and SAFE/HOLD behaviour through GNS3 and locally hosted software. 

These requirements and assumptions will guide the selection of temperature, dissolved-oxygen and pH equipment during the next design stages. They will also provide the basis for the farm network, MQTT infrastructure, administrative website, cybersecurity controls and control-system design. 

