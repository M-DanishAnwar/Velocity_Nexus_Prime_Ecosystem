import pyodbc
from .config import DBConfig

class DatabaseConnection:
    _instance = None
    _conn = None

    def __new__(cls):
        # Singleton Pattern: Ensures only one DB connection exists
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    def connect(self):
        try:
            if self._conn is None:
                self._conn = pyodbc.connect(DBConfig.get_connection_string())
            return self._conn
        except Exception as e:
            print(f"❌ Database Connection Error: {e}")
            raise e

    def get_cursor(self):
        return self.connect().cursor()

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None