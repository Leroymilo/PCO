import psycopg2

HOST : str = "localhost"
PORT : str = "5432"
USER : str = "postgres"
PWD : str = "password"
DATABASE : str = "RealTime"

con = psycopg2.connect(host=HOST, port=PORT, user=USER, password=PWD, database=DATABASE)
cur = con.cursor()

def close() :
    con.close()

if __name__ == "__main__" :

    cur.execute("""-- sql
    SELECT DISTINCT table_name
    FROM information_schema.columns
    ORDER BY table_name
    """)

    print(*cur.fetchall(), sep='\n')

    cur.execute("""-- sql
    SELECT * FROM public."RoomCommand"
    """)

    print(*cur.fetchall(), sep='\n')

    close()