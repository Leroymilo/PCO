import streamlit as st
import psycopg2

HOST : str = "255.255.211.1"
PORT : str = "5000"
USER : str = "user"
PWD : str = "password"
DATABASE : str = "DB_PCO"

con = psycopg2.connect(host=HOST, port=PORT, user=USER, password=PWD)
cur = con.cursor()

if __name__ == "__main__" :
    container = st.container()
    