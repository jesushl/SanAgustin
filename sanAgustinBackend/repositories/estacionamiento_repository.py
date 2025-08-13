from typing import Optional, List
from sqlalchemy.orm import Session
from .base_repository import BaseRepository
from models.database.estacionamiento import Estacionamiento

class EstacionamientoRepository(BaseRepository[Estacionamiento]):
    def __init__(self):
        super().__init__(Estacionamiento)

    def get_by_departamento_id(self, db: Session, departamento_id: int, es_visita: bool = False) -> Optional[Estacionamiento]:
        return db.query(Estacionamiento).filter(
            Estacionamiento.departamento_id == departamento_id,
            Estacionamiento.es_visita == es_visita
        ).first()

    def get_by_numero(self, db: Session, numero: str) -> Optional[Estacionamiento]:
        return db.query(Estacionamiento).filter(Estacionamiento.numero == numero).first()

    def get_by_placa(self, db: Session, placa: str) -> Optional[Estacionamiento]:
        return db.query(Estacionamiento).filter(Estacionamiento.placa == placa).first()

    def get_estacionamientos_visita(self, db: Session) -> List[Estacionamiento]:
        return db.query(Estacionamiento).filter(Estacionamiento.es_visita == True).all()
