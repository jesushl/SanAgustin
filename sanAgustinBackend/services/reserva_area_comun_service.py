from typing import List, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from repositories.departamento_repository import DepartamentoRepository
from repositories.area_comun_repository import AreaComunRepository
from repositories.reserva_area_comun_repository import ReservaAreaComunRepository
from repositories.adeudo_repository import AdeudoRepository
from models.schemas.reserva_area_comun import ReservaAreaComunCreate, ReservaAreaComunResponse

class ReservaAreaComunService:
    def __init__(self):
        self.departamento_repo = DepartamentoRepository()
        self.area_comun_repo = AreaComunRepository()
        self.reserva_repo = ReservaAreaComunRepository()
        self.adeudo_repo = AdeudoRepository()

    def check_availability(self, db: Session, area_comun_id: int, fecha_inicio: datetime, fecha_fin: datetime) -> Dict[str, Any]:
        """Verifica la disponibilidad de un área común en un periodo específico"""
        reservas_existentes = self.reserva_repo.check_availability(db, area_comun_id, fecha_inicio, fecha_fin)
        
        return {
            "disponible": len(reservas_existentes) == 0,
            "reservas_existentes": len(reservas_existentes)
        }

    def create_reserva(self, db: Session, usuario_id: int, reserva: ReservaAreaComunCreate) -> ReservaAreaComunResponse:
        """Crea una reserva de área común"""
        # Verificar que el usuario puede reservar (sin adeudos)
        departamento = self.departamento_repo.get_by_usuario_id(db, usuario_id)
        if not departamento:
            raise HTTPException(status_code=404, detail="No se encontró departamento asociado al usuario")
        
        adeudos_pendientes = self.adeudo_repo.get_pendientes_by_departamento_id(db, departamento.id)
        if adeudos_pendientes:
            raise HTTPException(status_code=400, detail="No puede realizar reservas mientras tenga adeudos pendientes")
        
        # Verificar disponibilidad
        disponibilidad = self.check_availability(db, reserva.area_comun_id, reserva.periodo_inicio, reserva.periodo_fin)
        if not disponibilidad["disponible"]:
            raise HTTPException(status_code=400, detail="El área común no está disponible en el periodo solicitado")
        
        # Crear la reserva
        reserva_data = {
            "area_comun_id": reserva.area_comun_id,
            "departamento_id": departamento.id,
            "periodo_inicio": reserva.periodo_inicio,
            "periodo_fin": reserva.periodo_fin
        }
        
        nueva_reserva = self.reserva_repo.create(db, obj_in=reserva_data)
        
        # Obtener información del área común
        area_comun = self.area_comun_repo.get(db, reserva.area_comun_id)
        
        return ReservaAreaComunResponse(
            **nueva_reserva.__dict__,
            area_comun=area_comun.__dict__
        )

    def get_user_reservas(self, db: Session, usuario_id: int) -> List[ReservaAreaComunResponse]:
        """Obtiene las reservas de área común del usuario"""
        departamento = self.departamento_repo.get_by_usuario_id(db, usuario_id)
        if not departamento:
            return []
        
        reservas = self.reserva_repo.get_by_departamento_id(db, departamento.id)
        return [ReservaAreaComunResponse.from_orm(reserva) for reserva in reservas]
