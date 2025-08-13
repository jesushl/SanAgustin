from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Adeudo(Base):
    __tablename__ = "adeudos"
    
    id = Column(Integer, primary_key=True, index=True)
    departamento_id = Column(Integer, ForeignKey("departamentos.id"))
    monto = Column(Float)
    descripcion = Column(String)
    fecha_vencimiento = Column(DateTime)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    pagado = Column(Boolean, default=False)
    
    # Relaciones
    departamento = relationship("Departamento", back_populates="adeudos")
