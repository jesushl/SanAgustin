from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from repositories.departamento_repository import DepartamentoRepository
from repositories.estacionamiento_repository import EstacionamientoRepository
from repositories.adeudo_repository import AdeudoRepository
from models.schemas.panel_residente import PanelResidenteResponse
from models.database.departamento import Departamento
from models.database.estacionamiento import Estacionamiento
from models.database.adeudo import Adeudo

class PanelResidenteService:
    def __init__(self):
        self.departamento_repo = DepartamentoRepository()
        self.estacionamiento_repo = EstacionamientoRepository()
        self.adeudo_repo = AdeudoRepository()

    def get_panel_residente(self, db: Session, usuario_id: int) -> PanelResidenteResponse:
        """Obtiene toda la información del panel de residente"""
        # Buscar el departamento del usuario
        departamento = self.departamento_repo.get_by_usuario_id(db, usuario_id)
        if not departamento:
            raise HTTPException(status_code=404, detail="No se encontró departamento asociado al usuario")
        
        # Buscar estacionamiento del departamento
        estacionamiento = self.estacionamiento_repo.get_by_departamento_id(db, departamento.id, es_visita=False)
        
        # Buscar adeudos pendientes
        adeudos_pendientes = self.adeudo_repo.get_pendientes_by_departamento_id(db, departamento.id)
        
        # Calcular total de adeudos
        total_adeudos = self.adeudo_repo.get_total_adeudos_by_departamento_id(db, departamento.id)
        puede_reservar = total_adeudos == 0
        
        return PanelResidenteResponse(
            departamento=departamento,
            estacionamiento=estacionamiento,
            adeudos_pendientes=adeudos_pendientes,
            total_adeudos=total_adeudos,
            puede_reservar=puede_reservar
        )
