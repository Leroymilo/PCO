import time as t
from datetime import datetime
import random as rd
from sqlite3 import connect


# Setup

db = connect("data.sql")
cursor = db.cursor()


# Constants

T_INIT = t.time()
SPEED = 90  # in deg/s
NB_ROOMS = 4
ROOM_LENGTHS = [15, 30, 35, 20]
SUM_LENGHTS = [15, 45, 80, 100]


# Main loop

if __name__ == "__main__" :
    while True :
        time = t.time() - T_INIT
        rot = (time * SPEED) % 360
        turns = (time * SPEED) // 360
        for i in range(NB_ROOMS) :
            if time % SUM_LENGHTS[-1] < SUM_LENGHTS[i] :
                room = i+1
                break
        
        query = f"""--sql
        INSERT INTO Sensors VALUES
        (
            "{datetime.now().strftime("%x %X.%f")}",
            {rot}, {turns}, {room},
            {", ".join(str(i+1 == room) for i in range(4))}
        )
        ;"""
        cursor.execute(query)
        db.commit()

        t.sleep(0.1)