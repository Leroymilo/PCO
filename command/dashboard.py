import streamlit as st

import mqtt_init as mqtt

from Room import *

def refresh() :
    for room in rooms :
        room.push()
    
    payload = {
        "timestamp": datetime.now(),
        "on_": st.session_state[0]
    }
    mqtt.client.publish(topic="global_command")

if __name__ == "__main__" :
    st.markdown("# État global")
    cols = st.columns(2)
    with cols[0] :
        state = st.checkbox(
            label="lancer modélisation physique",
            key=0,
            value=False,
            on_change=refresh
        )
    
    with cols[1] :
        if state :
            text = "ON"
        else :
            text = "OFF"
        st.markdown(f"### {text}")
    
    for room in rooms :
        room.loop(st.container())
