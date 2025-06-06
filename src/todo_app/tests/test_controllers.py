# test_task_controller.py
import unittest
from datetime import date
from todo_app.models import Base, Task
from todo_app.controllers import TaskController
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class TaskControllerTestCase(unittest.TestCase):
    def setUp(self):
        # Base de datos en memoria para pruebas (no afecta tasks.db)
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        TestingSession = sessionmaker(bind=self.engine)
        self.session = TestingSession()

        # Inyectar sesión de prueba
        self.controller = TaskController()
        self.controller.session = self.session

    def tearDown(self):
        self.session.close()

    def test_add_task(self):
        self.controller.add_task("Tarea 1", "Descripción 1", date(2025, 6, 6))
        tasks = self.controller.get_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Tarea 1")

    def test_get_tasks(self):
        self.controller.add_task("Tarea 1", "Desc", date.today())
        self.controller.add_task("Tarea 2", "Desc", date.today())
        tasks = self.controller.get_tasks()
        self.assertEqual(len(tasks), 2)

    def test_update_task(self):
        self.controller.add_task("Original", "Desc", date.today())
        task = self.controller.get_tasks()[0]
        self.controller.update_task(task.id, "Actualizado", "Nueva desc", date(2025, 1, 1))
        updated = self.controller.get_tasks()[0]
        self.assertEqual(updated.title, "Actualizado")
        self.assertEqual(updated.due_date, date(2025, 1, 1))

    def test_delete_task(self):
        self.controller.add_task("Eliminar", "Desc", date.today())
        task = self.controller.get_tasks()[0]
        self.controller.delete_task(task.id)
        self.assertEqual(len(self.controller.get_tasks()), 0)

    def test_filter_tasks_by_date(self):
        self.controller.add_task("Tarea A", "X", date(2025, 6, 6))
        self.controller.add_task("Tarea B", "Y", date(2025, 6, 7))
        tasks = self.controller.filter_tasks_by_date(date(2025, 6, 6))
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Tarea A")

if __name__ == "__main__":
    unittest.main()




