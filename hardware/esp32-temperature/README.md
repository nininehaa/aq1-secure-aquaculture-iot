# AQ-1 Physical Temperature Sensor

ESP32-C3 with a waterproof DS18B20 temperature sensor.

This component was developed and tested by Sahil Basnet and Neha Thanait as part of the AQ-1 cybersecurity capstone project.

The ESP32-C3 publishes temperature readings to the HiveMQ MQTT broker using HMAC-SHA256 for message integrity.

The GNS3 security gateway verifies the readings before forwarding trusted data to the Node-RED dashboard.

This prototype does not control physical pumps or aerators.
