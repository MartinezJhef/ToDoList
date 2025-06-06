from todo_app.models import Session, Task
from datetime import datetime

class TaskController:
    """
    Controlador para manejar operaciones CRUD relacionadas con tareas.
    Utiliza SQLAlchemy para interactuar con la base de datos.
    """

    def __init__(self):
        """
        Inicializa una nueva sesión de base de datos.
        """
        self.session = Session()

    def add_task(self, title, description, due_date):
        """
        Crea una nueva tarea y la guarda en la base de datos.

        Args:
            title (str): Título de la tarea.
            description (str): Descripción de la tarea.
            due_date (datetime.date): Fecha de vencimiento de la tarea.
        """
        task = Task(title=title, description=description, due_date=due_date)
        self.session.add(task)
        self.session.commit()

    def get_tasks(self):
        """
        Recupera todas las tareas almacenadas en la base de datos.

        Returns:
            list: Lista de objetos Task.
        """
        return self.session.query(Task).all()

    def update_task(self, task_id, title, description, due_date):
        """
        Actualiza los datos de una tarea existente.

        Args:
            task_id (int): ID de la tarea a actualizar.
            title (str): Nuevo título.
            description (str): Nueva descripción.
            due_date (datetime.date): Nueva fecha de vencimiento.
        """
        task = self.session.query(Task).get(task_id)
        if task:
            task.title = title
            task.description = description
            task.due_date = due_date
            self.session.commit()

    def delete_task(self, task_id):
        """
        Elimina una tarea de la base de datos.

        Args:
            task_id (int): ID de la tarea a eliminar.
        """
        task = self.session.query(Task).get(task_id)
        if task:
            self.session.delete(task)
            self.session.commit()

    def filter_tasks_by_date(self, target_date):
        """
        Filtra las tareas que coinciden con una fecha específica.

        Args:
            target_date (datetime.date): Fecha objetivo para filtrar.

        Returns:
            list: Lista de tareas con fecha de vencimiento igual a target_date.
        """
        return self.session.query(Task).filter(Task.due_date == target_date).all()
