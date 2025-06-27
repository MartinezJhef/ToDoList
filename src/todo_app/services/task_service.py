"""
Servicios para la gestión de tareas.

Este módulo implementa la clase TaskService, que actúa como intermediario
entre la capa de presentación y el controlador de base de datos, gestionando
las operaciones sobre tareas.

Historias de Usuario: HU005 - HU018
"""

from todo_app.repositories.controllers import TaskController
from todo_app.models.models import Tarea

class TaskService:
    """Servicio que encapsula las operaciones de negocio sobre tareas."""

    def __init__(self):
        """Inicializa el servicio con una instancia del controlador."""
        self.controller = TaskController()

    def create_task(self, title, description, due_date, prioridad='media', categoria=None):
        """
        Crear una nueva tarea (HU005, HU006, HU007).

        Args:
            title (str): Título de la tarea.
            description (str): Descripción de la tarea.
            due_date (date): Fecha de vencimiento.
            prioridad (str): Nivel de prioridad ('baja', 'media', 'alta').
            categoria (str): Categoría ('trabajo', 'hogar', 'estudio').
        """
        self.controller.add_task(title, description, due_date, prioridad, categoria)

    def get_tasks(self, include_deleted=False):
        """
        Obtener todas las tareas (HU010).

        Args:
            include_deleted (bool): Si True, incluye tareas eliminadas.

        Returns:
            list: Lista de tareas.
        """
        return self.controller.get_tasks(include_deleted)

    def update_task(self, task_id, title=None, description=None, due_date=None, prioridad=None, categoria=None):
        """
        Actualizar título, descripción, fecha, prioridad o categoría de una tarea (HU018).

        Args:
            task_id (int): ID de la tarea.
            title (str): Nuevo título.
            description (str): Nueva descripción.
            due_date (date): Nueva fecha de vencimiento.
            prioridad (str): Nueva prioridad ('baja', 'media', 'alta').
            categoria (str): Nueva categoría ('trabajo', 'hogar', 'estudio').
        """
        self.controller.update_task(task_id, title, description, due_date, prioridad, categoria)


    def delete_task(self, task_id):
        """
        Marcar una tarea como eliminada (HU014, HU017).

        Args:
            task_id (int): ID de la tarea.
        """
        self.controller.delete_task(task_id)

    def restore_task(self, task_id):
        """
        Restaurar una tarea previamente eliminada (HU017).

        Args:
            task_id (int): ID de la tarea.
        """
        self.controller.restore_task(task_id)

    def complete_task(self, task_id):
        """
        Marcar una tarea como completada (HU005).

        Args:
            task_id (int): ID de la tarea.
        """
        self.controller.complete_task(task_id)

    def favorite_task(self, task_id, is_favorite=True):
        """
        Marcar o desmarcar una tarea como favorita (HU015).

        Args:
            task_id (int): ID de la tarea.
            is_favorite (bool): True para marcar como favorita.
        """
        self.controller.favorite_task(task_id, is_favorite)

    def filter_tasks(self, estado=None, prioridad=None, categoria=None):
        """
        Filtrar tareas por estado, prioridad y/o categoría (HU010).

        Args:
            estado (str): 'completadas' o 'pendientes'.
            prioridad (str): 'alta', 'media' o 'baja'.
            categoria (str): 'trabajo', 'hogar' o 'estudio'.

        Returns:
            list: Lista de tareas filtradas.
        """
        return self.controller.filter_tasks(estado, prioridad, categoria)

    def search_tasks(self, keyword):
        """
        Buscar tareas por palabra clave en título o descripción (HU011).

        Args:
            keyword (str): Palabra clave a buscar.

        Returns:
            list: Lista de tareas que coincidan con la búsqueda.
        """
        return self.controller.search_tasks(keyword)
    def restore_task(self, task_id):
        self.controller.restore_task(task_id)

    def permanently_delete_task(self, task_id):
        """Elimina una tarea de la base de datos de forma permanente."""
        self.controller.session.query(Tarea).filter_by(id=task_id).delete()
        self.controller.session.commit()

    def get_favorite_tasks(self):
        return self.session.query(Tarea).filter_by(is_favorite=True).all()

    
 



