from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, status
from typing import Optional
import httpx

from models.auth_models import Usuario, RegistroPendiente, Contacto
from models.auth_schemas import UserCreate, RegistroPendienteCreate, ContactoCreate
from core.oauth_config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

class AuthService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    def get_user_by_email(self, email: str) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.email == email).first()
    
    def get_user_by_provider_id(self, provider: str, provider_id: str) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(
            and_(Usuario.provider == provider, Usuario.provider_id == provider_id)
        ).first()
    
    def create_user(self, user_data: UserCreate) -> Usuario:
        db_user = Usuario(**user_data.dict())
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def get_pending_registration(self, email: str) -> Optional[RegistroPendiente]:
        return self.db.query(RegistroPendiente).filter(RegistroPendiente.email == email).first()
    
    def create_pending_registration(self, reg_data: RegistroPendienteCreate) -> RegistroPendiente:
        db_reg = RegistroPendiente(**reg_data.dict())
        self.db.add(db_reg)
        self.db.commit()
        self.db.refresh(db_reg)
        return db_reg
    
    def approve_registration(self, reg_id: int, admin_user_id: int) -> Usuario:
        # Obtener el registro pendiente
        pending_reg = self.db.query(RegistroPendiente).filter(RegistroPendiente.id == reg_id).first()
        if not pending_reg:
            raise HTTPException(status_code=404, detail="Registro pendiente no encontrado")
        
        if pending_reg.is_approved:
            raise HTTPException(status_code=400, detail="El registro ya fue aprobado")
        
        # Crear el usuario
        user_data = UserCreate(
            email=pending_reg.email,
            nombre=pending_reg.nombre,
            apellido=pending_reg.apellido,
            provider=pending_reg.provider,
            provider_id=pending_reg.provider_id
        )
        user = self.create_user(user_data)
        
        # Crear el contacto si hay datos
        if pending_reg.telefono or pending_reg.direccion or pending_reg.departamento:
            contacto_data = ContactoCreate(
                telefono=pending_reg.telefono,
                direccion=pending_reg.direccion,
                departamento=pending_reg.departamento
            )
            contacto = Contacto(**contacto_data.dict(), usuario_id=user.id)
            self.db.add(contacto)
        
        # Marcar como aprobado
        pending_reg.is_approved = True
        pending_reg.approved_by = admin_user_id
        pending_reg.approved_at = datetime.utcnow()
        
        self.db.commit()
        return user
    
    def get_all_pending_registrations(self):
        return self.db.query(RegistroPendiente).filter(RegistroPendiente.is_approved == False).all()
    
    def authenticate_oauth_user(self, user_info: dict, provider: str) -> dict:
        """
        Autentica un usuario OAuth y retorna información sobre si necesita registro
        """
        email = user_info.get('email')
        if not email:
            raise HTTPException(status_code=400, detail="Email no proporcionado por el proveedor OAuth")
        
        # Verificar si el usuario ya existe
        existing_user = self.get_user_by_email(email)
        if existing_user:
            # Usuario existe, generar token
            token = self.create_access_token(data={"sub": existing_user.email})
            return {
                "needs_registration": False,
                "token": token,
                "user_id": existing_user.id,
                "email": existing_user.email,
                "is_admin": existing_user.is_admin
            }
        
        # Verificar si hay un registro pendiente
        pending_reg = self.get_pending_registration(email)
        if pending_reg:
            return {
                "needs_registration": True,
                "registration_id": pending_reg.id,
                "message": "Registro pendiente de aprobación"
            }
        
        # Usuario nuevo, necesita registro
        return {
            "needs_registration": True,
            "message": "Usuario nuevo, requiere registro"
        }
