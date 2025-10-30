import psycopg
from dotenv import load_dotenv
import os

load_dotenv()

class DB:
    def __init__(self):
        try:
            self._conn = psycopg.connect(
                host=os.getenv("DB_HOST", "localhost"),
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASS")
            )
            self._cur = self._conn.cursor()
        except Exception as e:
            print("Failed to connect to DB: ", e)
            self._conn = None
            self._cur = None
    def is_connected(self):
        return self._conn is not None and self._cur is not None

    def select_exists(self):
        self._cur.execute("SELECT CASE WHEN EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema='bed' AND table_name='act1') THEN 1 ELSE 0 END;")
        return self._cur.fetchone()[0] == 1

    #def write_to_db(self, processor):


