import time as t
import math as m

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def ensoleillement(t) :
    return max(0, -m.cos(2*m.pi*t/24))

T = [t/2 for t in range(48)]
data = [ensoleillement(t) for t in T]

class Dashboard :
    def __init__(self) -> None:
        self.main_container = st.container()
        self.top_cols = list(self.main_container.columns(3))
        self.top_left = self.top_cols[0].empty()
        self.top_mid = self.top_cols[1].empty()
        self.top_right = self.top_cols[2].empty()
        self.bottom_cols = list(self.main_container.columns(3))
        self.bottom_left = self.bottom_cols[0].empty()
        self.bottom_mid = self.bottom_cols[1].empty()
        self.bottom_right = self.bottom_cols[2].empty()
    
    def update(self) :
        data.append(data.pop(0))
        self.top_left.line_chart(
            pd.DataFrame(data=data, index=T, columns=["truncated sine"])
        )
        self.bottom_right.line_chart(
            pd.DataFrame(data=data[::-1], index=T, columns=["reverse truncated sine"])
        )
    
    def run(self) :
        while True :
            t0 = t.time()
            self.update()
            t.sleep(1)

if __name__ == "__main__" :
    db = Dashboard()
    db.run()