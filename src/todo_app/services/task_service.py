from todo_app.repositories.controllers import TaskRepository

class TaskService:
    def __init__(self):
        self.repo = TaskRepository()

    def create_task(self, title, description, due_date):
        return self.repo.add_task(title, description, due_date)

    def get_tasks(self):
        return self.repo.get_tasks()

    def update_task(self, task_id, title, description, due_date):
        return self.repo.update_task(task_id, title, description, due_date)

    def delete_task(self, task_id):
        return self.repo.delete_task(task_id)

    def filter_tasks_by_date(self, target_date):
        return self.repo.filter_tasks_by_date(target_date)
