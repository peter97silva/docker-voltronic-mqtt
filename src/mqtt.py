import paho.mqtt.client as mqtt


class MQTT:
    def __init__(self, config):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, config['INVERTER_NAME'])
        self.client.on_connect = self.on_connect
        self.client.username_pw_set(config['MQTT_USER'], config['MQTT_PASSWORD'])
        self.client.connect_timeout = 60
        self.client.connect_async(config['MQTT_SERVER'], config['MQTT_PORT'], 60)
        self.client.loop_start()
        self.topic_prefix = config['MQTT_TOPIC_PREFIX']

    def publish(self, data):
        for parameter in data.__dict__:
            self.client.publish(f"{self.topic_prefix}{parameter}", data[parameter], qos=1)

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
