import math as m
import time as t

import streamlit as st
import pandas as pd



def ensoleillement(t) :
    return max(0, -m.cos(2*m.pi*t/24))

T = [t/2 for t in range(48)]
Ens = [ensoleillement(t) for t in T]

chart = st.empty()

while True :
    t0 = t.time()

    Ens.append(Ens.pop(0))
    chart.line_chart(
        pd.DataFrame(data=Ens, index=T, columns=["Ensoleillement"])
    )

    while(t.time()-t0 < 2) :
        continue