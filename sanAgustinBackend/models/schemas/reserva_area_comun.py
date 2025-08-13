from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any

class ReservaAreaComunCreate(BaseModel):
    area_comun_id: int
    periodo_inicio: datetime
    periodo_fin: datetime

class ReservaAreaComunResponse(BaseModel):
    id: int
    area_comun_id: int
    departamento_id: int
    periodo_inicio: datetime
    periodo_fin: datetime
    estado: str
    area_comun: Dict[str, Any]
    
    model_config = {
        "from_attributes": True
    }
