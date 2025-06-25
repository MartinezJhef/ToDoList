"""
Modelos de datos para la aplicación de gestión de tareas.

Este módulo define las entidades: Tarea, Recordatorio y PreferenciasUsuario,
utilizando SQLAlchemy para mapearlas a una base de datos SQLite.
"""

from sqlalchemy import (
    Column, Integer, String, DateTime, Date, Boolean, Enum, ForeignKey, create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import enum

# Base de datos ORM
Base = declarative_base()


class NivelPrioridad(enum.Enum):
    """Enum que representa los niveles de prioridad de una tarea."""
    baja = "Baja"
    media = "Media"
    alta = "Alta"


class Categoria(enum.Enum):
    """Enum que representa las categorías posibles de una tarea."""
    trabajo = "Trabajo"
    hogar = "Hogar"
    estudio = "Estudio"


class Tarea(Base):
    """
    Modelo que representa una tarea del usuario.

    Atributos:
        id (int): Identificador único de la tarea.
        titulo (str): Título de la tarea.
        descripcion (str): Descripción opcional.
        fecha_vencimiento (date): Fecha límite de la tarea.
        completada (bool): Estado de finalización.
        prioridad (NivelPrioridad): Nivel de prioridad.
        categoria (Categoria): Categoría asociada.
        favorita (bool): Indicador si es favorita.
        eliminada (bool): Indicador si fue eliminada.
        creada_en (datetime): Fecha de creación.
        actualizada_en (datetime): Última fecha de modificación.
        recordatorios (List[Recordatorio]): Lista de recordatorios vinculados.
    """
    __tablename__ = 'tareas'

    id = Column(Integer, primary_key=True)
    titulo = Column(String, nullable=False)
    descripcion = Column(String)
    fecha_vencimiento = Column(Date)

    completada = Column(Boolean, default=False)
    prioridad = Column(Enum(NivelPrioridad), default=NivelPrioridad.media)
    categoria = Column(Enum(Categoria), nullable=True)
    favorita = Column(Boolean, default=False)
    eliminada = Column(Boolean, default=False)
    creada_en = Column(DateTime, default=datetime.utcnow)
    actualizada_en = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    recordatorios = relationship(
        "Recordatorio",
        back_populates="tarea",
        cascade="all, delete-orphan"
    )


class Recordatorio(Base):
    """
    Modelo que representa un recordatorio asociado a una tarea.

    Atributos:
        id (int): Identificador único.
        tarea_id (int): ID de la tarea a la que pertenece.
        fecha_hora (datetime): Fecha y hora del recordatorio.
        notificado (bool): Indicador de si ya fue notificado.
        tarea (Tarea): Objeto de la tarea asociada.
    """
    __tablename__ = 'recordatorios'

    id = Column(Integer, primary_key=True)
    tarea_id = Column(Integer, ForeignKey('tareas.id'))
    fecha_hora = Column(DateTime)
    notificado = Column(Boolean, default=False)

    tarea = relationship("Tarea", back_populates="recordatorios")


class PreferenciasUsuario(Base):
    """
    Modelo que representa las preferencias del usuario.

    Atributos:
        id (int): Identificador único.
        idioma (str): Idioma preferido del usuario.
        tema (str): Tema visual (claro/oscuro).
        notificaciones_activadas (bool): Preferencia de notificaciones.
    """
    __tablename__ = 'preferencias_usuario'

    id = Column(Integer, primary_key=True)
    idioma = Column(String, default="es")
    tema = Column(String, default="claro")
    notificaciones_activadas = Column(Boolean, default=True)


# Configuración de la base de datos SQLite
engine = create_engine('sqlite:///tareas.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
