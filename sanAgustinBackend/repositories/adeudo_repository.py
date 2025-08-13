from typing import List
from sqlalchemy.orm import Session
from .base_repository import BaseRepository
from models.database.adeudo import Adeudo

class AdeudoRepository(BaseRepository[Adeudo]):
    def __init__(self):
        super().__init__(Adeudo)

    def get_pendientes_by_departamento_id(self, db: Session, departamento_id: int) -> List[Adeudo]:
        return db.query(Adeudo).filter(
            Adeudo.departamento_id == departamento_id,
            Adeudo.pagado == False
        ).all()

    def get_total_adeudos_by_departamento_id(self, db: Session, departamento_id: int) -> float:
        result = db.query(Adeudo).filter(
            Adeudo.departamento_id == departamento_id,
            Adeudo.pagado == False
        ).with_entities(Adeudo.monto).all()
        return sum(row[0] for row in result) if result else 0.0

    def get_all_pendientes(self, db: Session) -> List[Adeudo]:
        return db.query(Adeudo).filter(Adeudo.pagado == False).all()
