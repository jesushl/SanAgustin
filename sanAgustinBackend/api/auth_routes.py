from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import List
import httpx

from models.auth_models import Usuario, RegistroPendiente
from models.auth_schemas import Token, User, RegistroPendiente as RegistroPendienteSchema
from services.auth_service import AuthService
from core.oauth_config import oauth, GOOGLE_REDIRECT_URI, FACEBOOK_REDIRECT_URI

# Dependency para obtener la sesión de BD
def get_db():
    from main import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency para obtener el usuario actual
def get_current_user(token: str = Depends(lambda: None), db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    payload = auth_service.verify_token(token)
    email = payload.get("sub")
    user = auth_service.get_user_by_email(email)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

# Dependency para verificar si es admin
def get_current_admin_user(current_user: Usuario = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Acceso denegado. Se requieren permisos de administrador")
    return current_user

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.get("/google/login")
async def google_login(request: Request):
    """Inicia el flujo de login con Google"""
    redirect_uri = request.url_for('google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    """Callback de Google OAuth"""
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = await oauth.google.parse_id_token(token)
        
        # Extraer información del usuario
        email = user_info.get('email')
        nombre = user_info.get('given_name', '')
        apellido = user_info.get('family_name', '')
        provider_id = user_info.get('sub')
        
        auth_service = AuthService(db)
        result = auth_service.authenticate_oauth_user({
            'email': email,
            'nombre': nombre,
            'apellido': apellido,
            'provider_id': provider_id
        }, 'google')
        
        if result['needs_registration']:
            # Redirigir al frontend para completar registro
            return RedirectResponse(
                url=f"http://localhost:5173/register?email={email}&nombre={nombre}&apellido={apellido}&provider=google&provider_id={provider_id}"
            )
        else:
            # Usuario existe, redirigir con token
            return RedirectResponse(
                url=f"http://localhost:5173/auth-success?token={result['token']}&user_id={result['user_id']}&email={result['email']}&is_admin={result['is_admin']}"
            )
            
    except Exception as e:
        return RedirectResponse(url=f"http://localhost:5173/auth-error?error={str(e)}")

@router.get("/facebook/login")
async def facebook_login(request: Request):
    """Inicia el flujo de login con Facebook"""
    redirect_uri = request.url_for('facebook_callback')
    return await oauth.facebook.authorize_redirect(request, redirect_uri)

@router.get("/facebook/callback")
async def facebook_callback(request: Request, db: Session = Depends(get_db)):
    """Callback de Facebook OAuth"""
    try:
        token = await oauth.facebook.authorize_access_token(request)
        
        # Obtener información del usuario de Facebook
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                'https://graph.facebook.com/me',
                params={'fields': 'id,name,email', 'access_token': token['access_token']}
            )
            user_info = resp.json()
        
        # Extraer información del usuario
        email = user_info.get('email')
        full_name = user_info.get('name', '').split(' ', 1)
        nombre = full_name[0] if full_name else ''
        apellido = full_name[1] if len(full_name) > 1 else ''
        provider_id = user_info.get('id')
        
        auth_service = AuthService(db)
        result = auth_service.authenticate_oauth_user({
            'email': email,
            'nombre': nombre,
            'apellido': apellido,
            'provider_id': provider_id
        }, 'facebook')
        
        if result['needs_registration']:
            # Redirigir al frontend para completar registro
            return RedirectResponse(
                url=f"http://localhost:5173/register?email={email}&nombre={nombre}&apellido={apellido}&provider=facebook&provider_id={provider_id}"
            )
        else:
            # Usuario existe, redirigir con token
            return RedirectResponse(
                url=f"http://localhost:5173/auth-success?token={result['token']}&user_id={result['user_id']}&email={result['email']}&is_admin={result['is_admin']}"
            )
            
    except Exception as e:
        return RedirectResponse(url=f"http://localhost:5173/auth-error?error={str(e)}")

@router.post("/register", response_model=RegistroPendienteSchema)
async def register_user(
    registration_data: dict,
    db: Session = Depends(get_db)
):
    """Registra un nuevo usuario pendiente de aprobación"""
    auth_service = AuthService(db)
    
    # Verificar que no exista ya un usuario con ese email
    existing_user = auth_service.get_user_by_email(registration_data['email'])
    if existing_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    # Verificar que no exista ya un registro pendiente
    existing_pending = auth_service.get_pending_registration(registration_data['email'])
    if existing_pending:
        raise HTTPException(status_code=400, detail="Ya existe un registro pendiente para este email")
    
    # Crear registro pendiente
    reg_data = {
        'email': registration_data['email'],
        'nombre': registration_data['nombre'],
        'apellido': registration_data['apellido'],
        'provider': registration_data['provider'],
        'provider_id': registration_data['provider_id'],
        'telefono': registration_data.get('telefono'),
        'direccion': registration_data.get('direccion'),
        'departamento': registration_data.get('departamento'),
        'notas_adicionales': registration_data.get('notas_adicionales')
    }
    
    pending_reg = auth_service.create_pending_registration(reg_data)
    return pending_reg

@router.get("/pending-registrations", response_model=List[RegistroPendienteSchema])
async def get_pending_registrations(
    current_admin: Usuario = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Obtiene todos los registros pendientes de aprobación (solo admin)"""
    auth_service = AuthService(db)
    return auth_service.get_all_pending_registrations()

@router.post("/approve-registration/{reg_id}", response_model=User)
async def approve_registration(
    reg_id: int,
    current_admin: Usuario = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Aprueba un registro pendiente y crea el usuario (solo admin)"""
    auth_service = AuthService(db)
    return auth_service.approve_registration(reg_id, current_admin.id)

@router.get("/me", response_model=User)
async def get_current_user_info(current_user: Usuario = Depends(get_current_user)):
    """Obtiene información del usuario actual"""
    return current_user
