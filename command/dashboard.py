from datetime import datetime

import streamlit as st
from streamlit.delta_generator import DeltaGenerator as DG

import pgsql_init as pgsql

class Room :
    def __init__(self, id: int, name: str, container: DG) -> None:
        self.id = id
        self.detect = False
        self.variate = False
        self.variation = 100
        self.cont: DG = container

        self.cont.markdown(f"# {name}")
        self.detect = self.cont.checkbox(
            "Détecteur de présence",
            key=200+i,
            on_change=self.push
        )
        self.variate = self.cont.checkbox(
            "Variateur de luminosité",
            key=300+i,
            on_change=self.push
        )
        self.variation = self.cont.slider(
            "Luminosité",
            0, 100, 100, 1,
            key=400+i,
            on_change=self.push,
            disabled=(not self.variate)
        )
    
    def push(self) :
        query = f"""-- sql
        INSERT INTO public."RoomCommand"
        VALUES (
            NOW()::TIMESTAMP,
            {self.id},
            {st.session_state[200+self.id]},
            {st.session_state[300+self.id]},
            {st.session_state[400+self.id]},
            TRUE
        )
        """
        # print(query)

        pgsql.cur.execute(query)

        pgsql.con.commit()


if __name__ == "__main__" :
    on, off = st.container().columns(2)
    on = on.button("ON", use_container_width=True)
    off = off.button("OFF", use_container_width=True)

    rooms = []
    for i in range(4) :
        rooms.append(Room(i, f"Salle {i+1}", st.container()))