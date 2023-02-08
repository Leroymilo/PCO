import time as t
from sqlite3 import connect

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# Setup

st.set_page_config(layout="wide")

con = connect("data.sql", isolation_level=None)
cursor = con.cursor()


# Classes

class Dashboard :
    def __init__(self) -> None:
        self.main_container = st.container()
        self.rows = []

        self.add_row(2)
        self.add_row(3, [2, 1, 1], [2, 1, 1])
        
        self.left[2].slider("Motor Speed", 0, 90, 90)
    
    def add_row(self, nb_cols: int = 1, layout: list[int] = None, spaces: list[int] = None) :
        if layout is None :
            layout = [1 for _ in range(nb_cols)]
        elif len(layout) < nb_cols :
            layout += [1 for _ in range(nb_cols - len(layout))]

        if spaces is None :
            spaces = [1 for _ in range(nb_cols)]
        elif len(spaces) < nb_cols :
            spaces += [1 for _ in range(nb_cols - len(spaces))]

        columns = self.main_container.columns(nb_cols, layout)
        elements = []
        for i in range(nb_cols) :
            column = [columns[i].empty() for _ in range(spaces[i])]
            elements.append(column)
        self.rows.append(elements)

    def update(self) :
        self.left[0].line_chart(
            pd.read_sql_query("""--sql
            SELECT timestamp_, tread_motor_rot AS "Treadmill Motor Rotation"
            FROM Sensors
            ORDER BY timestamp_ DESC LIMIT 100
            ;""", con=con, index_col="timestamp_")
        )

        cursor.execute("""--sql
        SELECT tread_motor_turns FROM Sensors ORDER BY timestamp_ DESC
        ;""")
        self.left[1].markdown(
            body=f"Treadmill Motor turns : {cursor.fetchone()[0]}"
        )

        self.right[0].line_chart(
            pd.read_sql_query("""--sql
            SELECT timestamp_, room_nb AS "Current Location"
            FROM Sensors
            ORDER BY timestamp_ DESC LIMIT 100
            ;""", con=con, index_col="timestamp_")
        )

        cursor.execute(f"""--sql
            SELECT {", ".join("room_led_"+str(i+1) for i in range(4))}
            FROM Sensors
            ORDER BY timestamp_ DESC
        ;""")
        room_states = cursor.fetchone()
        for i in range(4) :

            if room_states[i] :
                bg_col = "white"
                txt_col = "black"
            else :
                bg_col = "black"
                txt_col = "white"

            self.rooms[i].markdown(
                f"<h1 style='background-color:{bg_col}; color:{txt_col}; text-align:center;'>Room {i+1}</h1>",
                unsafe_allow_html=True
            )
    
    def run(self) :
        while True :
            t0 = t.time()
            self.update()
            while t.time() - t0 < 1 :
                t.sleep(0.01)


# Main

if __name__ == "__main__" :
    db = Dashboard()
    db.run()