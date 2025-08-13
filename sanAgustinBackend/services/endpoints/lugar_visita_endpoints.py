from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from services.lugar_visita_service import LugarVisitaService
from models.schemas.lugar_visita import LugarVisitaResponse
from core.database import get_db

router = APIRouter(prefix="/lugares-visita", tags=["lugares-visita"])

@router.get("/", response_model=List[LugarVisitaResponse])
def obtener_lugares_visita(db: Session = Depends(get_db)):
    """Obtiene todos los lugares de visita disponibles"""
    service = LugarVisitaService()
    return service.get_all_lugares_visita(db)
