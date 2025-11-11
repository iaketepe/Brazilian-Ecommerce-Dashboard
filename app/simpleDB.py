from psycopg import sql, connect
from psycopg.rows import dict_row
from dotenv import load_dotenv
import os

load_dotenv()

class SimpleDB:
    def __init__(self):
        try:
            self._conn = connect(
                host=os.getenv("DB_HOST", "localhost"),
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASS"),
                row_factory = dict_row
            )
            self._cur = self._conn.cursor()
        except Exception as e:
            print("Failed to connect to DB: ", e)
            self._conn = None
            self._cur = None
    def is_connected(self):
        return self._conn is not None and self._cur is not None

    def select_exists(self, schema_name, table_name):
        query = sql.SQL("""
                SELECT EXISTS (
                    SELECT 1
                    FROM information_schema.tables
                    WHERE table_schema = {schema}
                      AND table_name = {table}
                );
            """).format(
            schema=sql.Literal(schema_name),
            table=sql.Literal(table_name)
        )
        self._cur.execute(query)
        result = self._cur.fetchone()
        return result['exists']

    def get_table(self, schema_name, table_name):
        if (self.select_exists(schema_name, table_name)):
            query = sql.SQL("""
                SELECT * FROM {schema}.{table}
            """).format(
            schema=sql.Identifier(schema_name),
            table=sql.Identifier(table_name)
            )
            self._cur.execute(query)
            table = self._cur.fetchall()
            #print(f"Table: {table}")
            return table
        else:
            print("Cannot find table")

_  = """simpleDB = SimpleDB()
table = simpleDB.get_table("TEST_ACT1","metrics")
print(type(table))
print(type(table[0]))
print(type(table[0]['name']))
print(table[0]['name'])"""

