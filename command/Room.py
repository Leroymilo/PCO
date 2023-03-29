import json
from datetime import datetime

import streamlit as st
from streamlit.delta_generator import DeltaGenerator as DG

import mqtt_init as mqtt

class Room :
    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name
        self.cont: DG = None

        self.push(initial=True)

    def loop(self, cont: DG) :
        self.cont = cont
        
        with self.cont :

            st.markdown(f"## {self.name}")

            st.checkbox(
                label="Détecteur de présence", 
                key=200+self.id,
                value=False,
                on_change=self.push
            )

            var = st.checkbox(
                label="Variateur de luminosité",
                key=300+self.id,
                value=False,
                on_change=self.push
            )

            st.slider(
                "Luminosité (%)",
                0, 100, 100, 1,
                key=400+self.id,
                on_change=self.push,
                disabled=(not var)
            )

    def push(self, initial=False) :
        if initial :
            payload = {
                "timestamp": int(datetime.now().timestamp()),
                "room_id": self.id,
                "detect": False,
                "variate": False,
                "lum_prct": 100
            }
        
        else :
            payload = {
                "timestamp": int(datetime.now().timestamp()),
                "room_id": self.id,
                "detect": st.session_state[200+self.id],
                "variate": st.session_state[300+self.id],
                "lum_prct": st.session_state[400+self.id]
            }

        # print("mqtt payload :", payload)
        
        info = mqtt.client.publish("room_command", json.dumps(payload))
        info.wait_for_publish()
        print("message published !")
    
    def __hash__(self) -> int:
        return self.id

rooms: list[Room] = []
for i in range(4) :
    rooms.append(Room(i, f"Salle {i+1}"))