from typing import List
from sqlalchemy.orm import Session
from .base_repository import BaseRepository
from models.database.area_comun import AreaComun

class AreaComunRepository(BaseRepository[AreaComun]):
    def __init__(self):
        super().__init__(AreaComun)

    def get_by_nombre(self, db: Session, nombre: str) -> AreaComun:
        return db.query(AreaComun).filter(AreaComun.nombre == nombre).first()

    def get_all_active(self, db: Session) -> List[AreaComun]:
        return db.query(AreaComun).all()
