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