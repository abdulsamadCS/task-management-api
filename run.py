from flask import Flask
from flask_basicauth import BasicAuth

from app.database import Database
from app.views import tasks_bp

app = Flask(__name__)
app.config["BASIC_AUTH_USERNAME"] = "root"
app.config["BASIC_AUTH_PASSWORD"] = "root"
basic_auth = BasicAuth(app)

# Create an instance of the Database class
database = Database()

# Register the 'tasks' blueprint
app.register_blueprint(tasks_bp)

# Create the 'tasks' table if it doesn't exist
database.create_task_table()

if __name__ == "__main__":
    app.run(debug=True)
