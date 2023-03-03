import streamlit as st
import psycopg2

# HOST : str = "localhost"
# PORT : str = "5432"
# USER : str = "postgres"
# PWD : str = "password"
# DATABASE : str = "DB_PCO"

# con = psycopg2.connect(host=HOST, port=PORT, user=USER, password=PWD)
# cur = con.cursor()

if __name__ == "__main__" :
    on, off = st.container().columns(2)
    on = on.button("ON", use_container_width=True)
    off = off.button("OFF", use_container_width=True)

    rooms = []
    for i in range(4) :
        room = st.container()
        rooms.append(room)
        room.markdown(f"# Salle {i+1}")
        room.checkbox("Détecteur de présence", key=200+i)
        vars = room.checkbox("Variateur de luminosité", key=300+i)
        room.slider("Luminosité", 0, 100, 50, 1, key=400+i, disabled=(not vars))