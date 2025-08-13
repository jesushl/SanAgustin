from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.estacionamiento_service import EstacionamientoService
from models.schemas.estacionamiento import EstacionamientoResponse, EstacionamientoUpdate
from core.database import get_db
from core.auth import get_current_user
from models.auth_models import Usuario

router = APIRouter(prefix="/estacionamiento", tags=["estacionamiento"])

@router.put("/{estacionamiento_id}", response_model=EstacionamientoResponse)
def actualizar_estacionamiento(
    estacionamiento_id: int,
    datos: EstacionamientoUpdate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Actualiza los datos del vehículo del residente"""
    service = EstacionamientoService()
    return service.update_estacionamiento(db, estacionamiento_id, current_user.id, datos)
