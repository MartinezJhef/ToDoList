"""
Funciones auxiliares y utilidades generales para la aplicación.
"""

import os
import sys
from PyQt5.QtCore import QFile, QTextStream


def resource_path(relative_path: str) -> str:
    """
    Obtiene la ruta absoluta de un recurso, útil si se compila con pyinstaller.

    Args:
        relative_path (str): Ruta relativa dentro de la carpeta del proyecto.

    Returns:
        str: Ruta absoluta al recurso.
    """
    base_path = getattr(
        sys, "_MEIPASS", os.path.abspath(".")
    )  # para pyinstaller; si no, usa pwd
    return os.path.join(base_path, relative_path)


def load_qss(path: str) -> str:
    """
    Lee un archivo .qss y devuelve su contenido como cadena.

    Args:
        path (str): Ruta al archivo .qss.

    Returns:
        str: Contenido del QSS.
    """
    if not os.path.exists(path):
        return ""
    file = QFile(path)
    if not file.open(QFile.ReadOnly | QFile.Text):
        return ""
    stream = QTextStream(file)
    qss = stream.readAll()
    file.close()
    return qss
