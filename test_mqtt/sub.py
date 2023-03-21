import paho.mqtt.client as mqtt

print("defining client")
client = mqtt.Client(client_id="2", clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")

print("connecting client")
client.connect("192.168.66.26", port=1883, keepalive=60, bind_address="")

print("subscribing to topic 'test'")
client.subscribe("test")

stop = False

def custom_on_msg(client: mqtt.Client, userdata, message: mqtt.MQTTMessage) :
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

    global stop
    stop = True

client.on_message = custom_on_msg
print("starting client loop")
client.loop_start()

while True :
    if stop :
        break

client.loop_stop()