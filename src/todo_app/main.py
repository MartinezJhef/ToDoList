from todo_app.views import MainWindow
from PyQt5.QtWidgets import QApplication
import sys
import os

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Cargar hoja de estilos (QSS)
    style_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'styles', 'dark.qss'))
    with open(style_path, 'r') as f:
        style = f.read()
        app.setStyleSheet(style)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
