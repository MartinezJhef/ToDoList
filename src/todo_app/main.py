from todo_app.views import MainWindow
from PyQt5.QtWidgets import QApplication
import sys
import os

if __name__ == '__main__':
    """
    Punto de entrada principal de la aplicación To-Do List.

    Inicializa la aplicación Qt, carga la hoja de estilos (QSS) desde el archivo
    correspondiente y muestra la ventana principal de la interfaz gráfica.
    """
    app = QApplication(sys.argv)

    # Cargar hoja de estilos (QSS)
    style_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'styles', 'dark.qss'))
    with open(style_path, 'r') as f:
        style = f.read()
        app.setStyleSheet(style)

    # Crear y mostrar ventana principal
    window = MainWindow()
    window.show()

    # Ejecutar bucle principal de la aplicación
    sys.exit(app.exec_())
