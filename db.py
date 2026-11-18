import psycopg2
from psycopg2.extras import RealDictCursor

CONN = dict(
    host='localhost',
    port=5432,
    dbname='pis_db',
    user='postgres',
    password='1',
    client_encoding='UTF8'
)


class Database:
    def connect(self):
        return psycopg2.connect(**CONN)

    def fetch_all(self, sql, params=None):
        with self.connect() as c:
            with c.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql, params or ())
                return cur.fetchall()

    def execute(self, sql, params=None):
        with self.connect() as c:
            with c.cursor() as cur:
                cur.execute(sql, params or ())
                c.commit()


db = Database()