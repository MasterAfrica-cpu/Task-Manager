class Task:
    def __init__(self, id, title, description, priority, due_date, category, completed=False):
        self.id = id
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.category = category
        self.completed = completed

    def mark_as_completed(self):
        """Отметить задачу как выполненную"""
        self.completed = True

    def __repr__(self):
        return (f"Task(id={self.id}, title={self.title}, description={self.description}, "
                f"priority={self.priority}, due_date={self.due_date}, category={self.category}, "
                f"completed={self.completed})")