from pydantic import BaseModel
from typing import Optional

class EstacionamientoResponse(BaseModel):
    id: int
    numero: str
    placa: Optional[str] = None
    modelo_auto: Optional[str] = None
    color_auto: Optional[str] = None
    es_visita: bool
    departamento_id: int
    
    model_config = {
        "from_attributes": True
    }

class EstacionamientoUpdate(BaseModel):
    placa: Optional[str] = None
    modelo_auto: Optional[str] = None
    color_auto: Optional[str] = None
