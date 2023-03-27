from sys import exc_info

import paho.mqtt.client as mqtt

client = mqtt.Client(client_id="1", clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")

client.connect("localhost", port=1883, keepalive=60, bind_address="")

res = 1
while res :
    try :
        res = int(input("power? (0 <= power <= 255) : "))
        client.publish("test", payload = res)
    except :
        exc_info()