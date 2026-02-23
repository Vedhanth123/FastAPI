# https://www.youtube.com/watch?v=M2NzvnfS-hI
# referencing from the above youtube video to understand the python to postgre connection

import psycopg2
from dotenv import load_dotenv
import os

load_dotenv() 


DB_HOSTNAME = os.getenv("DB_HOSTNAME")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")
DB = os.getenv("DB")


# with clause don't need commits and close statements

try:

    # This is a connection object
    with psycopg2.connect(
        host=DB_HOSTNAME, database=DB, user=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT
    ) as conn:

        # But... to interact perform database transactions operations we need cursor object
        with conn.cursor() as cursor:

            sql_query = "CREATE TABLE IF NOT EXISTS test(" \
            "            id SERIAL PRIMARY KEY," \
            "            name VARCHAR(255)," \
            "            age INTEGER)"
            cursor.execute(sql_query)
            print(cursor)

except Exception as e:
    print(e)
