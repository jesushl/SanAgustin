from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from repositories.departamento_repository import DepartamentoRepository
from repositories.estacionamiento_repository import EstacionamientoRepository
from models.schemas.estacionamiento import EstacionamientoResponse, EstacionamientoUpdate

class EstacionamientoService:
    def __init__(self):
        self.departamento_repo = DepartamentoRepository()
        self.estacionamiento_repo = EstacionamientoRepository()

    def update_estacionamiento(self, db: Session, estacionamiento_id: int, usuario_id: int, datos: EstacionamientoUpdate) -> EstacionamientoResponse:
        """Actualiza los datos del vehículo del residente"""
        # Verificar que el estacionamiento pertenece al usuario
        departamento = self.departamento_repo.get_by_usuario_id(db, usuario_id)
        if not departamento:
            raise HTTPException(status_code=404, detail="No se encontró departamento asociado al usuario")
        
        estacionamiento = self.estacionamiento_repo.get_by_departamento_id(db, departamento.id, es_visita=False)
        if not estacionamiento or estacionamiento.id != estacionamiento_id:
            raise HTTPException(status_code=404, detail="Estacionamiento no encontrado")
        
        # Actualizar datos
        datos_dict = {k: v for k, v in datos.dict().items() if v is not None}
        updated_estacionamiento = self.estacionamiento_repo.update(db, db_obj=estacionamiento, obj_in=datos_dict)
        
        return EstacionamientoResponse.from_orm(updated_estacionamiento)
