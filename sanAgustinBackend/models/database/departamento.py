from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Departamento(Base):
    __tablename__ = "departamentos"
    
    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String, index=True, unique=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="departamento")
    estacionamientos = relationship("Estacionamiento", back_populates="departamento")
    adeudos = relationship("Adeudo", back_populates="departamento")
    reservas_area_comun = relationship("ReservaAreaComun", back_populates="departamento")
    reservas_visita = relationship("ReservaVisita", back_populates="departamento")
