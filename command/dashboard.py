import streamlit as st
import psycopg2

# HOST : str = "255.255.211.1"
# PORT : str = "5000"
# USER : str = "Admin"
# PWD : str = "Lasagnes42"
# DATABASE : str = "DB_PCO"

# con = psycopg2.connect(host=HOST, port=PORT, user=USER, password=PWD)
# cur = con.cursor()

if __name__ == "__main__" :
    on_off = st.container()
    on, off = on_off.columns(2)
    st.button("ON", use_container_width=True)
    st.button("OFF", use_container_width=True)
    