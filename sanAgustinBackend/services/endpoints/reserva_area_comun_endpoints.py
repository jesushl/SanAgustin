from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from services.reserva_area_comun_service import ReservaAreaComunService
from models.schemas.reserva_area_comun import ReservaAreaComunCreate, ReservaAreaComunResponse
from core.database import get_db
from core.auth import get_current_user
from models.auth_models import Usuario

router = APIRouter(prefix="/reservas-area-comun", tags=["reservas-area-comun"])

@router.get("/disponibilidad")
def verificar_disponibilidad_area_comun(
    area_comun_id: int,
    fecha_inicio: datetime,
    fecha_fin: datetime,
    db: Session = Depends(get_db)
):
    """Verifica la disponibilidad de un área común en un periodo específico"""
    service = ReservaAreaComunService()
    return service.check_availability(db, area_comun_id, fecha_inicio, fecha_fin)

@router.post("/", response_model=ReservaAreaComunResponse)
def crear_reserva_area_comun(
    reserva: ReservaAreaComunCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Crea una reserva de área común"""
    service = ReservaAreaComunService()
    return service.create_reserva(db, current_user.id, reserva)

@router.get("/usuario", response_model=List[ReservaAreaComunResponse])
def obtener_reservas_area_comun_usuario(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene las reservas de área común del usuario"""
    service = ReservaAreaComunService()
    return service.get_user_reservas(db, current_user.id)
