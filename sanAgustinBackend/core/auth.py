from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from services.auth_service import AuthService
from core.database import get_db
from typing import Optional

def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Dependency para obtener el usuario actual"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token de autorización requerido")
    
    token = authorization.replace("Bearer ", "")
    auth_service = AuthService(db)
    payload = auth_service.verify_token(token)
    email = payload.get("sub")
    user = auth_service.get_user_by_email(email)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user
