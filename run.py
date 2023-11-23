from flask import Flask

from app.database import Database
from app.views import tasks_bp

app = Flask(__name__)

# Create an instance of the Database class
database = Database()

# Register the 'tasks' blueprint
app.register_blueprint(tasks_bp)

# Create the 'tasks' table if it doesn't exist
database.create_task_table()

if __name__ == "__main__":
    app.run(debug=True)
