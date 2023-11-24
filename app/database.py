import os

import mysql.connector


class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.db_config = {
            "host": os.getenv("DB_HOST"),
            "database": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
        }

    def _connect(self):
        self.conn = mysql.connector.connect(**self.db_config)
        self.cursor = self.conn.cursor(dictionary=True)

    def _disconnect(self):
        if self.conn:
            self.conn.close()

    def execute_query(self, query, params=None, fetchone=False, return_id=False):
        try:
            self._connect()
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            if return_id and query.lower().startswith("insert"):
                last_inserted_id = self.cursor.lastrowid
                self.conn.commit()
                return last_inserted_id
            result = self.cursor.fetchone() if fetchone else self.cursor.fetchall()
            self.conn.commit()
            return result
        except Exception as e:
            print(f"Error executing query: {e}")
        finally:
            self._disconnect()

    def create_task_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.execute_query(query)
