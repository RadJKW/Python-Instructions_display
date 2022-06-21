import json 
from paho.mqtt.client import Client as mqtt
class MqttController:
    def __init__(self, coil_properties):
        self.client = mqtt()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("localhost", 1883, 60)
        self.client.loop_start()


    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        self.client.subscribe("coil_properties")
        # publish the coilproperties to the topic as a json string

    def on_message(self, client, userdata, msg):
        pass 

    def publish_message(self, message):
        self.client.publish()