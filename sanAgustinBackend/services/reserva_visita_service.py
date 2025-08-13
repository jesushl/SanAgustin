from typing import List, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from repositories.departamento_repository import DepartamentoRepository
from repositories.lugar_visita_repository import LugarVisitaRepository
from repositories.reserva_visita_repository import ReservaVisitaRepository
from models.schemas.reserva_visita import ReservaVisitaCreate, ReservaVisitaResponse

class ReservaVisitaService:
    def __init__(self):
        self.departamento_repo = DepartamentoRepository()
        self.lugar_visita_repo = LugarVisitaRepository()
        self.reserva_repo = ReservaVisitaRepository()

    def check_availability(self, db: Session, lugar_visita_id: int, fecha_inicio: datetime, fecha_fin: datetime) -> Dict[str, Any]:
        """Verifica la disponibilidad de un lugar de visita en un periodo específico"""
        reservas_existentes = self.reserva_repo.check_availability(db, lugar_visita_id, fecha_inicio, fecha_fin)
        
        return {
            "disponible": len(reservas_existentes) == 0,
            "reservas_existentes": len(reservas_existentes)
        }

    def create_reserva(self, db: Session, usuario_id: int, reserva: ReservaVisitaCreate) -> ReservaVisitaResponse:
        """Crea una reserva de lugar de visita"""
        # Verificar que el usuario tiene departamento
        departamento = self.departamento_repo.get_by_usuario_id(db, usuario_id)
        if not departamento:
            raise HTTPException(status_code=404, detail="No se encontró departamento asociado al usuario")
        
        # Verificar que la reserva no exceda 24 horas
        duracion = reserva.periodo_fin - reserva.periodo_inicio
        if duracion.total_seconds() > 24 * 3600:
            raise HTTPException(status_code=400, detail="La reserva no puede exceder 24 horas")
        
        # Verificar disponibilidad
        disponibilidad = self.check_availability(db, reserva.lugar_visita_id, reserva.periodo_inicio, reserva.periodo_fin)
        if not disponibilidad["disponible"]:
            raise HTTPException(status_code=400, detail="El lugar de visita no está disponible en el periodo solicitado")
        
        # Crear la reserva
        reserva_data = {
            "lugar_visita_id": reserva.lugar_visita_id,
            "departamento_id": departamento.id,
            "placa_visita": reserva.placa_visita,
            "periodo_inicio": reserva.periodo_inicio,
            "periodo_fin": reserva.periodo_fin
        }
        
        nueva_reserva = self.reserva_repo.create(db, obj_in=reserva_data)
        
        # Obtener información del lugar de visita
        lugar_visita = self.lugar_visita_repo.get(db, reserva.lugar_visita_id)
        
        return ReservaVisitaResponse(
            **nueva_reserva.__dict__,
            lugar_visita=lugar_visita
        )

    def get_user_reservas(self, db: Session, usuario_id: int) -> List[ReservaVisitaResponse]:
        """Obtiene las reservas de visita del usuario"""
        departamento = self.departamento_repo.get_by_usuario_id(db, usuario_id)
        if not departamento:
            return []
        
        reservas = self.reserva_repo.get_by_departamento_id(db, departamento.id)
        return [ReservaVisitaResponse.from_orm(reserva) for reserva in reservas]
