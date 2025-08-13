from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .lugar_visita import LugarVisitaResponse

class ReservaVisitaCreate(BaseModel):
    lugar_visita_id: int
    placa_visita: Optional[str] = None
    periodo_inicio: datetime
    periodo_fin: datetime

class ReservaVisitaResponse(BaseModel):
    id: int
    lugar_visita_id: int
    departamento_id: int
    placa_visita: Optional[str] = None
    periodo_inicio: datetime
    periodo_fin: datetime
    estado: str
    lugar_visita: LugarVisitaResponse
    
    model_config = {
        "from_attributes": True
    }
