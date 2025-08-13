from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class ReservaVisita(Base):
    __tablename__ = "reservas_visita"
    
    id = Column(Integer, primary_key=True, index=True)
    lugar_visita_id = Column(Integer, ForeignKey("lugares_visita.id"))
    departamento_id = Column(Integer, ForeignKey("departamentos.id"))
    placa_visita = Column(String, nullable=True)
    periodo_inicio = Column(DateTime)
    periodo_fin = Column(DateTime)
    estado = Column(String, default="activa")  # activa, cancelada, completada
    
    # Relaciones
    lugar_visita = relationship("LugarVisita", back_populates="reservas")
    departamento = relationship("Departamento", back_populates="reservas_visita")
