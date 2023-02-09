import time as t
from datetime import datetime
from sqlite3 import connect, OperationalError
import json

import pandas as pd

# Setup

db = connect("data.sql", isolation_level=None, timeout=10)
cursor = db.cursor()


# Constants

T_INIT = t.time()
NB_ROOMS = 4
ROOM_LENGTHS = [15, 20, 30, 35]
SUM_LENGTHS = [15, 35, 65, 100]


# Variables intialization

rot = 0
turns = 0
room = 1


# Main loop

last_time = t.time() - T_INIT
if __name__ == "__main__" :
    print("simulation started")
    while True :

        # Reading parameters
        data = pd.read_sql_query("""--sql
        SELECT speed FROM Parameters
        ORDER BY timestamp_ DESC LIMIT 1
        ;""", con=db)
        speed = data.to_numpy()[0,0]

        # Actual simulation
        if speed > 0 :
            time = (t.time() - T_INIT) / 5
            rot += (time - last_time) * speed
            if rot >= 360 :
                rot -= 360
                turns += 1
            last_time = time

            pos = (rot + turns * 360) / 10
            for i in range(NB_ROOMS) :
                if pos % SUM_LENGTHS[-1] < SUM_LENGTHS[i] :
                    room = i+1
                    break
        
        # Write data
        query = f"""--sql
        INSERT INTO Sensors VALUES
        (
            {datetime.now().timestamp()},
            {rot}, {round(turns)}, {room},
            {", ".join(str(i+1 == room) for i in range(4))}
        )
        ;"""

        while True :
            try :
                cursor.execute(query)
                break
            except OperationalError :
                continue
        db.commit()

        t.sleep(1)