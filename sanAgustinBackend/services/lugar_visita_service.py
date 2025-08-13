from typing import List
from sqlalchemy.orm import Session
from repositories.lugar_visita_repository import LugarVisitaRepository
from models.schemas.lugar_visita import LugarVisitaResponse

class LugarVisitaService:
    def __init__(self):
        self.lugar_visita_repo = LugarVisitaRepository()

    def get_all_lugares_visita(self, db: Session) -> List[LugarVisitaResponse]:
        """Obtiene todos los lugares de visita disponibles"""
        lugares_visita = self.lugar_visita_repo.get_all_active(db)
        return [LugarVisitaResponse.from_orm(lugar) for lugar in lugares_visita]
