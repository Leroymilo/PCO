from datetime import datetime, timedelta
import time as t

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import numpy as np

import pgsql_init as psql

# Some matplotlib settings :
plt.xticks(rotation=90)

# function to get data for example graph (sliding average over 10 seconds on the last 2 minutes)
def get_use_rate_data() -> pd.DataFrame :

    # Fetching data from database
    psql.cur.execute("""-- sql
    SELECT cast(extract(epoch FROM timestamp) as float) as tmstmp, SUM(lum_prct)/4 as use_rate
    FROM public."RoomData"
    WHERE timestamp > ((SELECT MAX(timestamp) from public."RoomData") - INTERVAL '2 minutes')
    GROUP BY tmstmp
    ORDER BY tmstmp ASC
    """)
    data = np.asarray(psql.cur.fetchall())

    # defining time constants
    window = timedelta(seconds=10)
    min_time = datetime.fromtimestamp(data[0,0]) + window
    max_time = datetime.fromtimestamp(data[-1,0])

    # initializing loop variables
    new_data = []
    time = min_time

    # computing sliding average
    while time <= max_time :
        lower = (time - window).timestamp()
        upper = time.timestamp()
        val = 0
        count = 0
        for line in data :
            if line[0] < lower :
                continue
            if line[0] > upper :
                break
            val += line[1]
            count += 1
        
        if count > 0 :
            new_data.append((time, val/count))

        time += timedelta(seconds=1)
    
    # converting data to dataframe for easier plotting

    df = pd.DataFrame(new_data)
    df.set_index(0, inplace=True)

    return df   

# where the dashboard is made
if __name__ == "__main__" :

    # grid setup
    col1, col2 = st.columns(2)

    col1.markdown("# Title 1-1")
    graph11 = col1.empty()
    col1.markdown("# Title 1-2")
    graph12 = col1.empty()

    col2.markdown("# Title 2-1")
    graph21 = col2.empty()
    col2.markdown("# Title 2-2")
    graph22 = col2.empty()

    # infinite loop to update plots in real time

    while True :

        t0 = t.time()

        # making a graph
        fig, ax = plt.subplots(figsize = (10, 4))

        # fetching data
        data_on = get_use_rate_data()

        # plotting graph with matplotlib
        ax.plot(data_on)

        # setting axes limits for aesthetics
        ax.set_ylim(-2, 102)
        ax.set_xlim(datetime.now()-timedelta(minutes=1), datetime.now())

        # plotting on dashboard
        graph11.pyplot(fig)
        plt.close()

        # actualization delay (1 second)
        while t.time() - t0 < 1 :
            continue
