from psycopg import sql, connect
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row
from dotenv import load_dotenv
import os

load_dotenv()

class SimpleDB:
    def __init__(self):
        try:
            conninfo = os.getenv('CONN_INFO')
            self._pool = ConnectionPool(conninfo)
        except Exception as e:
            print("Failed to connect to DB: ", e)
    def get_connected(self):
        return connect(
                host=os.getenv("DB_HOST", "localhost"),
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASS"),
                row_factory = dict_row
            )

    def select_exists(self, schema_name, table_name, column_name=None):
        if column_name is None:
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
        else:
            query = sql.SQL("""
                    SELECT EXISTS (
                        SELECT 1
                        FROM information_schema.columns
                        WHERE table_schema = {schema}
                          AND table_name = {table}
                          AND column_name = {column}
                    );
                """).format(
                schema=sql.Literal(schema_name),
                table=sql.Literal(table_name),
                column=sql.Literal(column_name)
            )
        with self._pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(query)
                result = cur.fetchone()
                return result["exists"]


    def get_table(self, schema_name, table_name):
        if self.select_exists(schema_name, table_name):
            query = sql.SQL("""
                SELECT * FROM {schema}.{table}
            """).format(
            schema=sql.Identifier(schema_name),
            table=sql.Identifier(table_name)
            )
            with self._pool.connection() as conn:
                with conn.cursor(row_factory=dict_row) as cur:
                    cur.execute(query)
                    table = cur.fetchall()
                    return table
        else:
            print("Cannot find table")

    def get_filtered_table(self, schema_name, table_name, column_name, item_name):
        if self.select_exists(schema_name, table_name, column_name):
            query = sql.SQL("""
                SELECT * FROM {schema}.{table}
                WHERE {column} = {item}
            """).format(
            schema=sql.Identifier(schema_name),
            table=sql.Identifier(table_name),
            column=sql.Identifier(column_name),
            item=sql.Literal(item_name),
            )
            with self._pool.connection() as conn:
                with conn.cursor(row_factory=dict_row) as cur:
                    cur.execute(query)
                    table = cur.fetchall()
                    return table
        else:
            print("Cannot find table")


