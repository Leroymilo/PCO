from sqlite3 import connect

con = connect("data.sql")
cursor = con.cursor()

cursor.execute("""--sql
DROP TABLE IF EXISTS `Sensors`
;""")
cursor.execute("""--sql
CREATE TABLE Sensors
(
    timestamp_ DATETIME PRIMARY KEY,
    tread_motor_rot DOUBLE(5, 2) CHECK (0 <= tread_motor_rot < 360),
    tread_motor_turns INT,
    room_nb INT CHECK (room_nb in (1, 2, 3, 4)),
    room_led_1 BOOLEAN,
    room_led_2 BOOLEAN,
    room_led_3 BOOLEAN,
    room_led_4 BOOLEAN
)
;""")

cursor.execute("""--sql
DROP TABLE IF EXISTS `Parameters`
;""")
cursor.execute("""--sql
CREATE TABLE Parameters
(
    timestamp_ DATETIME PRIMARY KEY,
    speed INT
);""")
cursor.execute("""--sql
INSERT INTO Parameters VALUES (0, 135)
;""")

con.commit()