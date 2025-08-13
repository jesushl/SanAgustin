from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Estacionamiento(Base):
    __tablename__ = "estacionamientos"
    
    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String, unique=True)
    placa = Column(String)
    modelo_auto = Column(String)
    color_auto = Column(String)
    es_visita = Column(Boolean, default=False)
    departamento_id = Column(Integer, ForeignKey("departamentos.id"))
    
    # Relaciones
    departamento = relationship("Departamento", back_populates="estacionamientos")
