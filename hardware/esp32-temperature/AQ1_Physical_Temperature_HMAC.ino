#include <WiFi.h>
#include <PubSubClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <Preferences.h>
#include <math.h>
#include <stdint.h>
#include "mbedtls/md.h"
#include "secrets.h"

// =============================================
// AQ-1 PHYSICAL TEMPERATURE SENSOR V2
// ESP32-C3 + DS18B20
// MQTT + HMAC-SHA256 + Replay Protection
// =============================================

// DEVICE IDENTITY
const char* DEVICE_ID   = "POND-A-ESP32-01";
const char* SENSOR_ID   = "TEMP-001";
const char* POND_ID     = "POND-01";
const char* SENSOR_TYPE = "temperature";
const char* UNIT        = "C";

// MQTT
const char* MQTT_TOPIC = "aq1/pond1/temperature";
const int MQTT_PORT = 1883;

// DS18B20
#define ONE_WIRE_BUS 4

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

// NETWORK
WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);

// PERSISTENT REPLAY COUNTER
Preferences preferences;
uint32_t sequenceNumber = 0;

// =============================================
// HMAC-SHA256
// =============================================

String createHMAC(const String& message) {

  byte hmacResult[32];

  mbedtls_md_context_t ctx;
  mbedtls_md_init(&ctx);

  const mbedtls_md_info_t* info =
    mbedtls_md_info_from_type(MBEDTLS_MD_SHA256);

  if (info == nullptr ||
      mbedtls_md_setup(&ctx, info, 1) != 0) {
    mbedtls_md_free(&ctx);
    return "";
  }

  int result = mbedtls_md_hmac_starts(
    &ctx,
    (const unsigned char*)TEMP_HMAC_KEY,
    strlen(TEMP_HMAC_KEY)
  );

  if (result == 0) {
    result = mbedtls_md_hmac_update(
      &ctx,
      (const unsigned char*)message.c_str(),
      message.length()
    );
  }

  if (result == 0) {
    result = mbedtls_md_hmac_finish(
      &ctx,
      hmacResult
    );
  }

  mbedtls_md_free(&ctx);

  if (result != 0) {
    return "";
  }

  char outputBuffer[65];

  for (int i = 0; i < 32; i++) {
    sprintf(
      outputBuffer + (i * 2),
      "%02x",
      hmacResult[i]
    );
  }

  outputBuffer[64] = '\0';

  return String(outputBuffer);
}

// =============================================
// WIFI
// =============================================

void connectWiFi() {

  Serial.println("Connecting to Wi-Fi...");

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("Wi-Fi: CONNECTED");

  Serial.print("ESP32 IP: ");
  Serial.println(WiFi.localIP());
}

// =============================================
// MQTT
// =============================================

void connectMQTT() {

  while (!mqttClient.connected()) {

    Serial.println("Connecting to MQTT broker...");

    // Public HiveMQ broker
    bool connected = mqttClient.connect(DEVICE_ID);

    if (connected) {
      Serial.println("MQTT: CONNECTED");
    } else {
      Serial.print("MQTT: FAILED, state=");
      Serial.println(mqttClient.state());
      delay(5000);
    }
  }
}

// =============================================
// SETUP
// =============================================

void setup() {

  Serial.begin(115200);
  delay(1500);

  Serial.println();
  Serial.println("=================================");
  Serial.println("AQ-1 Secure Physical Temperature V2");
  Serial.println("=================================");

  Serial.print("Device ID: ");
  Serial.println(DEVICE_ID);

  Serial.print("Sensor ID: ");
  Serial.println(SENSOR_ID);

  // Initialise persistent storage
  if (!preferences.begin("aq1-temp", false)) {
    Serial.println("ERROR: Cannot open sequence storage");

    while (true) {
      delay(1000);
    }
  }

  // Load saved sequence
  sequenceNumber = preferences.getUInt("sequence", 0);

  Serial.print("Stored sequence number: ");
  Serial.println(sequenceNumber);

  // Initialise physical sensor
  sensors.begin();

  Serial.print("Temperature sensors detected: ");
  Serial.println(sensors.getDeviceCount());

  if (sensors.getDeviceCount() == 0) {
    Serial.println("ERROR: No DS18B20 sensor detected");

    while (true) {
      delay(1000);
    }
  }

  // Connect Wi-Fi
  connectWiFi();

  // Configure MQTT
  mqttClient.setServer(MQTT_BROKER, MQTT_PORT);
  mqttClient.setBufferSize(1024);

  connectMQTT();
}

// =============================================
// MAIN LOOP
// =============================================

void loop() {

  // Maintain Wi-Fi
  if (WiFi.status() != WL_CONNECTED) {
    connectWiFi();
  }

  // Maintain MQTT
  if (!mqttClient.connected()) {
    connectMQTT();
  }

  mqttClient.loop();

  // Read temperature
  sensors.requestTemperatures();

  float temperature = sensors.getTempCByIndex(0);

  // Validate physical reading
  if (
    temperature == DEVICE_DISCONNECTED_C ||
    !isfinite(temperature) ||
    temperature < -55.0 ||
    temperature > 125.0
  ) {
    Serial.println("ERROR: Invalid temperature reading");
    delay(5000);
    return;
  }

  String value = String(temperature, 2);
  String status = "OK";

  // ===========================================
  // PERSISTENT SEQUENCE COUNTER
  // ===========================================

  if (sequenceNumber == UINT32_MAX) {
    Serial.println("ERROR: Sequence counter exhausted");

    while (true) {
      delay(1000);
    }
  }

  uint32_t nextSequence = sequenceNumber + 1;

  // Save BEFORE publishing
  size_t bytesWritten =
    preferences.putUInt("sequence", nextSequence);

  if (bytesWritten != sizeof(uint32_t)) {
    Serial.println("ERROR: Cannot persist sequence number");
    delay(5000);
    return;
  }

  sequenceNumber = nextSequence;

  Serial.print("Sequence Number: ");
  Serial.println(sequenceNumber);

  // ===========================================
  // TIMESTAMP
  // ===========================================

  // ESP32 uptime in milliseconds.
  // Unix timestamp upgrade planned later.
  String timestamp = String(millis());

  // ===========================================
  // CANONICAL HMAC MESSAGE
  //
  // sensor_id|pond_id|sensor_type|value|
  // unit|status|timestamp|sequence
  // ===========================================

  String signedMessage =
    String(SENSOR_ID) + "|" +
    String(POND_ID) + "|" +
    String(SENSOR_TYPE) + "|" +
    value + "|" +
    String(UNIT) + "|" +
    status + "|" +
    timestamp + "|" +
    String(sequenceNumber);

  String hmacValue = createHMAC(signedMessage);

  if (hmacValue.length() != 64) {
    Serial.println("ERROR: HMAC generation failed");
    delay(5000);
    return;
  }

  // ===========================================
  // JSON PAYLOAD
  // ===========================================

  String payload = "{";

  payload += "\"sensor_id\":\"" + String(SENSOR_ID) + "\",";
  payload += "\"pond_id\":\"" + String(POND_ID) + "\",";
  payload += "\"sensor_type\":\"" + String(SENSOR_TYPE) + "\",";
  payload += "\"value\":" + value + ",";
  payload += "\"unit\":\"" + String(UNIT) + "\",";
  payload += "\"status\":\"" + status + "\",";
  payload += "\"timestamp\":\"" + timestamp + "\",";
  payload += "\"sequence\":" + String(sequenceNumber) + ",";
  payload += "\"hmac\":\"" + hmacValue + "\"";

  payload += "}";

  // ===========================================
  // SERIAL OUTPUT
  // ===========================================

  Serial.println();

  Serial.print("Temperature: ");
  Serial.print(value);
  Serial.println(" C");

  Serial.print("MQTT topic: ");
  Serial.println(MQTT_TOPIC);

  Serial.print("Payload: ");
  Serial.println(payload);

  // ===========================================
  // MQTT PUBLISH
  // ===========================================

  bool published = mqttClient.publish(
    MQTT_TOPIC,
    payload.c_str()
  );

  if (published) {
    Serial.println("Publish: SUCCESS");
  } else {
    Serial.println("Publish: FAILED");
  }

  delay(5000);
}