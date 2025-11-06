from psycopg import sql, connect
from dotenv import load_dotenv
import os

load_dotenv()

class DB:
    def __init__(self):
        try:
            self._conn = connect(
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
        return self._cur.fetchone()[0]

    # creating a schema
    def create_schema(self, schema_name):
        query = sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(
            sql.Identifier(schema_name)
        )
        self._cur.execute(query)
    def create_table(self, schema_name, table_name):
        query = sql.SQL("CREATE TABLE IF NOT EXISTS {}.{}").format(
            sql.Identifier(schema_name),
            sql.Identifier(table_name)
        )
        self._cur.execute(query)

    #def write_to_table(self, processor, table_name):
    def write_to_table(self, schema_name, table_name, data):
        if not (data):
            print("Missing data for write")
            return
        if not self.select_exists(schema_name, table_name):
            print("Incorrect table parameters")
            return

        for record in data:
            columns = list(record.keys())
            values = list(record.values())

            query = sql.SQL("""
                INSERT INTO {}.{} ({})
                VALUES ({})
            """).format(
                sql.Identifier(schema_name),
                sql.Identifier(table_name),
                sql.SQL(', ').join(map(sql.Identifier, columns)),
                sql.SQL(', ').join(sql.Placeholder() * len(values))
            )

            try:
                self._cur.execute(query, values)
            except Exception as e:
                print(f"Failed to insert record: {e}")
                self._conn.rollback()
                return

        self._conn.commit()
        print(f"Successfully inserted {len(data)} record(s) into {schema_name}.{table_name}.")


