import os

import mysql.connector


class Database:
    def __init__(self):
        self.db_config = {
            "host": os.getenv("DB_HOSTNAME"),
            "user": os.getenv("DB_NAME"),
            "password": os.getenv("DB_USER"),
            "database": os.getenv("DB_PASSWORD"),
        }

    def execute_query(self, query, params=None, fetchone=False):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params)
            conn.commit()
            result = cursor.fetchone() if fetchone else cursor.fetchall()
            return result
        except mysql.connector.Error as e:
            print(f"Error: {e}")
        finally:
            if "cursor" in locals() and cursor is not None:
                cursor.close()
            if "conn" in locals() and conn is not None:
                conn.close()

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
