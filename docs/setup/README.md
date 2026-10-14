**# AQ-1 Secure Aquaculture IoT — Team 2 Setup & Runbook**



**\*\*Deployment:\*\*** Team 2 (independent deployment)  

**\*\*Purpose:\*\*** Reproduce, start, validate, demonstrate and stop independent AQ-1 prototype.  

**\*\*Status:\*\*** Based on the Team 2 setup recorded during integration. Local paths, GNS3 container addresses, script versions and Node-RED exports must be checked on Team 2 PC before use.



\> **\*\*Important:\*\*** This is the **\*\*Team 2\*\*** runbook. The separately supplied \`flows (1).json\` uses Team 1 topics (\`aquaculture/...\`) and a Team 1-specific SQLite path. **\*\*Do not import it into Team 2 deployment without adapting the topics, database path and flows.\*\*** Use Team 2 Node-RED flow backup instead. The GitHub repository is a development source tree, not necessarily a complete image of Team 2 locally configured GNS3 containers.



**## 1. Architecture and responsibilities**



\| Component | Where it runs | Function |

\|---|---|---|

\| VMware Workstation Pro | Windows host | Runs the GNS3 VM |

\| GNS3 Desktop + GNS3 VM (previously 2.2.61) | Windows / VMware | Hosts virtual topology and Alpine Docker containers |

\| \`DO-001\` | GNS3 Alpine container | Simulated dissolved oxygen publisher |

\| \`PH-001\` | GNS3 Alpine container | Simulated pH publisher |

\| \`AQ1-Gateway\` | GNS3 Alpine container | Verifies HMAC and freshness/replay checks; emits verified data and events |

\| \`Attacker1\` | GNS3 Alpine container | Authorised attack test source; **\*\*do not start by default\*\*** |

\| Node-RED + FlowFuse Dashboard 2.0 | **\*\*Windows host\*\***, not a GNS3 VM | Monitoring, analytics, incident UI |

\| SQLite | Windows host | Stores readings/events |

\| Physical ESP32-C3 (\`TEMP-001\`) | External device | Publishes temperature to shared temperature topic |

\| HiveMQ public broker | Internet | MQTT transport; **\*\*not a trusted/authenticated broker\*\*** |



**\*\*Data flow:\*\*** Sensor publisher → \`broker.hivemq.com:1883\` → Team 2 Gateway HMAC/replay verification → Team 2 verified/status/security topics → Windows Node-RED → SQLite/dashboard. The gateway, not the MQTT broker, decides whether a reading is trusted.



**## 2. Prerequisites and local assets**



1\. Windows with VMware Workstation Pro, GNS3 Desktop and its GNS3 VM installed and working.

2\. Team 2 GNS3 project containing \`DO-001\`, \`PH-001\`, \`AQ1-Gateway\`, \`Attacker1\` and configured NAT/switch connections. Other topology nodes may exist.

3\. Node.js, npm, Node-RED and the Team 2 Node-RED flow backup. Previously recorded versions: Node.js **\*\*22.14.0\*\***, Node-RED **\*\*5.0.7\*\***, \`@flowfuse/node-red-dashboard\` **\*\*1.32.0\*\***. These are historical working versions, not mandatory upgrade targets.

4\. Node-RED SQLite node package and any other packages required by the exported flow (check **\*\*Manage palette\*\*** after import).

5\. Team 2 SQLite database, if historical data must be preserved, and a database schema/init procedure for a clean install.

6\. Python 3 and dependencies **\*\*inside each Alpine container\*\***; MQTT Python client \`paho-mqtt\` is required by the Python publishers/gateway.

7\. **\*\*Correct matching per-device HMAC keys\*\*** already provisioned on the sensor and gateway containers. Do not copy secrets into this README or screenshots.

8\. Internet access to HiveMQ on TCP **\*\*1883\*\***. Public broker connectivity is needed for this demonstration; the connection is not TLS-protected.

9\. The physical ESP32-C3 must be powered, connected and publishing for live \`TEMP-001\` data.



**\*\*Recorded Windows working directory:\*\*** \`C:\AQ1_Team2\Deployment\NodeRED_Install\`  

**\*\*Recorded database path:\*\*** \`C:\AQ1_Team2\Deployment\NodeRED_Install\aq1_team2.db\`  

**\*\*Environment variable used:\*\*** \`AQ1_TEAM2_DB_PATH\`.



**\*\*Do not delete or replace\*\*** the existing GNS3 project, Docker container files, \`.env\` files, key files, replay-state files or SQLite database when restarting the demonstration.



**## 3. MQTT topic map — Team 2**



\| Purpose | Topic |

\|---|---|

\| DO publisher | \`aq1/team2/sensors/dissolved_oxygen\` |

\| pH publisher | \`aq1/team2/sensors/ph\` |

\| Gateway sensor subscription | \`aq1/team2/sensors/#\` |

\| Verified readings | \`aq1/team2/gateway/verified\` |

\| Security events | \`aq1/team2/events/security\` |

\| Sensor availability/status | \`aq1/team2/events/status\` |

\| Shared physical temperature | \`aq1/pond1/temperature\` |



**\*\*Isolation:\*\*** Team 2's DO/pH/verified/status/security topics are distinct from Team 1's topics. The physical temperature topic is shared. Do **\*\*not\*\*** publish attack payloads to \`aq1/pond1/temperature\`.



**## 4. Start the system — existing installation (recommended)**



Follow this order. **\*\*Only start a process if it is not already running.\*\*** The DO/pH publishers and gateway were intentionally configured for **\*\*manual startup\*\***, not automatic launch at GNS3 container boot.



**### Step 1 — Start VMware and GNS3**



1\. Start **\*\*VMware Workstation Pro\*\*** and ensure the **\*\*GNS3 VM\*\*** is powered on and healthy.

2\. Open **\*\*GNS3 Desktop\*\***, load Team 2 saved AQ-1 Team 2 project.

3\. Start the topology or the required nodes: \`DO-001\`, \`PH-001\`, \`AQ1-Gateway\` and supporting NAT/switch.

4\. Leave \`Attacker1\` stopped until an authorised test is scheduled.

5\. Check GNS3 node link status and console access. GNS3 NAT addresses can change; **\*\*do not hard-code an old IP\*\***.



**### Step 2 — Check connectivity in the Gateway console**



Open \`AQ1-Gateway\` → **\*\*Console\*\***. Example checks:



\`\`\`sh

ip addr

ip route

ping -c 3 1.1.1.1

\`\`\`



If name resolution fails, inspect \`/etc/resolv.conf\` and the GNS3 NAT connection. Previously, using a working DNS server such as \`1.1.1.1\` resolved a DNS issue, but do not overwrite network configuration unnecessarily. To test MQTT connectivity, check the gateway startup output rather than assuming a ping proves broker port 1883 is reachable.



**### Step 3 — Start DO and pH publishers (only if stopped)**



In **\*\*DO-001 → Console\*\***, check the files and process:



\`\`\`sh

ls -l /root/do_sensor.py /root/do_sensor.env /root/setup.sh

ps | grep '[d]o_sensor.py'

\`\`\`



If not running, use the previously established launcher:



\`\`\`sh

sh /root/setup.sh

\`\`\`



In **\*\*PH-001 → Console\*\***:



\`\`\`sh

ls -l /root/ph_sensor.py /root/ph_sensor.env /root/setup.sh

ps | grep '[p]h_sensor.py'

\`\`\`



If not running:



\`\`\`sh

sh /root/setup.sh

\`\`\`



**\*\*Do not run \`setup.sh\` twice\*\*** while a publisher is active; duplicate publishers may cause misleading readings, sequence collisions and replay alerts. The launcher is specific to the configured Team 2 containers. If files are missing, restore from Team 2 container backup rather than guessing new HMAC keys or rewriting scripts.



**### Step 4 — Start the verification Gateway**



In **\*\*AQ1-Gateway → Console\*\***:



\`\`\`sh

ls -l /root/gateway.py /root/do_hmac.key /root/ph_hmac.key /root/temp_hmac.key

ps | grep '[g]ateway.py'

\`\`\`



If no gateway process is running:



\`\`\`sh

python3 /root/gateway.py

\`\`\`



Observe \`ACCEPTED\` messages for legitimate DO/pH and, if online, TEMP. The gateway should reject invalid signatures and replayed sequences. Do not display key contents. A local \`/root/replay_state.json\` was used for sequence tracking; **\*\*do not delete/reset it casually\*\***, because resetting replay state can affect the demonstration's freshness assumptions.



**### Step 5 — Start Windows Node-RED**



Open **\*\*PowerShell\*\*** on Team 2 Windows host:



\`\`\`powershell

node --version

npm --version

node-red --version

\`\`\`



If Node-RED is not installed, see Section 5. If it is installed, set the Team 2 database path in the **\*\*same PowerShell session\*\*** and start Node-RED:



\`\`\`powershell

$env:AQ1_TEAM2_DB_PATH = 'C:\AQ1_Team2\Deployment\NodeRED_Install\aq1_team2.db'

node-red

\`\`\`



Open the editor at **\*\*http\://localhost:1880\*\***. The dashboard URL is determined by Team 2 imported \`ui-base\` and \`ui-page\` paths; open it using the Dashboard link in Node-RED rather than assuming a specific \`/ui\` or \`/dashboard\` URL.



Confirm the Team 2 flow is deployed and its MQTT nodes subscribe to \`aq1/team2/...\` topics. Do not accidentally deploy the Team 1 flow or write to the Team 1 database path.



**### Step 6 — Verify physical temperature**



Power the ESP32-C3. Confirm that the gateway receives valid \`TEMP-001\` readings from \`aq1/pond1/temperature\` and that the dashboard labels temperature as **\*\*PHYSICAL\*\***. If it is absent, DO/pH can still be tested independently; record the temperature feed as unavailable rather than inventing data.



**## 5. Fresh Windows Node-RED installation or recovery**



Use this only if the original installation is missing or broken.



1\. Install a supported Node.js version compatible with the intended Node-RED release. The previous working installation used Node.js 22.14.0.

2\. Install Node-RED in PowerShell:



   \`\`\`powershell

   npm install -g --unsafe-perm node-red

   \`\`\`



3\. Start \`node-red\` once to create its user directory (normally \`%USERPROFILE%\\.node-red\`), then stop it with **\*\*Ctrl+C\*\***.

4\. From that user directory, install the Dashboard and SQLite nodes used by the Team 2 flow:



   \`\`\`powershell

   cd "$env:USERPROFILE\\.node-red"

   npm install @flowfuse/node-red-dashboard\@1.32.0

   npm install node-red-node-sqlite

   \`\`\`



5\. In Node-RED editor, use **\*\*Menu → Import\*\*** to load **\*\*Team 2 flows export\*\***. Review missing nodes and install other packages if required.

6\. Check the MQTT broker settings (\`broker.hivemq.com\`, port \`1883\`) and verify **\*\*all\*\*** Team 2 MQTT topics before Deploy.

7\. Ensure the database directory exists. Set \`AQ1_TEAM2_DB_PATH\` and inspect SQLite node configuration. If the flow hard-codes a database path, update it in the editor to Team 2 actual path. Restore a backed-up \`aq1_team2.db\` if historical records matter. **\*\*Do not assume the schema is automatically created by the flow.\*\***

8\. Deploy, check the debug sidebar, open the dashboard, and verify a new accepted reading reaches the display/database.



\> A clean install cannot be guaranteed from the information in this README alone: the exact Team 2 flow JSON, SQLite schema, container image definitions and provisioned keys must be retained/backed up. Section 4 is the tested **\*\*restart path\*\*** for the previously configured system.



**## 6. Normal-operation acceptance checklist**



\- [ ] GNS3 VM and Team 2 topology are running.

\- [ ] DO-001 publisher is active **\*\*once\*\*** and sending signed readings.

\- [ ] PH-001 publisher is active **\*\*once\*\*** and sending signed readings.

\- [ ] Gateway is active **\*\*once\*\*** and logging \`ACCEPTED\` for legitimate sensor traffic.

\- [ ] \`TEMP-001\` is accepted if the physical device is available.

\- [ ] Node-RED starts on Windows and the Team 2 dashboard opens.

\- [ ] DO/pH/temperature cards reflect accepted gateway values, not unverified raw publications.

\- [ ] SQLite writes/reads succeed; historical charts populate as data accumulates.

\- [ ] No unexplained repeated \`REJECTED\`, replay or sensor-outage alerts.



**\*\*Evidence:\*\*** Save a GNS3 topology screenshot, both publisher consoles, gateway accepted logs, Node-RED live dashboard, and history/incident view. Redact credentials, HMAC keys and private configuration.



**## 7. Security demonstration — authorised testing only**



The planned demonstration covers: **\*\*(1)\*\*** valid signed baseline, **\*\*(2)\*\*** forged/tampered DO rejection, **\*\*(3)\*\*** replay rejection, **\*\*(4)\*\*** publisher outage/monitoring response, and **\*\*(5)\*\*** optional cross-team invalid publication. Perform attacks **\*\*only on Team 2 topics and only with team permission\*\***. Do not attack public broker infrastructure, unrelated topics or the shared physical temperature feed.



1\. Capture baseline \`ACCEPTED\` output and dashboard values.

2\. Start \`Attacker1\` **\*\*only for the demonstration\*\***; verify its existing script/configuration before running it. A generic attack command is intentionally not given because the exact deployed attacker script and test results were not confirmed in the previous setup.

3\. For a tamper/forgery test, send a deliberately invalid signed DO message to the **\*\*Team 2 DO topic\*\***, then verify gateway \`REJECTED\` and that the trusted reading did not change.

4\. For replay testing, reuse a previously valid Team 2 message only within the authorised lab and verify the gateway's sequence rejection. Gateway supports replay checks; this should be documented as a separate security control from HMAC.

5\. For outage testing, stop **\*\*one\*\*** legitimate publisher and observe status/SAFE-HOLD in Node-RED **\*\*if implemented and verified on this Team 2 build\*\***. No physical actuator is controlled. Restart the publisher after capturing evidence.

6\. Optional Team 1 → Team 2 test should be attempted only after local tests pass; use a **\*\*Team 2 test topic\*\***, never the shared temperature topic.



**\*\*Do not claim PASS\*\*** for attack/outage scenarios without actual gateway and dashboard evidence from Team 2 machine.



**## 8. Troubleshooting**



\| Symptom | Check / action |

\|---|---|

\| GNS3 cannot connect to server | Confirm GNS3 VM powered on; check GNS3 server preferences and VMware network adapters; restart GNS3 if needed. |

\| Container has no internet | Inspect \`ip route\`, NAT link, DNS and Windows firewall; don't assume a previously recorded IP is still valid. |

\| No DO/pH readings | Verify one publisher process, broker hostname/port, correct Team 2 topic, and MQTT connection logs. |

\| Gateway rejects all DO/pH readings | Check sensor and gateway **\*\*matching per-device keys\*\***, message serialization, sequence numbers and timestamps. Do not print keys. |

\| \`REPLAY\` alerts after restart | Check duplicate publisher processes, sequence-file persistence (\`/root/do_sequence.txt\` or equivalent), and gateway replay state. Avoid blindly resetting counters. |

\| Temperature missing | Check ESP32-C3 power/Wi-Fi, \`aq1/pond1/temperature\`, TEMP key match and gateway acceptance. |

\| Node-RED won't open | Confirm \`node-red\` is running, port 1880 is free and firewall/browser are not blocking localhost. |

\| Dashboard shows no data | Check Node-RED MQTT-in subscriptions to **\*\*Team 2 verified topic\*\***, JSON parsing, node errors and gateway publishing. |

\| SQLite errors | Check the database path, directory permissions, database schema and the environment variable set in the Node-RED launch shell. |

\| Dashboard shows stale values | Check last accepted timestamp and gateway status events; an MQTT packet reaching the broker is not evidence of gateway acceptance. |

\| Attacker test unexpectedly changes trusted value | Stop the test, capture logs and verify topic routing, gateway verification and whether a valid key was inadvertently used. |



**## 9. Shut down and preserve state**



1\. Stop the authorised attacker test first, if active.

2\. Stop publishers and Gateway gracefully with **\*\*Ctrl+C\*\*** in their active consoles where possible; avoid terminating the entire GNS3 VM first.

3\. Stop Node-RED with **\*\*Ctrl+C\*\*** in PowerShell.

4\. Back up Team 2 flows, SQLite database, project file and **\*\*securely stored\*\*** device key material. Keep secrets outside shared repositories and screenshots.

5\. Save the GNS3 project, stop containers and power down the GNS3 VM/VMware as required.



**## 10. Backup inventory before a presentation**



Store a private backup of:



\- Team 2 **\*\*actual Team 2 Node-RED flow export\*\*** and required Node-RED package list.

\- \`C:\AQ1_Team2\Deployment\NodeRED_Install\aq1_team2.db\` plus the SQLite schema/init instructions.

\- GNS3 project, GNS3 VM version and container template/image configuration.

\- \`/root/do_sensor.py\`, \`/root/ph_sensor.py\`, \`/root/gateway.py\`, their \`.env\`/launcher files, and sequence/replay state files.

\- DO, pH and TEMP device-specific HMAC keys **\*\*stored securely, not in the README\*\***.

\- ESP32-C3 firmware/configuration and the temperature publisher topic.



**## 11. Source and deployment notes**



\- Development repository: https\://github.com/nininehaa/aq1-secure-aquaculture-iot

\- Team 2 paths, topics, and launch commands above are based on the earlier working configuration. Verify them on Team 2 PC because later edits may have changed them.

\- The provided Team 1 Node-RED export has **\*\*88 nodes\*\*** and subscribes to \`aquaculture/gateway/verified\`, \`aquaculture/events/status\`, and \`aquaculture/events/security\`; it is **\*\*not\*\*** a ready-to-deploy Team 2 configuration.

\- Azure dashboard code in the development repository was a **\*\*stretch plan, not deployed\*\***. Do not add Azure setup to this runbook or claim Azure was used.

\- Public HiveMQ at port 1883 does not provide the confidentiality, broker access control or availability guarantees of a production deployment. HMAC provides application-layer integrity/authenticity when keys are protected; sequence checks provide replay resistance for supported message formats.



**---**



**\*\*Quick start:\*\*** VMware/GNS3 → start DO-001 and PH-001 **\*\*once\*\*** (\`sh /root/setup.sh\`) → start Gateway **\*\*once\*\*** (\`python3 /root/gateway.py\`) → PowerShell set \`AQ1_TEAM2_DB_PATH\` and run \`node-red\` → verify dashboard and gateway logs → only then start authorised tests.
