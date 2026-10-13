# AQ-1 — Final showcase evidence extracted from submitted report

**Evidence provenance:** All images in this directory were extracted **unchanged** from `Group-6_AQ1_Final_Report_All.pdf` (the submitted 53-page final report). They are reproductions of figures **already in the submitted report**, not new live-test results or independently validated evidence. Captions below describe exactly what the figures support.

| Filename | Report page / figure | Supported observation |
|---|---|---|
| `physical_esp32_ds18b20_photo.jpeg` | Page 24, Artefact 2 Figure 5 | Actual prototype temperature sensor, breadboard and wiring shown; not a validated complete wiring schematic |
| `physical_temperature_serial_output.jpeg` | Page 24, Artefact 2 Figure 4 | Physical temperature firmware/development serial view |
| `gateway_valid_hmac_acceptance.png` | Page 20, Artefact 2 Figure 2 | Gateway console accepting authenticated readings |
| `gateway_verified_messages.png` | Page 30, Artefact 2 Figure 10 | Gateway accepting signed messages |
| `gateway_do_replay_rejection.png` | Page 31, Artefact 2 Figure 11 | **DO-001 replay rejected by sequence checking**, NOT proof of incorrect HMAC |
| `gateway_sensor_outage_safehold.png` | Page 31, Artefact 2 Figure 12 | Sensor outage / software safe-state indication; **no physical actuator controlled** |
| `node_red_trusted_readings.png` | Page 32, Artefact 2 Figure 13 | Node-RED monitoring trusted readings |
| `node_red_outage_indication.png` | Page 32, Artefact 2 Figure 14 | Dashboard stale/offline condition; does not evidence physical control |
| `final_showcase_data_flow.jpeg` | Page 20, Artefact 2 Figure 1 | Schematic flow from physical and simulated sensor sources through gateway |

## Physical temperature sensor (submitted implementation)

- Hardware: ESP32-C3 and waterproof DS18B20, with DS18B20 one-wire data connected at **GPIO4** in the final sketch.
- MQTT topic: `aq1/pond1/temperature` via the HiveMQ public broker on port 1883 (not encrypted).
- The Arduino sketch is in [`../../../hardware/esp32-temperature/AQ1_Physical_Temperature_HMAC.ino`](../../../hardware/esp32-temperature/AQ1_Physical_Temperature_HMAC.ino).
- HMAC-SHA256 authenticates signed readings for holders of the shared secret; it is not encryption.
- The accompanying photograph documents the setup visually but is **not** a complete verified pin-by-pin wiring schematic. Do not label an inferred schematic as photographed/tested.

## Evidence gaps that these report figures cannot resolve

The submitted report identifies a **separate invalid-HMAC capture** as necessary to substantiate wrong-HMAC rejection. These images contain replay rejection and successful HMAC verification but do not independently prove the specific wrong-HMAC attacker demonstration. The separate GNS3 attacker log is needed to close that exact gap. The final GNS3 project, node programs and Node-RED flow export must also be provided by the team as sanitised files; they should not be fabricated from report screenshots.

**Secrets:** Do not upload real `secrets.h`, Wi-Fi passwords, HMAC keys, `.env`, or unredacted GNS3/Node-RED data. This evidence package contains only the report's extracted figures and explanatory text.
