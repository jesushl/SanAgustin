from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class LugarVisita(Base):
    __tablename__ = "lugares_visita"
    
    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String, unique=True)
    descripcion = Column(String)
    capacidad = Column(Integer, default=1)
    
    # Relaciones
    reservas = relationship("ReservaVisita", back_populates="lugar_visita")
