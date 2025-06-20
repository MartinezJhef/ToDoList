from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QPushButton, QListWidgetItem, QMessageBox
from PyQt5.QtCore import QDate
from todo_app.repositories.controllers import TaskController
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
        self.controller = TaskController()
        self.input_due_date.setDate(QDate(2025, 6, 20))

        self.btn_add.clicked.connect(self.create_task)
        self.btn_update.clicked.connect(self.update_task)
        self.btn_delete.clicked.connect(self.delete_task)
        self.btn_filter.clicked.connect(self.filter_tasks)

        self.load_tasks()

    def create_task(self):
        title = self.input_title.text()
        description = self.input_description.toPlainText()
        due_date = self.input_due_date.date().toPyDate()
        if not title:
            QMessageBox.warning(self, "Error", "El título es obligatorio.")
            return
        self.controller.add_task(title, description, due_date)
        self.load_tasks()

    def load_tasks(self, tasks=None):
        if tasks is None:
            tasks = self.controller.get_tasks()
        self.list_tasks.clear()
        for task in tasks:
            item_text = f"»» {task.title}\n🗒️ {task.description} \n📅 {task.due_date.strftime('%d-%m-%Y')}"
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
        self.controller.update_task(task_id, title, description, due_date)
        self.load_tasks()

    def delete_task(self):
        item = self.list_tasks.currentItem()
        if item is None:
            return
        task_id = item.data(1000)
        self.controller.delete_task(task_id)
        self.load_tasks()

    def filter_tasks(self):
        date = self.input_due_date.date().toPyDate()
        tasks = self.controller.filter_tasks_by_date(date)
        self.load_tasks(tasks)