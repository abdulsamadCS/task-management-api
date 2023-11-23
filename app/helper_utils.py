def validate_task_data(self, task_data):
    if "title" not in task_data or "description" not in task_data:
        raise ValueError("Invalid request data")
