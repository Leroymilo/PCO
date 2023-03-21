import paho.mqtt.client as mqtt

client = mqtt.Client(client_id="1", clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")

client.connect("192.168.66.26", port=1883, keepalive=60, bind_address="")