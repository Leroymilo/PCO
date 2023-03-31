import time as t
from datetime import datetime

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import pgsql_init as psql

if __name__ == "__main__" :

    col1, col2 = st.columns(2)
    graph11, graph12 = col1.container(), col1.container()
    graph21, graph22 = col2.container(), col2.container()

    # while True :

    fig = plt.figure("is_on")
    psql.cur.execute("""-- sql
    SELECT cast(extract(epoch FROM timestamp) * 1000 as bigint) as tmstmp, motor_on
    FROM public."GlobalData"
    WHERE timestamp > (NOW()::TIMESTAMP - INTERVAL '10 minutes')
    ORDER BY tmstmp DESC
    """)

    data_on = pd.DataFrame(data=psql.cur.fetchall())
    print(data_on)
