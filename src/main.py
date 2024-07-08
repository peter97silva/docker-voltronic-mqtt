#! /usr/bin/python3
import time
from voltronic import Voltronic
from mqtt import MQTT
import os

REPORT_INTERVAL_S = int(os.getenv('REPORT_INTERVAL_S', 1))

inverter = Voltronic()
client = MQTT()


def loop():
    while True:
        inverter.update("QMOD")
        inverter.update("QPIGS")
        inverter.update("QPIWS")

        inverter.print_sensors()

        client.publish(inverter.sensors)
        time.sleep(REPORT_INTERVAL_S)


def single():
    inverter.update("QMOD")
    inverter.update("QPIGS")
    inverter.update("QPIWS")
    inverter.update("QPIRI")

    inverter.print_sensors()

    # client.publish(inverter.sensors)


if __name__ == "__main__":
    loop()
