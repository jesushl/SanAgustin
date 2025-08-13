from typing import List
from sqlalchemy.orm import Session
from repositories.area_comun_repository import AreaComunRepository
from models.schemas.area_comun import AreaComunResponse

class AreaComunService:
    def __init__(self):
        self.area_comun_repo = AreaComunRepository()

    def get_all_areas_comunes(self, db: Session) -> List[AreaComunResponse]:
        """Obtiene todas las áreas comunes disponibles"""
        areas_comunes = self.area_comun_repo.get_all_active(db)
        return [AreaComunResponse.from_orm(area) for area in areas_comunes]
