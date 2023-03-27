import psycopg2

HOST : str = "localhost"
PORT : str = "5432"
USER : str = "postgres"
PWD : str = "password"
DATABASE : str = "RealTime"

con = psycopg2.connect(host=HOST, port=PORT, user=USER, password=PWD, database=DATABASE)
cur = con.cursor()

def reset() :
    print("Reseting tables...")

    cur.execute("""-- sql
    -- Table: public.GlobalData

    DROP TABLE IF EXISTS public."GlobalData";

    CREATE TABLE IF NOT EXISTS public."GlobalData"
    (
        "timestamp" timestamp(3) without time zone NOT NULL,
        motor_on boolean NOT NULL DEFAULT 'false',
        CONSTRAINT "GlobalData_pkey" PRIMARY KEY ("timestamp")
    )

    TABLESPACE pg_default;

    ALTER TABLE IF EXISTS public."GlobalData"
        OWNER to postgres;
    """)

    cur.execute("""-- sql
    -- Table: public.RoomCommand

    DROP TABLE IF EXISTS public."RoomCommand";

    CREATE TABLE IF NOT EXISTS public."RoomCommand"
    (
        "timestamp" timestamp(3) without time zone NOT NULL,
        room_id integer NOT NULL,
        detect boolean NOT NULL DEFAULT 'false',
        variate boolean NOT NULL DEFAULT 'false',
        variation integer NOT NULL DEFAULT 100,
        is_on boolean NOT NULL DEFAULT 'true',
        CONSTRAINT "RoomCommand_pkey" PRIMARY KEY ("timestamp", room_id)
    )

    TABLESPACE pg_default;

    ALTER TABLE IF EXISTS public."RoomCommand"
        OWNER to postgres;
    """)

    cur.execute("""-- sql
    -- Table: public.RoomData

    DROP TABLE IF EXISTS public."RoomData";

    CREATE TABLE IF NOT EXISTS public."RoomData"
    (
        "timestamp" timestamp(3) without time zone NOT NULL,
        room_id integer NOT NULL,
        is_on boolean NOT NULL DEFAULT 'false',
        luminosity double precision NOT NULL DEFAULT 100,
        CONSTRAINT "RoomData_pkey" PRIMARY KEY ("timestamp", room_id)
    )

    TABLESPACE pg_default;

    ALTER TABLE IF EXISTS public."RoomData"
        OWNER to postgres;
    """)

    con.commit()

    print("Tables reset !")

def close() :
    con.close()

reset()

if __name__ == "__main__" :

    cur.execute("""-- sql
    SELECT table_name, column_name
    FROM information_schema.columns
    WHERE table_name in ('GlobalData', 'RoomCommand', 'RoomData')
    """)

    print(*cur.fetchall(), sep='\n')

    close()