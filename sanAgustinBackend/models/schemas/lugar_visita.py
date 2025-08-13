from pydantic import BaseModel

class LugarVisitaResponse(BaseModel):
    id: int
    numero: str
    descripcion: str
    capacidad: int
    
    model_config = {
        "from_attributes": True
    }
