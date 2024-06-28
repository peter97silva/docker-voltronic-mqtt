import time
import yaml
from voltronic import Voltronic
from mqtt import MQTT


def secrets_constructor(loader, node):
    with open('config/secrets.yml', 'r') as secrets_file:
        secrets = yaml.safe_load(secrets_file)
    secret_name = node.value[:].strip()  # :[] to copy the node value
    return secrets.get(secret_name)


yaml.SafeLoader.add_constructor('!secrets', secrets_constructor)

file = open('config/config.yml')
config = yaml.safe_load(file)

inverter = Voltronic(config)
client = MQTT(config)


def loop():
    while True:
        inverter.get("QMOD")
        inverter.get("QPIGS")
        inverter.get("QPIWS")
        inverter.sensors.print()
        client.publish(inverter.sensors)
        time.sleep(config['REPORT_INTERVAL_S'])


if __name__ == "__main__":
    loop()
