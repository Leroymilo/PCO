from sys import exc_info
from datetime import datetime

import paho.mqtt.client as mqtt

client = mqtt.Client(client_id="python publisher", clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")

client.connect("localhost", port=1883, keepalive=60, bind_address="")

client.loop_start()

res = 1
while res :
    topic = input("topic : ")
    msg = input("message : ") + " at " + datetime.now().strftime("%H:%M:%S")
    if msg == "stop" :
        break
    try :
        client.publish(topic, payload = msg)
    except :
        exc_info()