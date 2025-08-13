from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from services.area_comun_service import AreaComunService
from models.schemas.area_comun import AreaComunResponse
from core.database import get_db

router = APIRouter(prefix="/areas-comunes", tags=["areas-comunes"])

@router.get("/", response_model=List[AreaComunResponse])
def obtener_areas_comunes(db: Session = Depends(get_db)):
    """Obtiene todas las áreas comunes disponibles"""
    service = AreaComunService()
    return service.get_all_areas_comunes(db)
