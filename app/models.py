class Task:
    def __init__(self, id, title, description, created_at):
        self.id = id
        self.title = title
        self.description = description
        self.created_at = created_at

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at,
        }
