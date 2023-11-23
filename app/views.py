from flask import Blueprint, jsonify, request
from flask.views import MethodView

from app.database import Database
from app.helper_utils import validate_task_data
from app.models import Task

db = Database()
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


class TaskViewFactory:
    @staticmethod
    def create(is_list_view=True):
        if is_list_view:
            return TaskListView.as_views("tasks")
        return TaskDetailView.as_views("task")


class TaskListView(MethodView):
    def get(self):
        try:
            query = "SELECT * FROM tasks"
            results = db.execute_query(query)
            tasks = [Task(**result).to_dict() for result in results]
            return jsonify(tasks), 200
        except Exception as e:
            return {"error": str(e)}, 500

    def post(self):
        try:
            new_task = request.json
            validate_task_data(new_task)
            query = "Insert INTO tasks (title, description) VALUES (%s, %s)"
            db.execute_query(query, (new_task["title"], new_task["description"]))
            return {"messege": "Task added successfully"}, 201
        except ValueError as ve:
            return {"error": str(ve)}, 400
        except Exception as e:
            return {"error": str(e)}, 500


class TaskDetailView(MethodView):
    def get(self, task_id):
        try:
            query = "SELECT * FROM tasks WHERE id = %s"
            result = db.execute_query(query, (task_id,), fetchone=True)

            if result:
                task = Task(**result)
                return jsonify(task.to_dict()), 200
            else:
                return {"message": "Task not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 500

    def put(self, task_id):
        try:
            updated_task = request.json
            validate_task_data(updated_task)
            query = "UPDATE tasks SET title = %s, description = %s WHERE id = %s"
            db.execute_query(
                query, (updated_task["title"], updated_task["description"], task_id)
            )
            return {"message": "Task updated successfully"}, 200
        except ValueError as ve:
            return {"error": str(ve)}, 400
        except Exception as e:
            return {"error": str(e)}, 500

    def delete(self, task_id):
        try:
            query = "DELETE FROM tasks WHERE id = %s"
            db.execute_query(query, (task_id,))
            return {"message": "Task deleted successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500


tasks_bp.add_url_rule("/<int:task_id>", view_func=TaskViewFactory.create(False))
tasks_bp.add_url_rule("", view_func=TaskViewFactory.create(True))
