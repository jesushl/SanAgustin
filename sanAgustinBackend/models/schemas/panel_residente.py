from pydantic import BaseModel
from typing import List, Optional
from .departamento import DepartamentoResponse
from .estacionamiento import EstacionamientoResponse
from .adeudo import AdeudoResponse

class PanelResidenteResponse(BaseModel):
    departamento: DepartamentoResponse
    estacionamiento: Optional[EstacionamientoResponse] = None
    adeudos_pendientes: List[AdeudoResponse]
    total_adeudos: float
    puede_reservar: bool
