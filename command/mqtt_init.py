import paho.mqtt.client as mqtt

client = mqtt.Client(client_id="Command Dashboard", clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")

client.connect("localhost", port=1883, keepalive=60, bind_address="")

client.loop_start()

if __name__ == "__main__" :
    client.publish("test", "this is a test message")
    client.publish_callback = print("message published !")
    input("waiting, press enter to close")