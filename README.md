MQTT interface for Voltronic(aka MPPSolar, Axpert, Powland, EASun. etc.) solar inverters.

#Exposed sensors:
- Inverter status
- Grid voltage
- Grid frequency
- Output load watt
- Battery capacity (SOC)
- Inverter heatsink temperature
- PV voltage
- PV current

To run create /config/config.yaml with the following content:
```yaml
MQTT_SERVER: "192.168.1.1"
MQTT_USER: "MQTT_USER"
MQTT_PASSWORD: "MQTT_PASSWORD"
MQTT_PORT: 1883
MQTT_TOPIC_PREFIX: "homeassistant/sensor/inverter_"
INVERTER_NAME: "easun_inverter"
REPORT_INTERVAL_S: 0
SERIAL_PORT: "/dev/ttyUSB0"
```

Then attach config.yaml to the image as '/config/config.yaml' and run the container.