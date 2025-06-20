from todo_app.models.models import Session, Task  # Ajusta el import según tu estructura

class TaskController:
    def __init__(self):
        self.session = Session()

    def add_task(self, title, description, due_date):
        task = Task(title=title, description=description, due_date=due_date)
        self.session.add(task)
        self.session.commit()

    def get_tasks(self):
        return self.session.query(Task).all()

    def update_task(self, task_id, title, description, due_date):
        task = self.session.query(Task).get(task_id)
        if task:
            task.title = title
            task.description = description
            task.due_date = due_date
            self.session.commit()

    def delete_task(self, task_id):
        task = self.session.query(Task).get(task_id)
        if task:
            self.session.delete(task)
            self.session.commit()

    def filter_tasks_by_date(self, target_date):
        return self.session.query(Task).filter(Task.due_date == target_date).all()
