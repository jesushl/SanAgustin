from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importar rutas de autenticación
from api.auth_routes import router as auth_router

# Importar rutas de servicios
from services.endpoints.panel_residente_endpoints import router as panel_residente_router
from services.endpoints.estacionamiento_endpoints import router as estacionamiento_router
from services.endpoints.area_comun_endpoints import router as area_comun_router
from services.endpoints.lugar_visita_endpoints import router as lugar_visita_router
from services.endpoints.reserva_area_comun_endpoints import router as reserva_area_comun_router
from services.endpoints.reserva_visita_endpoints import router as reserva_visita_router

# Creación de la aplicación FastAPI
app = FastAPI(
    title="San Agustín API",
    description="API para la gestión de servicios de la privada San Agustín",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas de autenticación
app.include_router(auth_router)

# Incluir rutas de servicios
app.include_router(panel_residente_router)
app.include_router(estacionamiento_router)
app.include_router(area_comun_router)
app.include_router(lugar_visita_router)
app.include_router(reserva_area_comun_router)
app.include_router(reserva_visita_router)

# Configurar OAuth
from core.oauth_config import oauth

@app.get("/")
def read_root():
    return {"message": "San Agustín API - Sistema de Gestión de Residencias"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API funcionando correctamente"}