from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class AreaComun(Base):
    __tablename__ = "areas_comunes"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String)
    ubicacion = Column(String)
    capacidad = Column(Integer, default=1)
    
    # Relaciones
    reservas = relationship("ReservaAreaComun", back_populates="area_comun")
