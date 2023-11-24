# task-management-api

This is a simple Flask application for managing tasks. It includes basic CRUD (Create, Read, Update, Delete) operations for tasks using a MySQL database.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python (version 3.6 or higher)
- pip
- MySQL

## Getting Started

Follow these steps to run the Flask Task Manager application:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/abdulsamadCS/task-management-api.git
   cd task-management-api

   ```

2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Database:**

   ```bash
   touch .env
   ```

   Open .env and write DB credentials

   ```bash
   DB_HOST=your_db_host
   DB_NAME=your_db_name
   DB_USER=your_db_user_name
   DB_PASSWORD=your_db_password
   ```

4. **Run the application:**

   ```bash
   python run.py
   ```

5. **Access the Application:**

   ```bash
   Open your web browser and go to http://localhost:5000/tasks
   ```

## Usage

- The application provides a simple task API to perform CRUD operations on tasks.
- Basic authentication is enabled with the username and password configured in run.py.
- Username: root, Password: root
- Tasks are stored in a MySQL database, and the necessary tables are created automatically on application startup.

## Examples

- ### Create a Task

```bash
curl -X POST -H "Content-Type: application/json" -u root:root -d '{"title": "New Task", "description": "Task Description"}' http://localhost:5000/tasks
```

- ### Get All Tasks

```bash
curl -u root:root http://localhost:5000/tasks
```

- ### Get Specific Task

```bash
curl -u root:root http://localhost:5000/tasks/1
```

- ### Update a Task

```bash
curl -X PUT -H "Content-Type: application/json" -u root:root -d '{"title": "Updated Task", "description": "Updated Task Description"}' http://localhost:5000/tasks/1
```

- ### Delet a Task

```bash
curl -X DELETE -u root:root http://localhost:5000/tasks/1
```

## Testing

To run unit tests, run:

```bash
pytest
```
