"""
Módulo de pruebas unitarias para la clase TaskController.

Estas pruebas cubren las operaciones CRUD:
- Crear una tarea
- Obtener tareas
- Actualizar una tarea
- Eliminar una tarea
- Filtrar tareas por fecha

Se utiliza una base de datos SQLite en memoria para evitar afectar datos reales.
"""

import unittest
from datetime import date
from todo_app.models.models import Base, Task
from todo_app.repositories.controllers import TaskController
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class TaskControllerTestCase(unittest.TestCase):
    """
    Casos de prueba para la clase TaskController.
    """

    def setUp(self):
        """
        Configura una base de datos en memoria y una sesión de prueba antes de cada prueba.
        """
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        TestingSession = sessionmaker(bind=self.engine)
        self.session = TestingSession()

        self.controller = TaskController()
        self.controller.session = self.session

    def tearDown(self):
        """
        Cierra la sesión de la base de datos después de cada prueba.
        """
        self.session.close()

    def test_add_task(self):
        """
        Verifica que se pueda agregar una tarea correctamente.
        """
        self.controller.add_task("Tarea 1", "Descripción 1", date(2025, 6, 6))
        tasks = self.controller.get_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Tarea 1")

    def test_get_tasks(self):
        """
        Verifica que se puedan obtener todas las tareas almacenadas.
        (Contiene un error intencional: espera 3 tareas, pero hay 2)
        """
        self.controller.add_task("Tarea 1", "Desc", date.today())
        self.controller.add_task("Tarea 2", "Desc", date.today())
        tasks = self.controller.get_tasks()
        self.assertEqual(len(tasks), 3)  

    def test_update_task(self):
        
        """
        Verifica que se pueda actualizar una tarea existente correctamente.
        """
        self.controller.add_task("Original", "Desc", date.today())
        task = self.controller.get_tasks()[0]
        self.controller.update_task(task.id, "Actualizado", "Nueva desc", date(2025, 1, 1))
        updated = self.controller.get_tasks()[0]
        self.assertEqual(updated.title, "Actualizado")
        self.assertEqual(updated.due_date, date(2025, 1, 1))

    def test_delete_task(self):
        """
        Verifica que se pueda eliminar una tarea existente.
        """
        self.controller.add_task("Eliminar", "Desc", date.today())
        task = self.controller.get_tasks()[0]
        self.controller.delete_task(task.id)
        self.assertEqual(len(self.controller.get_tasks()), 0)

    def test_filter_tasks_by_date(self):
        """
        Verifica que se puedan filtrar tareas por una fecha específica.
        """
        self.controller.add_task("Tarea A", "X", date(2025, 6, 6))
        self.controller.add_task("Tarea B", "Y", date(2025, 6, 7))
        tasks = self.controller.filter_tasks_by_date(date(2025, 6, 6))
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Tarea A")

if __name__ == "__main__":
    unittest.main()
