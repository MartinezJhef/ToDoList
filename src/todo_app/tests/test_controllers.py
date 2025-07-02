"""
Módulo de pruebas unitarias para la clase TaskController.

Estas pruebas cubren:
- Crear, obtener, actualizar y eliminar tareas
- Restaurar, completar, marcar como favorita
- Buscar por palabra clave
- Filtrar por estado, prioridad y categoría
- Casos adicionales como tareas sin categoría o restaurar no eliminadas
- Casos extremos: duplicados, tareas ya completadas o eliminadas, filtros inválidos

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

    # FUNCIONALIDADES BÁSICAS

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
        filtered = self.controller.filter_tasks(estado="pendientes", prioridad="alta")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].prioridad, NivelPrioridad.alta)

    # FUNCIONALIDADES ADICIONALES

    def test_restore_non_deleted_task(self):
        self.controller.add_task("Activa", "No eliminada", date.today())
        task = self.controller.get_tasks()[0]
        self.controller.restore_task(task.id)
        restored = self.controller.get_tasks()[0]
        self.assertFalse(restored.eliminada)

    def test_update_priority_and_category(self):
        self.controller.add_task("Cambiar", "Test", date.today())
        task = self.controller.get_tasks()[0]
        self.controller.update_task(task.id, prioridad='alta', categoria='estudio')
        updated = self.controller.get_tasks()[0]
        self.assertEqual(updated.prioridad, NivelPrioridad.alta)
        self.assertEqual(updated.categoria, Categoria.estudio)

    def test_filter_by_category_only(self):
        self.controller.add_task("Estudiar", "Mate", date.today(), categoria='estudio')
        self.controller.add_task("Limpiar", "Casa", date.today(), categoria='hogar')
        filtered = self.controller.filter_tasks(categoria='hogar')
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].categoria, Categoria.hogar)

    def test_add_task_without_category(self):
        self.controller.add_task("Sin categoría", "Prueba", date.today())
        task = self.controller.get_tasks()[0]
        self.assertIsNone(task.categoria)

    def test_filter_by_completed_state(self):
        self.controller.add_task("Tarea A", "Desc", date.today())
        self.controller.add_task("Tarea B", "Desc", date.today())
        task_b = self.controller.get_tasks()[1]
        self.controller.complete_task(task_b.id)
        completadas = self.controller.filter_tasks(estado="completadas")
        self.assertEqual(len(completadas), 1)
        self.assertTrue(completadas[0].completada)

    # PRUEBAS EXTRA PARA ROBUSTEZ

    def test_add_duplicate_titles(self):
        self.controller.add_task("Duplicada", "Desc1", date.today())
        self.controller.add_task("Duplicada", "Desc2", date.today())
        tasks = self.controller.search_tasks("Duplicada")
        self.assertEqual(len(tasks), 2)

    def test_delete_already_deleted_task(self):
        self.controller.add_task("Eliminar dos veces", "Desc", date.today())
        task = self.controller.get_tasks()[0]
        self.controller.delete_task(task.id)
        self.controller.delete_task(task.id)
        self.assertEqual(len(self.controller.get_tasks()), 0)

    def test_complete_already_completed_task(self):
        self.controller.add_task("Ya completada", "Desc", date.today())
        task = self.controller.get_tasks()[0]
        self.controller.complete_task(task.id)
        self.controller.complete_task(task.id)
        self.assertTrue(self.controller.get_tasks()[0].completada)

    def test_favorite_toggle(self):
        self.controller.add_task("Alternar favorito", "Desc", date.today())
        task = self.controller.get_tasks()[0]
        self.controller.favorite_task(task.id, True)
        self.assertTrue(self.controller.get_tasks()[0].favorita)
        self.controller.favorite_task(task.id, False)
        self.assertFalse(self.controller.get_tasks()[0].favorita)

    def test_update_task_partial_fields(self):
        self.controller.add_task("Parcial", "Desc", date.today())
        task = self.controller.get_tasks()[0]
        self.controller.update_task(task.id, titulo="Solo nuevo título")
        updated = self.controller.get_tasks()[0]
        self.assertEqual(updated.titulo, "Solo nuevo título")
        self.assertEqual(updated.descripcion, "Desc")

    def test_add_task_with_past_due_date(self):
        past_date = date(2020, 1, 1)
        self.controller.add_task("Pasada", "Antigua", past_date)
        task = self.controller.get_tasks()[0]
        self.assertEqual(task.fecha_vencimiento, past_date)

    def test_filter_tasks_no_match(self):
        self.controller.add_task("Algo", "Desc", date.today(), prioridad='baja', categoria='hogar')
        result = self.controller.filter_tasks(prioridad='alta', categoria='estudio')
        self.assertEqual(len(result), 0)

    def test_search_case_insensitive(self):
        self.controller.add_task("Caso", "Descripción", date.today())
        result = self.controller.search_tasks("caso")
        self.assertEqual(len(result), 1)

    def test_delete_then_complete_should_fail(self):
        self.controller.add_task("Eliminar y completar", "Desc", date.today())
        task = self.controller.get_tasks()[0]
        self.controller.delete_task(task.id)
        self.controller.complete_task(task.id)
        completadas = self.controller.filter_tasks(estado="completadas")
        self.assertEqual(len(completadas), 0)

    def test_filter_pending_tasks(self):
        self.controller.add_task("Pendiente", "Desc", date.today())
        self.controller.add_task("Completa", "Desc", date.today())
        task = self.controller.get_tasks()[1]
        self.controller.complete_task(task.id)
        pendientes = self.controller.filter_tasks(estado="pendientes")
        self.assertEqual(len(pendientes), 1)
        self.assertFalse(pendientes[0].completada)

    def test_update_deleted_task_should_not_fail(self):
        self.controller.add_task("Eliminada", "Desc", date.today())
        task = self.controller.get_tasks()[0]
        self.controller.delete_task(task.id)
        try:
            self.controller.update_task(task.id, descripcion="Nuevo")
            updated = self.controller.session.get(type(task), task.id)
            self.assertTrue(updated.eliminada)
        except Exception as e:
            self.fail(f"Ocurrió una excepción inesperada: {e}")

    def test_add_multiple_tasks_and_filter_combo(self):
        self.controller.add_task("T1", "D", date.today(), prioridad='media', categoria='hogar')
        self.controller.add_task("T2", "D", date.today(), prioridad='media', categoria='hogar')
        task = self.controller.get_tasks()[1]
        self.controller.complete_task(task.id)
        result = self.controller.filter_tasks(estado="completadas", prioridad="media")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].titulo, "T2")

    def test_restore_then_delete_again(self):
        self.controller.add_task("Restaurar y eliminar", "Desc", date.today())
        task = self.controller.get_tasks()[0]
        self.controller.delete_task(task.id)
        self.controller.restore_task(task.id)
        self.assertEqual(len(self.controller.get_tasks()), 1)
        self.controller.delete_task(task.id)
        self.assertEqual(len(self.controller.get_tasks()), 0)

    def test_filter_tasks_invalid_estado(self):
        self.controller.add_task("Invalida", "Desc", date.today())
        result = self.controller.filter_tasks(estado="archivadas")
        self.assertEqual(result, [])

    def test_add_task_with_all_fields(self):
        self.controller.add_task("Completa", "Descripción completa", date.today(), prioridad='alta', categoria='estudio')
        task = self.controller.get_tasks()[0]
        self.assertEqual(task.titulo, "Completa")
        self.assertEqual(task.prioridad, NivelPrioridad.alta)
        self.assertEqual(task.categoria, Categoria.estudio)


if __name__ == '__main__':
    unittest.main()
