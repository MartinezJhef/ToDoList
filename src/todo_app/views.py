from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QPushButton, QListWidgetItem, QMessageBox
from PyQt5.QtCore import QDate
from todo_app.services.task_service import TaskService
from datetime import datetime
import os


class MainWindow(QMainWindow):
    """
    Ventana principal de la aplicación To-Do List.
    """
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), 'ui', 'main_window.ui')
        uic.loadUi(ui_path, self)

        self.service = TaskService()
        self.input_due_date.setDate(QDate(2025, 6, 25))

        self.btn_add.clicked.connect(self.create_task)
        self.btn_update.clicked.connect(self.update_task)
        self.btn_delete.clicked.connect(self.delete_task)
        self.btn_filter.clicked.connect(self.filter_tasks)
        self.btn_complete.clicked.connect(self.complete_task)
        self.btn_favorite.clicked.connect(self.favorite_task)
        


        self.load_tasks()

    def create_task(self):
        title = self.input_title.text()
        description = self.input_description.toPlainText()
        due_date = self.input_due_date.date().toPyDate()

        priority = self.input_priority.currentText().lower()  # 'baja', 'media', 'alta'
        category = self.input_category.currentText().lower()  # 'trabajo', 'hogar', 'estudio'

        if not title:
            QMessageBox.warning(self, "Error", "El título es obligatorio.")
            return

        self.service.create_task(title, description, due_date, priority, category)
        self.load_tasks()

    def load_tasks(self, tasks=None):
        if tasks is None:
            tasks = self.service.get_tasks()
        self.list_tasks.clear()
        for task in tasks:
            estado = "🟢 Completada" if task.completada else "🔴 Pendiente"
            estrella = "⭐" if task.favorita else ""
            prioridad = f"⚡{task.prioridad.value}" if task.prioridad else ""
            categoria = f"📂{task.categoria.value}" if task.categoria else ""
            vencimiento = task.fecha_vencimiento.strftime('%d-%m-%Y') if task.fecha_vencimiento else "Sin fecha"

            item_text = f"{estrella} {task.titulo}\n🗒️ {task.descripcion}\n📅 {vencimiento}  |  {estado}  |  {prioridad}  |  {categoria}"
            item = QListWidgetItem(item_text)
            item.setData(1000, task.id)
            self.list_tasks.addItem(item)


    def update_task(self):
        item = self.list_tasks.currentItem()
        if item is None:
            return
        task_id = item.data(1000)
        title = self.input_title.text()
        description = self.input_description.toPlainText()
        due_date = self.input_due_date.date().toPyDate()

        priority = self.input_priority.currentText().lower()
        category = self.input_category.currentText().lower()

        self.service.update_task(task_id, title, description, due_date, priority, category)
        self.load_tasks()


    def delete_task(self):
        item = self.list_tasks.currentItem()
        if item is None:
            return
        task_id = item.data(1000)
        self.service.delete_task(task_id)
        self.load_tasks()

    def filter_tasks(self):
        date = self.input_due_date.date().toPyDate()
        all_tasks = self.service.get_tasks()
        filtered = [task for task in all_tasks if task.fecha_vencimiento == date]
        self.load_tasks(filtered)
    def complete_task(self):
        item = self.list_tasks.currentItem()
        if item is None:
            return
        task_id = item.data(1000)
        self.service.complete_task(task_id)
        self.load_tasks()

    def favorite_task(self):
        item = self.list_tasks.currentItem()
        if item is None:
            return
        task_id = item.data(1000)
        self.service.favorite_task(task_id, is_favorite=True)
        self.load_tasks()
    



