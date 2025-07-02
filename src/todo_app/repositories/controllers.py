"""
Controlador de tareas.

Este módulo implementa la clase TaskController, que permite gestionar
las tareas almacenadas en la base de datos: crear, actualizar, eliminar,
filtrar, buscar, marcar como favoritas o completadas, entre otras acciones.

Historias de Usuario: HU005 - HU018
"""

from todo_app.models.models import Session, Tarea as Task, NivelPrioridad, Categoria


class TaskController:
    """Controlador para gestionar operaciones CRUD sobre tareas."""

    def __init__(self):
        """Inicializa una nueva sesión de base de datos."""
        self.session = Session()

    def add_task(self, title, description, due_date, prioridad='media', categoria=None):
        """
        Crear una nueva tarea (HU005, HU006, HU007).

        Args:
            title (str): Título de la tarea.
            description (str): Descripción de la tarea.
            due_date (date): Fecha de vencimiento.
            prioridad (str): Nivel de prioridad ('baja', 'media', 'alta').
            categoria (str): Categoría de la tarea ('trabajo', 'hogar', 'estudio').
        """
        task = Task(
            titulo=title,
            descripcion=description,
            fecha_vencimiento=due_date,
            prioridad=NivelPrioridad[prioridad],
            categoria=Categoria[categoria] if categoria else None
        )
        self.session.add(task)
        self.session.commit()

    def get_tasks(self, include_deleted=False):
        """
        Obtener todas las tareas activas (HU010).

        Args:
            include_deleted (bool): Si es True, también incluye tareas eliminadas.

        Returns:
            list: Lista de tareas.
        """
        query = self.session.query(Task)
        if not include_deleted:
            query = query.filter(Task.eliminada.is_(False))
        return query.all()

    def update_task(self, task_id, title=None, description=None, due_date=None, prioridad=None, categoria=None):
        """
        Actualiza los campos de una tarea existente (incluye prioridad y categoría).

        Args:
            task_id (int): ID de la tarea.
            title (str): Nuevo título.
            description (str): Nueva descripción.
            due_date (date): Nueva fecha de vencimiento.
            prioridad (str): Nueva prioridad ('baja', 'media', 'alta').
            categoria (str): Nueva categoría ('trabajo', 'hogar', 'estudio').
        """
        task = self.session.query(Task).get(task_id)
        if task and not task.eliminada:
            if title:
                task.titulo = title
            if description:
                task.descripcion = description
            if due_date:
                task.fecha_vencimiento = due_date
            if prioridad:
                task.prioridad = NivelPrioridad[prioridad]
            if categoria:
                task.categoria = Categoria[categoria]
            self.session.commit()


    def delete_task(self, task_id):
        """
        Marcar una tarea como eliminada (HU014, HU017).

        Args:
            task_id (int): ID de la tarea.
        """
        task = self.session.query(Task).get(task_id)
        if task:
            task.eliminada = True
            self.session.commit()

    def complete_task(self, task_id):
        """
        Marcar una tarea como completada (HU005).

        Args:
            task_id (int): ID de la tarea.
        """
        task = self.session.query(Task).get(task_id)
        if task:
            task.completada = True
            self.session.commit()

    def favorite_task(self, task_id, is_favorite=True):
        """
        Marcar o desmarcar una tarea como favorita (HU015).

        Args:
            task_id (int): ID de la tarea.
            is_favorite (bool): True si se desea marcar como favorita.
        """
        task = self.session.query(Task).get(task_id)
        if task:
            task.favorita = is_favorite
            self.session.commit()

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
        query = self.session.query(Task).filter(Task.eliminada.is_(False))

        if estado == "completadas":
            query = query.filter(Task.completada.is_(True))
        elif estado == "pendientes":
            query = query.filter(Task.completada.is_(False))

        if prioridad:
            query = query.filter(Task.prioridad == NivelPrioridad[prioridad])

        if categoria:
            query = query.filter(Task.categoria == Categoria[categoria])

        return query.all()

    def search_tasks(self, keyword):
        """
        Buscar tareas por palabra clave en título o descripción (HU011).

        Args:
            keyword (str): Palabra clave a buscar.

        Returns:
            list: Lista de tareas que coincidan con la búsqueda.
        """
        return self.session.query(Task).filter(
            (Task.titulo.ilike(f"%{keyword}%") | Task.descripcion.ilike(f"%{keyword}%")),
            Task.eliminada.is_(False)
        ).all()
    def restore_task(self, task_id):
        task = self.session.query(Task).get(task_id)
        if task and task.eliminada:
            task.eliminada = False
            self.session.commit()
