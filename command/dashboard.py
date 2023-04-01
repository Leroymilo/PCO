import json
from datetime import datetime

import streamlit as st
from streamlit_toggle import st_toggle_switch

import mqtt_init as mqtt


nb_rooms = 4
room_names = [f"Salle {i+1}" for i in range(nb_rooms)]

def get_time() :
    return int(datetime.now().timestamp() * 1000)

def display_room_settings(i: int) :
    st.markdown(f"## {room_names[i]}")

    det = st_toggle_switch(
        label="Détecteur de présence", 
        key=200+i,
        default_value=False
    )

    var = st_toggle_switch(
        label="Variateur de luminosité",
        key=300+i,
        default_value=False
    )

    lum = st.slider(
        "Luminosité (%)",
        0, 100, 100, 1,
        key=400+i,
        disabled=(not var)
    )

    payload = {
        "timestamp": get_time(),
        "room_id": i,
        "detect": det,
        "variate": var,
        "lum_prct": lum
    }
    mqtt.client.publish("room_command", json.dumps(payload))

if __name__ == "__main__" :
    st.markdown("# État global")
    state = st_toggle_switch(
        label="",
        key=0,
        default_value=False,
        label_after=True
    )
    
    if state :
        text = "### ON"
    else :
        text = "### OFF"
    
    st.markdown(text)

    payload = {
        "timestamp": get_time(),
        "on_": state
    }
    mqtt.client.publish("global_command", json.dumps(payload))

    for i in range(nb_rooms) :
        display_room_settings(i)
    
    if mqtt.client.want_write() :
        mqtt.client.loop_write()