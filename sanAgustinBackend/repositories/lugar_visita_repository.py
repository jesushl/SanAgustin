from typing import List
from sqlalchemy.orm import Session
from .base_repository import BaseRepository
from models.database.lugar_visita import LugarVisita

class LugarVisitaRepository(BaseRepository[LugarVisita]):
    def __init__(self):
        super().__init__(LugarVisita)

    def get_by_numero(self, db: Session, numero: str) -> LugarVisita:
        return db.query(LugarVisita).filter(LugarVisita.numero == numero).first()

    def get_all_active(self, db: Session) -> List[LugarVisita]:
        return db.query(LugarVisita).all()
