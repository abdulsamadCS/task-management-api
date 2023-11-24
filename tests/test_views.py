# tests/test_views.py
import base64

import pytest
from flask import Flask

from app.database import Database
from app.views import tasks_bp


@pytest.fixture(scope="module")
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["BASIC_AUTH_USERNAME"] = "root"
    app.config["BASIC_AUTH_PASSWORD"] = "root"
    app.register_blueprint(tasks_bp)
    return app


@pytest.fixture(scope="module")
def client(app):
    return app.test_client()


@pytest.fixture(scope="module")
def test_database():
    return Database()


@pytest.fixture(scope="module")
def test_auth_headers(app):
    valid_credentials = base64.b64encode(
        f'{app.config["BASIC_AUTH_USERNAME"]}:{app.config["BASIC_AUTH_USERNAME"]}'.encode(
            "utf-8"
        )
    ).decode("utf-8")
    return {"Authorization": "Basic " + valid_credentials}


def test_get_tasks(client, test_database, test_auth_headers):
    # Add a sample task to the database
    test_database.execute_query(
        "INSERT INTO tasks (title, description) VALUES (%s, %s)",
        params=("Test Task", "This is a test task."),
    )
    # Test GET /tasks endpoint
    response = client.get("/tasks", headers=test_auth_headers)
    assert response.status_code == 200
    assert response.json[-1]["title"] == "Test Task"


def test_create_task(client, test_database, test_auth_headers):
    # Test POST /tasks endpoint
    new_task_data = {"title": "New Task", "description": "This is a new task."}
    response = client.post(
        "/tasks",
        json=new_task_data,
        headers=test_auth_headers,
    )
    res_json = response.json
    id = res_json.get("id")
    assert response.status_code == 201

    # Check if the task is added to the database
    check_query = "SELECT * FROM tasks WHERE id = %s"
    check_result = test_database.execute_query(
        check_query, params=(f"{str(id)}",), fetchone=True
    )
    assert check_result is not None
    assert check_result["description"] == "This is a new task."


def test_get_task(client, test_database, test_auth_headers):
    # Add a sample task to the database
    id = test_database.execute_query(
        "INSERT INTO tasks (title, description) VALUES (%s, %s)",
        params=("Test Task", "This is a test task."),
        return_id=True,
    )

    # Test GET /tasks/{id} endpoint
    response = client.get(f"/tasks/{str(id)}", headers=test_auth_headers)
    assert response.status_code == 200


def test_update_task(client, test_database, test_auth_headers):
    # Add a sample task to the database
    id = test_database.execute_query(
        "INSERT INTO tasks (title, description) VALUES (%s, %s)",
        params=("Test Task", "This is a test task."),
        return_id=True,
    )

    # Test PUT /tasks/{id} endpoint
    updated_task_data = {
        "title": "Updated Task",
        "description": "This task has been updated.",
    }
    response = client.put(
        f"/tasks/{str(id)}",
        json=updated_task_data,
        headers=test_auth_headers,
    )
    assert response.status_code == 200

    # Check if the task is updated in the database
    check_query = "SELECT * FROM tasks WHERE id = %s"
    check_result = test_database.execute_query(
        check_query, params=(str(id),), fetchone=True
    )
    assert check_result is not None
    assert check_result["description"] == "This task has been updated."


def test_delete_task(client, test_database, test_auth_headers):
    # Add a sample task to the database
    id = test_database.execute_query(
        "INSERT INTO tasks (title, description) VALUES (%s, %s)",
        params=("Test Task", "This is a test task."),
        return_id=True,
    )

    # Test DELETE /tasks/{id} endpoint
    response = client.delete(f"/tasks/{str(id)}", headers=test_auth_headers)
    assert response.status_code == 200

    # Check if the task is deleted from the database
    check_query = "SELECT * FROM tasks WHERE id = %s"
    check_result = test_database.execute_query(
        check_query, params=(str(id),), fetchone=True
    )
    assert check_result is None
