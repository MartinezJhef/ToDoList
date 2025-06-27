"""
Módulo de pruebas unitarias para la clase TaskController.

Estas pruebas cubren:
- Crear, obtener, actualizar y eliminar tareas
- Restaurar, completar, marcar como favorita
- Buscar por palabra clave
- Filtrar por estado, prioridad y categoría
- Casos adicionales como tareas sin categoría o restaurar no eliminadas

Se utiliza una base de datos SQLite en memoria para aislamiento de pruebas.
"""

import unittest
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from todo_app.models.models import Base, NivelPrioridad, Categoria
from todo_app.repositories.controllers import TaskController


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
        """Cierra la sesión al finalizar cada prueba."""
        self.session.close()

    def test_add_task(self):
        """Debe agregar una tarea correctamente."""
        self.controller.add_task("Tarea 1", "Desc 1", date.today())
        tasks = self.controller.get_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].titulo, "Tarea 1")

    def test_get_tasks(self):
        """Debe retornar todas las tareas activas."""
        self.controller.add_task("Tarea 1", "Desc", date.today())
        self.controller.add_task("Tarea 2", "Desc", date.today())
        tasks = self.controller.get_tasks()
        self.assertEqual(len(tasks), 2)

    def test_update_task(self):
        """Debe actualizar título, descripción y fecha de vencimiento."""
        self.controller.add_task("Original", "Desc", date.today())
        task = self.controller.get_tasks()[0]
        self.controller.update_task(task.id, "Nuevo", "Actualizado", date(2025, 1, 1))
        updated = self.controller.get_tasks()[0]
        self.assertEqual(updated.titulo, "Nuevo")
        self.assertEqual(updated.fecha_vencimiento, date(2025, 1, 1))

    def test_delete_and_restore_task(self):
        """Debe eliminar lógicamente y luego restaurar una tarea."""
        self.controller.add_task("Eliminar", "Desc", date.today())
        task = self.controller.get_tasks()[0]
        self.controller.delete_task(task.id)
        self.assertEqual(len(self.controller.get_tasks()), 0)

        self.controller.restore_task(task.id)
        self.assertEqual(len(self.controller.get_tasks()), 1)

    def test_complete_task(self):
        """Debe marcar una tarea como completada."""
        self.controller.add_task("Completar", "Desc", date.today())
        task = self.controller.get_tasks()[0]
        self.controller.complete_task(task.id)
        self.assertTrue(self.controller.get_tasks()[0].completada)

    def test_favorite_task(self):
        """Debe marcar una tarea como favorita."""
        self.controller.add_task("Favorita", "Desc", date.today())
        task = self.controller.get_tasks()[0]
        self.controller.favorite_task(task.id, True)
        self.assertTrue(self.controller.get_tasks()[0].favorita)

    def test_search_tasks(self):
        """Debe buscar correctamente por palabra clave en título o descripción."""
        self.controller.add_task("Buscar esto", "Descripción interesante", date.today())
        self.controller.add_task("Otro título", "Nada relevante", date.today())
        results = self.controller.search_tasks("esto")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].titulo, "Buscar esto")

    def test_filter_tasks(self):
        """Debe filtrar por estado pendiente y prioridad alta."""
        self.controller.add_task("Alta", "Importante", date.today(), prioridad='alta', categoria='trabajo')
        self.controller.add_task("Media", "Normal", date.today(), prioridad='media', categoria='hogar')
        filtered = self.controller.filter_tasks(estado="pendientes", prioridad="alta")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].prioridad, NivelPrioridad.alta)

    # 🔁 PRUEBAS ADICIONALES

    def test_restore_non_deleted_task(self):
        """Restaurar una tarea no eliminada no debe cambiar su estado."""
        self.controller.add_task("Activa", "No eliminada", date.today())
        task = self.controller.get_tasks()[0]
        self.controller.restore_task(task.id)
        restored = self.controller.get_tasks()[0]
        self.assertFalse(restored.eliminada)

    def test_update_priority_and_category(self):
        """Debe actualizar la prioridad y la categoría de una tarea."""
        self.controller.add_task("Cambiar", "Test", date.today())
        task = self.controller.get_tasks()[0]
        self.controller.update_task(task.id, prioridad='alta', categoria='estudio')
        updated = self.controller.get_tasks()[0]
        self.assertEqual(updated.prioridad, NivelPrioridad.alta)
        self.assertEqual(updated.categoria, Categoria.estudio)

    def test_filter_by_category_only(self):
        """Debe filtrar correctamente solo por categoría."""
        self.controller.add_task("Estudiar", "Mate", date.today(), categoria='estudio')
        self.controller.add_task("Limpiar", "Casa", date.today(), categoria='hogar')
        filtered = self.controller.filter_tasks(categoria='hogar')
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].categoria, Categoria.hogar)

    def test_add_task_without_category(self):
        """Debe permitir crear una tarea sin categoría."""
        self.controller.add_task("Sin categoría", "Prueba", date.today())
        task = self.controller.get_tasks()[0]
        self.assertIsNone(task.categoria)

    def test_filter_by_completed_state(self):
        """Debe filtrar correctamente las tareas completadas."""
        self.controller.add_task("Tarea A", "Desc", date.today())
        self.controller.add_task("Tarea B", "Desc", date.today())
        task_b = self.controller.get_tasks()[1]
        self.controller.complete_task(task_b.id)
        completadas = self.controller.filter_tasks(estado="completadas")
        self.assertEqual(len(completadas), 1)
        self.assertTrue(completadas[0].completada)


if __name__ == '__main__':
    unittest.main()
