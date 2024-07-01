MQTT interface for Voltronic(aka MPPSolar, Axpert, Powland, EASun. etc.) solar inverters.

# Exposed sensors:
- Inverter status
- Grid voltage
- Grid frequency
- Output load watt
- Battery capacity (SOC)
- Inverter heatsink temperature
- PV voltage

To run add environmental variables to the container:
```env
MQTT_SERVER: "192.168.1.1"
MQTT_USER: "MQTT_USER"
MQTT_PASSWORD: "MQTT_PASSWORD"
SERIAL_PORT: "/dev/ttyUSB0"
```

Then attach config folder to the image as '/config' and run the container.