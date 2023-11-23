import os

import mysql.connector


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.db_config = {
            "host": os.getenv("DB_HOSTNAME"),
            "user": os.getenv("DB_NAME"),
            "password": os.getenv("DB_USER"),
            "database": os.getenv("DB_PASSWORD"),
        }

    def _connect(self):
        try:
            if not self.conn:
                self.conn = mysql.connector.connect(**self.db_config)
                self.cursor = self.conn.cursor(dictionary=True)
        except mysql.connector.Error as e:
            print(f"Error connecting to the database: {e}")

    def _disconnect(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
        except mysql.connector.Error as e:
            print(f"Error disconnecting from the database: {e}")

    def execute_query(self, query, params=None, fetchone=False):
        try:
            self._connect()
            self.cursor.execute(query, params)
            self.conn.commit()
            result = self.cursor.fetchone() if fetchone else self.cursor.fetchall()
            return result
        except mysql.connector.Error as e:
            print(f"Error executing query: {e}")
        finally:
            self._disconnect()

    def create_task_table(self):
        try:
            self._connect()
            query = """
            CREATE TABLE IF NOT EXISTS tasks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            self.execute_query(query)
        except mysql.connector.Error as e:
            print(f"Error creating 'tasks' table: {e}")
        finally:
            self._disconnect()
