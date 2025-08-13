from typing import List
from sqlalchemy.orm import Session
from datetime import datetime
from .base_repository import BaseRepository
from models.database.reserva_visita import ReservaVisita

class ReservaVisitaRepository(BaseRepository[ReservaVisita]):
    def __init__(self):
        super().__init__(ReservaVisita)

    def get_by_departamento_id(self, db: Session, departamento_id: int) -> List[ReservaVisita]:
        return db.query(ReservaVisita).filter(
            ReservaVisita.departamento_id == departamento_id
        ).all()

    def check_availability(self, db: Session, lugar_visita_id: int, fecha_inicio: datetime, fecha_fin: datetime) -> List[ReservaVisita]:
        return db.query(ReservaVisita).filter(
            ReservaVisita.lugar_visita_id == lugar_visita_id,
            ReservaVisita.estado == "activa",
            ReservaVisita.periodo_inicio < fecha_fin,
            ReservaVisita.periodo_fin > fecha_inicio
        ).all()

    def get_active_reservas(self, db: Session) -> List[ReservaVisita]:
        return db.query(ReservaVisita).filter(ReservaVisita.estado == "activa").all()
