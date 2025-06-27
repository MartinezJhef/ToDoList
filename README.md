# 📝 To-Do List App

Una aplicación de lista de tareas desarrollada con **Python**, **PyQt5** y **SQLAlchemy**, que permite a los usuarios gestionar sus actividades diarias desde una interfaz gráfica moderna, intuitiva y funcional.

---

## 📂 Estructura del Proyecto

```
src/
└── todo_app/
    ├── models/               # Modelos y ORM
    │   └── models.py
    ├── repositories/         # Lógica de acceso a datos
    │   └── controllers.py
    ├── services/             # Lógica de negocio
    │   └── task_service.py
    ├── ui/                   # Interfaz de usuario y lógica de presentación
    │   ├── main_window.ui
    │   ├── main_window_ui.py
    │   ├── views.py
    │   └── utils.py
    ├── tests/                # Pruebas unitarias
    │   └── test_controllers.py
    └── main.py               # Punto de entrada de la aplicación
```

---

## 🚀 Características Principales

- ✅ Crear tareas con título, descripción, prioridad, categoría y fecha límite.
- 🗂 Visualizar y clasificar tareas por estado, categoría o prioridad.
- ✏ Editar tareas ya existentes.
- ❌ Eliminar tareas de forma lógica (papelera).
- 📌 Marcar tareas como favoritas.
- 🔔 Agregar recordatorios con fecha y hora.
- 🗃 Filtrar tareas por estado, prioridad o categoría.
- 🔍 Buscar tareas por palabras clave.
- 📊 Visualizar un resumen del progreso (dashboard).
- 🎨 Interfaz moderna y responsive con soporte de tema oscuro.
- 🧪 Pruebas automatizadas para asegurar calidad y consistencia.

---

## 🛠 Tecnologías Utilizadas

| Tecnología   | Función Principal                                 |
|--------------|---------------------------------------------------|
| Python       | Lenguaje de programación base                     |
| PyQt5        | Construcción de la interfaz gráfica de escritorio |
| SQLAlchemy   | ORM para interacción con la base de datos         |
| SQLite       | Base de datos local embebida                      |
| Unittest     | Framework de pruebas unitarias                    |

---

## 📥 Instalación

```bash
# Clona el repositorio
git clone https://github.com/MartinezJhef/ToDoList.git
cd ToDoList

# (Opcional) Crea y activa un entorno virtual
python -m venv venv
venv\Scripts\activate      # En Windows
source venv/bin/activate   # En macOS/Linux

# Instala las dependencias
pip install -r requirements.txt
```

---

## ▶ Ejecución de la Aplicación

```bash
cd src
python main.py
```

Se abrirá la ventana principal para comenzar a gestionar tus tareas.

---

## 🧪 Ejecutar Pruebas Unitarias

```bash
cd src
python -m todo_app.tests.test_controllers
```

Esto ejecutará las pruebas CRUD sobre tareas, utilizando una base de datos SQLite temporal en memoria.

---

## 🧱 Estructura de la Base de Datos (Resumen)

**Tabla: tareas**

| Campo         | Tipo     | Descripción                            |
|---------------|----------|----------------------------------------|
| id            | Integer  | ID único (PK)                          |
| titulo        | String   | Título de la tarea                     |
| descripcion   | String   | Descripción adicional (opcional)       |
| fecha_vencimiento | Date | Fecha límite                           |
| completada    | Boolean  | Estado de finalización                 |
| prioridad     | Enum     | Nivel de prioridad: baja, media, alta  |
| categoria     | Enum     | Contexto: trabajo, hogar, estudio      |
| favorita      | Boolean  | Marcada como favorita                  |
| eliminada     | Boolean  | Indicador de eliminación lógica        |
| creada_en     | DateTime | Fecha de creación                      |
| actualizada_en| DateTime | Última modificación                    |

---

## 💡 Recomendaciones

- Ejecutar siempre desde la carpeta `src` para evitar errores de importación.
- Si se empaqueta con `PyInstaller`, asegurarse de incluir correctamente los archivos `.qss` desde `utils`.

---

## 🚧 Ideas Futuras

- Implementar autenticación y gestión de usuarios.
- Añadir sincronización en la nube.
- Migración a bases de datos robustas como PostgreSQL.
- Crear versión web (Flask) o móvil (Flutter).

---

## 👨‍💻 Autores

- Martinez Jheferson  
- Miranda Mario  
- Ortega Pedro  
- Rojas Angela  

Desarrollado como parte del curso de **Programación en Python (2025)**.
