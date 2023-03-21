import streamlit as st

from Room import *

if __name__ == "__main__" :
    st.markdown("# État global")
    cols = st.columns(2)
    with cols[0] :
        state = st.checkbox(
            label="lancer modélisation physique",
            key=0,
            value=False
        )
    
    with cols[1] :
        if state :
            text = "ON"
        else :
            text = "OFF"
        st.markdown(f"### {text}")
    
    for room in rooms :
        room.loop(st.container())
