from sqlalchemy import (
    Column, Integer, String, DateTime, Date, Boolean, Enum, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
import enum
from datetime import datetime

Base = declarative_base()

# ---------- ENUMS ----------
class NivelPrioridad(enum.Enum):
    baja = "Baja"
    media = "Media"
    alta = "Alta"

class Categoria(enum.Enum):
    trabajo = "Trabajo"
    hogar = "Hogar"
    estudio = "Estudio"

# ---------- TAREA ----------
class Tarea(Base):
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

    recordatorios = relationship("Recordatorio", back_populates="tarea", cascade="all, delete-orphan")

# ---------- RECORDATORIO ----------
class Recordatorio(Base):
    __tablename__ = 'recordatorios'

    id = Column(Integer, primary_key=True)
    tarea_id = Column(Integer, ForeignKey('tareas.id'))
    fecha_hora = Column(DateTime)
    notificado = Column(Boolean, default=False)

    tarea = relationship("Tarea", back_populates="recordatorios")

# ---------- PREFERENCIAS ----------
class PreferenciasUsuario(Base):
    __tablename__ = 'preferencias_usuario'

    id = Column(Integer, primary_key=True)
    idioma = Column(String, default="es")
    tema = Column(String, default="claro")
    notificaciones_activadas = Column(Boolean, default=True)

# ---------- CONFIGURACIÓN DE BASE DE DATOS ----------
engine = create_engine('sqlite:///tareas.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
