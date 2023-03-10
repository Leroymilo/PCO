import streamlit as st

from Room import *

if __name__ == "__main__" :
    on, off = st.container().columns(2)
    on = on.button("ON", use_container_width=True)
    off = off.button("OFF", use_container_width=True)
    
    for room in rooms :
        room.loop(st.container())