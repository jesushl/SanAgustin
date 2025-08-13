from pydantic import BaseModel

class AreaComunResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str
    ubicacion: str
    capacidad: int
    
    model_config = {
        "from_attributes": True
    }
