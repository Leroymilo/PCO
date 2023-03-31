import time as t
from datetime import datetime

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import pgsql_init as psql

def timestamp2int(timestamp: pd.Timestamp) -> int :
    return int(datetime.strptime(timestamp.ctime(), '%Y-%m-%d %H:%M:%S.%f').timestamp())

if __name__ == "__main__" :

    col1, col2 = st.columns(2).
    graph11, graph12 = col1.container(), col1.container()
    graph21, graph22 = col2.container(), col2.container()

    # while True :

    # psql.cur.execute("""-- sql
    # SELECT table_name, column_name, column_type
    # FROM information_schema.columns
    # WHERE table_name in ('GlobalCommand', 'GlobalData', 'RoomCommand', 'RoomData')
    # """)

    # print(*psql.cur.fetchall(), sep='\n')

    fig = plt.figure("is_on")
    psql.cur.execute("""-- sql
    SELECT timestamp as tmstmp, motor_on FROM public."GlobalData"
    ORDER BY tmstmp DESC
    LIMIT 1000
    """)

    data_on = pd.DataFrame(data=psql.cur.fetchall())
    print(data_on)
    data_on[0].apply(timestamp2int)
    datetime().strptime('%Y-%m-%d %H:%M:%S.%f')

    print(data_on)
