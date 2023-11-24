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
            return TaskListView.as_view("tasks")
        return TaskDetailView.as_view("task")


class TaskListView(MethodView):
    def get(self):
        try:
            query = "SELECT * FROM tasks"
            results = db.execute_query(query) or {}
            tasks = [Task(**result).to_dict() for result in results]
            return jsonify(tasks), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def post(self):
        try:
            new_task = request.json
            validate_task_data(new_task)
            query = "Insert INTO tasks (title, description) VALUES (%s, %s)"
            db.execute_query(query, params=(new_task["title"], new_task["description"]))
            return jsonify({"messege": "Task added successfully"}), 201
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500


class TaskDetailView(MethodView):
    def get(self, task_id):
        try:
            query = "SELECT * FROM tasks WHERE id = %s"
            result = db.execute_query(query, params=(task_id,), fetchone=True)

            if result:
                task = Task(**result)
                return jsonify(task.to_dict()), 200
            else:
                return jsonify({"message": "Task not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def put(self, task_id):
        try:
            # Check if the task with the given ID exists
            check_query = "SELECT * FROM tasks WHERE id = %s"
            check_result = db.execute_query(
                check_query, params=(task_id,), fetchone=True
            )

            if not check_result:
                return jsonify({"message": "Task not found"}), 404
            updated_task = request.json
            validate_task_data(updated_task)
            query = "UPDATE tasks SET title = %s, description = %s WHERE id = %s"
            db.execute_query(
                query,
                params=(updated_task["title"], updated_task["description"], task_id),
            )
            return jsonify({"message": "Task updated successfully"}), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def delete(self, task_id):
        try:
            query = "DELETE FROM tasks WHERE id = %s"
            db.execute_query(query, params=(task_id,))
            return jsonify({"message": "Task deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


tasks_bp.add_url_rule("/<int:task_id>", view_func=TaskViewFactory.create(False))
tasks_bp.add_url_rule("", view_func=TaskViewFactory.create(True), strict_slashes=False)
