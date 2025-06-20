# 📝 To-Do List App

Una aplicación de lista de tareas desarrollada con **Python**, **PyQt5** y **SQLAlchemy**, que permite a los usuarios **crear, visualizar, actualizar, eliminar y filtrar tareas** mediante una interfaz gráfica amigable y moderna.

---

## 📦 Estructura del Proyecto

```
todolist/
├── src/
│   └── todo_app/
│       ├── __init__.py 
│       ├── controllers.py    
│       ├── models.py      
│       ├── views.py       
│       ├── utils.py        
│       ├── tests/          
│       │   └── test_controllers.py
│       └── main.py         
├── requirements.txt
└── README.md
```

---

## 🚀 Características Principales

- ✅ Crear tareas con título, descripción y fecha límite.
- 🗂 Visualizar todas las tareas en una lista organizada.
- ✏ Editar tareas existentes.
- ❌ Eliminar tareas innecesarias.
- 🗓 Filtrar tareas por fecha.
- 🔔 Añadir recordatorios.
- 📌 Marcar tareas como favoritas.
- 📊 Visualizar resumen de progreso.
- 🔍 Buscar y filtrar por prioridad o categoría.
- 🎨 Interfaz moderna con tema oscuro.
- 🧪 Pruebas unitarias automatizadas (CRUD).

---

## 🛠 Tecnologías Utilizadas

| Tecnología   | Propósito principal                              |
|--------------|--------------------------------------------------|
| Python       | Lenguaje base del proyecto                       |
| PyQt5        | Desarrollo de interfaz gráfica de escritorio     |
| SQLAlchemy   | ORM para manejar la base de datos SQLite         |
| SQLite       | Base de datos embebida, liviana y local          |
| Unittest     | Validación de la lógica con pruebas unitarias    |

---

## 📥 Instalación

1. **Clona el repositorio**
```bash
git clone https://github.com/MartinezJhef/ToDoList.git
cd todolist
```

2. **Crea un entorno virtual (opcional pero recomendado)**
```bash
python -m venv venv
venv\Scripts\activate    # En Windows
source venv/bin/activate # En macOS/Linux
```

3. **Instala las dependencias**
```bash
pip install -r requirements.txt
```

---

## ▶ Ejecución de la Aplicación

```bash
cd src
python main.py
```

La interfaz gráfica se abrirá para que puedas empezar a gestionar tus tareas.

---

## 🧪 Ejecutar Pruebas Unitarias

```bash
cd src
python -m todo_app.tests.test_controllers
```

Se ejecutarán pruebas sobre agregar, obtener, actualizar, eliminar y filtrar tareas, utilizando una base de datos temporal en memoria (`sqlite:///:memory:`).

---

## 🧱 Estructura de la Base de Datos

**Tabla: `tasks`**

| Campo         | Tipo     | Descripción                             |
|---------------|----------|-----------------------------------------|
| `id`          | Integer  | ID único de la tarea (clave primaria)   |
| `title`       | String   | Título de la tarea (requerido)          |
| `description` | String   | Descripción opcional                    |
| `due_date`    | Date     | Fecha límite de la tarea                |

---

## 📌 Recomendaciones Finales

- Ejecuta siempre desde la carpeta `src` para evitar errores de importación.
- Si empaquetas con PyInstaller, incluye `utils/helpers.py` para que los estilos `.qss` carguen correctamente.

### 💡 Ideas para mejoras

- Añadir persistencia con PostgreSQL o MySQL.
- Sincronización en la nube.
- Versión web o móvil usando Flask o Flutter.

---

## 👨‍💻 Autores

- Martinez Jheferson  
- Miranda Mario  
- Ortega Pedro  
- Rojas Angela  

Desarrollado como parte del curso de **Programación en Python (2025)**.
