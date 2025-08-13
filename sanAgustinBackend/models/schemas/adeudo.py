from pydantic import BaseModel
from datetime import datetime

class AdeudoResponse(BaseModel):
    id: int
    departamento_id: int
    monto: float
    descripcion: str
    fecha_vencimiento: datetime
    fecha_creacion: datetime
    pagado: bool
    
    model_config = {
        "from_attributes": True
    }
