import time as t
from sqlite3 import connect
import json

import streamlit as st
from streamlit.delta_generator import DeltaGenerator as DG
import pandas as pd
import matplotlib.pyplot as plt

# Setup

st.set_page_config(layout="wide")

con = connect("data.sql", isolation_level=None, timeout=10)
cursor = con.cursor()


# Functions

def update_speed() :
    new_speed = st.session_state.speed_slider
    cursor.execute(f"INSERT INTO Parameters VALUES ({t.time()}, {new_speed})")
    con.commit()


# Classes

class Dashboard :
    def __init__(self) -> None:
        self.run_ = True
        self.main_container = st.container()
        self.rows: list[DG | list[DG | list[DG]]] = []

        self.add_row(2)
        self.add_row(3, [2, 1, 1], [2, 2, 2])
        self.add_row(2, [1, 1], [2, 1])
        
        self.speed = self.rows[1][0][1].slider("Motor Speed", 0, 180, 60, on_change=update_speed, key="speed_slider")
        self.rows[2][0][0].write("# Percentage of LED lighting :")
        leds = self.rows[2][0][1].number_input("text", 0, 100, 25, label_visibility="hidden")
        self.rows[2][1].write(f"# ROI : {leds*200}k€")
    
    def add_row(self, nb_cols: int = 1, layout: list[int] = None, capacities: list[int] = None) :
        assert nb_cols > 0
        
        if nb_cols == 1 :
            self.rows.append(self.main_container.empty())
            return
        
        if layout is None :
            layout = [1 for _ in range(nb_cols)]
        elif len(layout) < nb_cols :
            layout += [1 for _ in range(nb_cols - len(layout))]

        if capacities is None :
            capacities = [1 for _ in range(nb_cols)]
        elif len(capacities) < nb_cols :
            capacities += [1 for _ in range(nb_cols - len(capacities))]

        columns = self.main_container.columns(layout)
        elements = []
        for i in range(nb_cols) :
            assert capacities[i] > 0

            if capacities[i] == 1 :
                elements.append(columns[i].empty())
            else :
                column = [columns[i].empty() for _ in range(capacities[i])]
                elements.append(column)
        
        self.rows.append(elements)

    def update(self) :
        self.rows[0][0].line_chart(
            pd.read_sql_query("""--sql
            SELECT timestamp_, tread_motor_rot AS "Treadmill Motor Rotation"
            FROM Sensors
            ORDER BY timestamp_ DESC LIMIT 100
            ;""", con=con, index_col="timestamp_")
        )

        data1 = pd.read_sql_query("""--sql
        SELECT tread_motor_turns FROM Sensors ORDER BY timestamp_ DESC LIMIT 1
        ;""", con=con)
        data2 = pd.read_sql_query("""--sql
        SELECT speed FROM Parameters ORDER BY timestamp_ DESC LIMIT 1
        ;""", con=con)
        self.rows[1][0][0].markdown(
            body=f"### Treadmill Motor turns : {data1.to_numpy()[0,0]}, Speed : {data2.to_numpy()[0,0]}"
        )

        self.rows[0][1].line_chart(
            pd.read_sql_query("""--sql
            SELECT timestamp_, room_nb AS "Current Location"
            FROM Sensors
            ORDER BY timestamp_ DESC LIMIT 100
            ;""", con=con, index_col="timestamp_")
        )

        data = pd.read_sql_query(f"""--sql
            SELECT {", ".join("room_led_"+str(i+1) for i in range(4))}
            FROM Sensors
            ORDER BY timestamp_ DESC
        ;""", con=con)
        room_states = data.to_numpy()[0]
        c, s_r = [1, 2, 2, 1], [0, 0, 1, 1]
        for i in range(4) :

            if room_states[i] :
                bg_col = "white"
                txt_col = "black"
            else :
                bg_col = "black"
                txt_col = "white"

            self.rows[1][c[i]][s_r[i]].markdown(
                f"<h1 style='background-color:{bg_col}; color:{txt_col}; text-align:center;'>Room {i+1}</h1>",
                unsafe_allow_html=True
            )
    
    def run(self) :
        while self.run_ :
            t0 = t.time()
            self.update()
            while t.time() - t0 < 1 :
                t.sleep(0.01)


# Main

if __name__ == "__main__" :
    db = Dashboard()
    db.run()