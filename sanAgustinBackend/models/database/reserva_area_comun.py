from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class ReservaAreaComun(Base):
    __tablename__ = "reservas_area_comun"
    
    id = Column(Integer, primary_key=True, index=True)
    area_comun_id = Column(Integer, ForeignKey("areas_comunes.id"))
    departamento_id = Column(Integer, ForeignKey("departamentos.id"))
    periodo_inicio = Column(DateTime)
    periodo_fin = Column(DateTime)
    estado = Column(String, default="activa")  # activa, cancelada, completada
    
    # Relaciones
    area_comun = relationship("AreaComun", back_populates="reservas")
    departamento = relationship("Departamento", back_populates="reservas_area_comun")
