import streamlit as st

tab_names = ["Panneaux Solaires", "LEDs"]

if __name__ == "__main__" :
    st.set_page_config(layout="wide")

    tabs = st.tabs(tab_names)
    tabs = {tab_names[i]: tabs[i] for i in {0, 1}}
    
    