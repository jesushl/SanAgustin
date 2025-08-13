from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from services.reserva_visita_service import ReservaVisitaService
from models.schemas.reserva_visita import ReservaVisitaCreate, ReservaVisitaResponse
from core.database import get_db
from core.auth import get_current_user
from models.auth_models import Usuario

router = APIRouter(prefix="/reservas-visita", tags=["reservas-visita"])

@router.get("/disponibilidad")
def verificar_disponibilidad_lugar_visita(
    lugar_visita_id: int,
    fecha_inicio: datetime,
    fecha_fin: datetime,
    db: Session = Depends(get_db)
):
    """Verifica la disponibilidad de un lugar de visita en un periodo específico"""
    service = ReservaVisitaService()
    return service.check_availability(db, lugar_visita_id, fecha_inicio, fecha_fin)

@router.post("/", response_model=ReservaVisitaResponse)
def crear_reserva_visita(
    reserva: ReservaVisitaCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Crea una reserva de lugar de visita"""
    service = ReservaVisitaService()
    return service.create_reserva(db, current_user.id, reserva)

@router.get("/usuario", response_model=List[ReservaVisitaResponse])
def obtener_reservas_visita_usuario(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene las reservas de visita del usuario"""
    service = ReservaVisitaService()
    return service.get_user_reservas(db, current_user.id)
