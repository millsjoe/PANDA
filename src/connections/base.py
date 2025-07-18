import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


class BaseConnection:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="db",
            database="panda_db",
            user="postgres",
            password=os.getenv("DB_PASSWORD"),
        )

    def get_connection(self):
        return self.conn

    def close_connection(self):
        self.conn.close()

    def health_check(self):
        return self.conn.status
