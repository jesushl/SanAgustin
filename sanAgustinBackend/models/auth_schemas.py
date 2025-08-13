from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    email: str
    is_admin: bool

class UserBase(BaseModel):
    email: EmailStr
    nombre: str
    apellido: str

class UserCreate(UserBase):
    provider: str
    provider_id: str

class User(UserBase):
    id: int
    provider: str
    is_active: bool
    is_admin: bool
    created_at: datetime
    
    model_config = {
        "from_attributes": True
    }

class RegistroPendienteBase(BaseModel):
    email: EmailStr
    nombre: str
    apellido: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    departamento: Optional[str] = None
    notas_adicionales: Optional[str] = None

class RegistroPendienteCreate(RegistroPendienteBase):
    provider: str
    provider_id: str

class RegistroPendiente(RegistroPendienteBase):
    id: int
    provider: str
    provider_id: str
    is_approved: bool
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    created_at: datetime
    
    model_config = {
        "from_attributes": True
    }

class ContactoBase(BaseModel):
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    departamento: Optional[str] = None

class ContactoCreate(ContactoBase):
    pass

class Contacto(ContactoBase):
    id: int
    usuario_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True
    }

class OAuthUserInfo(BaseModel):
    email: str
    nombre: str
    apellido: str
    provider: str
    provider_id: str
