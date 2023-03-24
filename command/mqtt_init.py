import paho.mqtt.client as mqtt

client = mqtt.Client(client_id="Command Dashboard", clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")

client.connect("192.168.123.26", port=1883, keepalive=60, bind_address="")

def custom_reconnect(client: mqtt.Client, *args, **kwargs) :
    print("disconnected")
    client.reconnect()
    print("reconnected")

# client.on_disconnect = custom_reconnect

client.loop_start()