from urllib.parse import urlparse, parse_qs
import psycopg
from psycopg.types.json import Jsonb
from dataclasses import dataclass
from typing import Generic, TypeVar, Optional

T = TypeVar("T")


@dataclass
class Extremes(Generic[T]):
    min_value: T
    max_value: T


class Postgres:
    def __init__(self, url: str):
        print(f"Postgres url: {url}")
        parsed = urlparse(url)
        parsed_query = parse_qs(parsed.query)
        dbname = parsed.path.lstrip("/") if parsed.path else "postgres"
        self.client = psycopg.connect(
            f"host={parsed.hostname or 'localhost'} port={parsed.port or 8123} "
            f"dbname={dbname} user={parsed_query.get('user', ['postgres'])[0]} "
            f"password={parsed_query.get('password', ['postgres'])[0]}",
            autocommit=True,
        )

    def command(self, sql: str):
        cursor = self.client.cursor()
        cursor.execute(sql)

    def query(self, sql: str) -> list[any]:
        cursor = self.client.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows

    def insert_data(self, table_name: str, data: list, date_field: str = 'epoch'):
        cursor = self.client.cursor()
        sql = f"INSERT INTO {table_name} (id, epoch, data) VALUES (%s, %s, %s)"
        data_jsonb = ((record[0], record[1][date_field], Jsonb(record[1])) for record in data)
        cursor.executemany(sql, data_jsonb)

    def create_table_as(self, new_table_name: str, source_table_name: str):
        self.command(f"CREATE TABLE {new_table_name} AS SELECT * FROM {source_table_name} WHERE FALSE")

    def drop_table(self, table_name: str):
        self.command(f"DROP TABLE IF EXISTS {table_name} ")

    def count_rows(self,table_name:str):
        sql = f"SELECT Count(*) FROM {table_name}"
        return self.query(sql)[0][0]

    def get_extremes(self, table_name: str, field_name: str) -> Optional[Extremes]:
        sql = f"SELECT Count(*),MIN(data->>{field_name}),MAX(data->>{field_name}) FROM {table_name}"
        [count, min_value, max_value] = self.query(sql)[0]
        if count > 0:
            return Extremes(min_value, max_value)
        else:
            return None

    def get_number_by_day(self, table_name: str) ->list[tuple]:
        sql = f"""
            SELECT epoch AS event_date , Count(*) AS count 
            FROM {table_name} 
            GROUP BY event_date 
            ORDER BY event_date
            """
        return self.query(sql)
