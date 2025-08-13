from pydantic import BaseModel
from typing import Optional

class DepartamentoResponse(BaseModel):
    id: int
    numero: str
    usuario_id: Optional[int] = None
    
    model_config = {
        "from_attributes": True
    }
