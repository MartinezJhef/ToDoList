"""
Módulo de pruebas unitarias para la clase TaskController.

Estas pruebas cubren las operaciones CRUD y funcionalidades clave:
- Crear una tarea
- Obtener tareas
- Actualizar una tarea
- Eliminar una tarea
- Restaurar tarea
- Completar tarea
- Marcar como favorita
- Buscar por palabra clave
- Filtrar tareas

Se utiliza una base de datos SQLite en memoria para evitar afectar datos reales.
"""

import unittest
from datetime import date
from todo_app.models.models import Base, NivelPrioridad, Categoria
from todo_app.repositories.controllers import TaskController
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class TaskControllerTestCase(unittest.TestCase):
    """Casos de prueba para la clase TaskController."""

    def setUp(self):
        """Configura una base de datos SQLite en memoria antes de cada prueba."""
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        TestingSession = sessionmaker(bind=engine)
        self.session = TestingSession()

        self.controller = TaskController()
        self.controller.session = self.session

    def tearDown(self):
        """Cierra la sesión después de cada prueba."""
        self.session.close()

    def test_add_task(self):
        self.controller.add_task("Tarea 1", "Desc 1", date.today())
        tasks = self.controller.get_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].titulo, "Tarea 1")

    def test_get_tasks(self):
        self.controller.add_task("Tarea 1", "Desc", date.today())
        self.controller.add_task("Tarea 2", "Desc", date.today())
        tasks = self.controller.get_tasks()
        self.assertEqual(len(tasks), 2)

    def test_update_task(self):
        self.controller.add_task("Original", "Desc", date.today())
        task = self.controller.get_tasks()[0]
        self.controller.update_task(task.id, "Nuevo", "Actualizado", date(2025, 1, 1))
        updated = self.controller.get_tasks()[0]
        self.assertEqual(updated.titulo, "Nuevo")
        self.assertEqual(updated.fecha_vencimiento, date(2025, 1, 1))

    def test_delete_and_restore_task(self):
        self.controller.add_task("Eliminar", "Desc", date.today())
        task = self.controller.get_tasks()[0]
        self.controller.delete_task(task.id)
        self.assertEqual(len(self.controller.get_tasks()), 0)

        self.controller.restore_task(task.id)
        self.assertEqual(len(self.controller.get_tasks()), 1)

    def test_complete_task(self):
        self.controller.add_task("Completar", "Desc", date.today())
        task = self.controller.get_tasks()[0]
        self.controller.complete_task(task.id)
        self.assertTrue(self.controller.get_tasks()[0].completada)

    def test_favorite_task(self):
        self.controller.add_task("Favorita", "Desc", date.today())
        task = self.controller.get_tasks()[0]
        self.controller.favorite_task(task.id, True)
        self.assertTrue(self.controller.get_tasks()[0].favorita)

    def test_search_tasks(self):
        self.controller.add_task("Buscar esto", "Descripción interesante", date.today())
        self.controller.add_task("Otro título", "Nada relevante", date.today())
        results = self.controller.search_tasks("esto")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].titulo, "Buscar esto")

    def test_filter_tasks(self):
        self.controller.add_task("Alta", "Importante", date.today(), prioridad='alta', categoria='trabajo')
        self.controller.add_task("Media", "Normal", date.today(), prioridad='media', categoria='hogar')

        completadas = self.controller.filter_tasks(estado="pendientes", prioridad="alta")
        self.assertEqual(len(completadas), 1)
        self.assertEqual(completadas[0].prioridad, NivelPrioridad.alta)


if __name__ == '__main__':
    unittest.main()
