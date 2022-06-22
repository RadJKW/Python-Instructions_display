# -*- coding: utf-8 -*-

# Copyright (c) 2013 Roger Light <roger@atchoo.org>
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Distribution License v1.0
# which accompanies this distribution.
#
# The Eclipse Distribution License is available at
#   http://www.eclipse.org/org/documents/edl-v10.php.
#
# Contributors:
#    Roger Light - initial implementation

# This example shows how you can use the MQTT client in a class.

# from context import context  # Ensures paho is in PYTHONPATH

import socket
import threading
import time
import paho.mqtt.client as mqtt
import json
import pprint as pp
import os


class MyMQTTClass(mqtt.Client):
    def on_connect(self, mqttc, obj, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    def on_connect_fail(self, mqttc, obj):
        print("Connect failed")

    def on_message(self, mqttc, obj, msg):
        # if message is a json string, convert to dict and
        print("MESSAGE RECEIVED: {}".format(msg.topic))
        if msg.payload is not None:
            msg.payload = json.loads(msg.payload)
            pp.pprint(msg.payload, indent=2, sort_dicts=False, compact=False)
            return
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    def on_publish(self, mqttc, obj, mid):
        pass
        # #print("mid: "+str(mid))
        # print("Published message: "+str(mid))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        pass
        # print("Subscribed: "+str(mid)+" "+str(granted_qos))

    def on_log(self, mqttc, obj, level, string):
        # if logging level is MQTT_LOG_ERROR
        if level == mqtt.MQTT_LOG_ERROR:
            print("LOGGING: {}".format(string))


def do_mqtt_stuff(hostname):
    mqttc = MyMQTTClass(client_id="python-test")
    mqttc.connect("192.168.0.30", 1883, 60)
    mqttc.publish(
        topic="pi/{}/coil_info".format(hostname),
        payload="Hello World!",
        qos=2,
        retain=False,
    )
    mqttc.subscribe("pi/cw88/#", 2)
    mqttc.loop_forever()


def do_other_stuff():
    while True:
        time.sleep(30)
        print("Hello World!")


def main():
    hostname = socket.gethostname()
    hostname = hostname.split(".")[0]
    print("Hostname: {}".format(hostname))
    # allow mqtt to run in a seperate thread and do other stuff at the same time
    # both should be able to print to the console
    other_thread = threading.Thread(target=do_other_stuff)
    other_thread.start()
    do_mqtt_stuff(hostname)


if __name__ == "__main__":
    os.system("clear")
    main()
