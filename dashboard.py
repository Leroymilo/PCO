import streamlit as st
import matplotlib.pyplot as plt

class Dashboard :
    def __init__(self) -> None:
        self.led_settings = st.empty
        self.conso = st.empty
        self.led_chart = st.empty
        self.economy = st.empty
        self.ROI = st.empty
        self.facture = st.empty
        self.daily_activ = st.empty
        self.luminosity = st.empty
        