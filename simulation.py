import time as t
from datetime import datetime
import json

import paho.mqtt.client as mqtt

client = mqtt.Client(client_id="Simulation", clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")

client.connect("localhost", port=1883, keepalive=60, bind_address="")

client.subscribe("room_command")
client.subscribe("global_command")

nb_leds = 4

on_ = False
detect = [False for _ in range(nb_leds)]
variate = [False for _ in range(nb_leds)]
lum_prct = [100 for _ in range(nb_leds)]

cur_room = 0
is_on = [False for _ in range(nb_leds)]

def update_room(room_id) :
    global is_on

    if 0 <= room_id < nb_leds :
        if not on_ :
            is_on[room_id] = False
            return

        if not detect[room_id] or (detect[room_id] and room_id == cur_room) :
            
            if variate[room_id] :
                is_on[room_id] = (lum_prct[room_id] > 0)
            else :
                is_on[room_id] = True
        
        else :
            is_on[room_id] = False

def on_room_command(client: mqtt.Client, userdata, message: mqtt.MQTTMessage) :
    global detect
    global variate
    global lum_prct

    print("command received")

    payload = json.loads(message.payload)
    room_id = payload["room_id"]
    detect[room_id] = payload["detect"]
    variate[room_id] = payload["variate"]
    lum_prct[room_id] = payload["lum_prct"]

    update_room(room_id)

def on_global_command(client: mqtt.Client, userdata, message: mqtt.MQTTMessage) :
    global on_

    print("command received")

    payload = json.loads(message.payload)
    on_ = payload["on_"]

    for i in range(nb_leds) :
        update_room(i)

client.message_callback_add("room_command", on_room_command)
client.message_callback_add("global_command", on_global_command)
client.loop_start()

print("start loop")

while True :
    t0 = t.time()

    now = int(datetime.now().timestamp() * 1000)

    payload = {}
    payload["timestamp"] = now
    payload["motor_on"] = on_
    payload["cur_room"] = cur_room

    client.publish("global_data", json.dumps(payload))

    for i in range(nb_leds) :
        payload = {}
        payload["timestamp"] = now
        payload["room_id"] = i
        payload["is_on"] = is_on[i]
        payload["lum_prct"] = lum_prct[i]

        client.publish("room_data", json.dumps(payload))

    while t.time() - t0 < 0.1 :
        continue