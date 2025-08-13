from typing import Optional, List
from sqlalchemy.orm import Session
from .base_repository import BaseRepository
from models.database.departamento import Departamento

class DepartamentoRepository(BaseRepository[Departamento]):
    def __init__(self):
        super().__init__(Departamento)

    def get_by_usuario_id(self, db: Session, usuario_id: int) -> Optional[Departamento]:
        return db.query(Departamento).filter(Departamento.usuario_id == usuario_id).first()

    def get_by_numero(self, db: Session, numero: str) -> Optional[Departamento]:
        return db.query(Departamento).filter(Departamento.numero == numero).first()

    def get_all_with_adeudos(self, db: Session) -> List[Departamento]:
        return db.query(Departamento).join(Departamento.adeudos).all()
