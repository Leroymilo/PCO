import streamlit as st
from streamlit.delta_generator import DeltaGenerator as DG

import pgsql_init as pgsql

class Room :
    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name
        self.detect = False
        self.variate = False
        self.variation = 100
        self.cont: DG = None

        self.init_push()

    def loop(self, cont: DG) :
        self.cont = cont
        
        self.cont.markdown(f"# {self.name}")
        self.detect = self.cont.checkbox(
            "Détecteur de présence",
            key=200+self.id,
            on_change=self.push
        )
        self.variate = self.cont.checkbox(
            "Variateur de luminosité",
            key=300+self.id,
            on_change=self.push
        )
        self.variation = self.cont.slider(
            "Luminosité",
            0, 100, 100, 1,
            key=400+self.id,
            on_change=self.push,
            disabled=(not self.variate)
        )

    def init_push(self) :
        print("initial push")

        query = f"""-- sql
        INSERT INTO public."RoomCommand"
        VALUES (
            NOW()::TIMESTAMP,
            {self.id},
            FALSE,
            FALSE,
            100,
            TRUE
        )
        """
        # print(query)

        pgsql.cur.execute(query)

        pgsql.con.commit()
    
    def push(self) :
        print("push")

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
    
    def __hash__(self) -> int:
        return self.id

rooms: list[Room] = []
for i in range(4) :
    rooms.append(Room(i, f"Salle {i+1}"))