from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from services.panel_residente_service import PanelResidenteService
from models.schemas.panel_residente import PanelResidenteResponse
from core.database import get_db
from core.auth import get_current_user
from models.auth_models import Usuario

router = APIRouter(prefix="/panel-residente", tags=["panel-residente"])

@router.get("/", response_model=PanelResidenteResponse)
def obtener_panel_residente(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene toda la información del panel de residente"""
    service = PanelResidenteService()
    return service.get_panel_residente(db, current_user.id)
