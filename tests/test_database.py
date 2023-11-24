import pytest

from app.database import Database


@pytest.fixture(scope="module")
def test_database():
    return Database()


def test_connect(test_database):
    # Test the connection to the database
    test_database._connect()
    assert test_database.conn is not None


def test_disconnect(test_database):
    # Test disconnecting from the database
    test_database._connect()  # Ensure there is an active connection
    test_database._disconnect()
    assert test_database.conn.connection_id is None


def test_execute_query_select(test_database):
    # Test executing a SELECT query
    query = "SELECT * FROM tasks"
    result = test_database.execute_query(query)
    assert isinstance(result, list)


def test_execute_query_insert(test_database):
    # Test executing an INSERT query
    query = "INSERT INTO tasks (title, description) VALUES (%s, %s)"
    params = ("Test Task", "This is a test task.")
    result = test_database.execute_query(query, params=params, return_id=True)
    assert isinstance(result, int)  # Expecting the inserted ID


def test_execute_query_update(test_database):
    # Test executing an UPDATE query
    # Assuming there is a task with ID=1 in the database
    query = "UPDATE tasks SET title = %s WHERE id = %s"
    params = ("Updated Task", 1)
    result = test_database.execute_query(query, params=params)
    assert result is not None


def test_execute_query_delete(test_database):
    # Test executing a DELETE query
    # Assuming there is a task with ID=1 in the database
    query = "DELETE FROM tasks WHERE id = %s"
    params = (1,)
    result = test_database.execute_query(query, params=params)
    assert result is not None
