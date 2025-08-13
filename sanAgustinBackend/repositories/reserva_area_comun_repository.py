from typing import List
from sqlalchemy.orm import Session
from datetime import datetime
from .base_repository import BaseRepository
from models.database.reserva_area_comun import ReservaAreaComun

class ReservaAreaComunRepository(BaseRepository[ReservaAreaComun]):
    def __init__(self):
        super().__init__(ReservaAreaComun)

    def get_by_departamento_id(self, db: Session, departamento_id: int) -> List[ReservaAreaComun]:
        return db.query(ReservaAreaComun).filter(
            ReservaAreaComun.departamento_id == departamento_id
        ).all()

    def check_availability(self, db: Session, area_comun_id: int, fecha_inicio: datetime, fecha_fin: datetime) -> List[ReservaAreaComun]:
        return db.query(ReservaAreaComun).filter(
            ReservaAreaComun.area_comun_id == area_comun_id,
            ReservaAreaComun.estado == "activa",
            ReservaAreaComun.periodo_inicio < fecha_fin,
            ReservaAreaComun.periodo_fin > fecha_inicio
        ).all()

    def get_active_reservas(self, db: Session) -> List[ReservaAreaComun]:
        return db.query(ReservaAreaComun).filter(ReservaAreaComun.estado == "activa").all()
