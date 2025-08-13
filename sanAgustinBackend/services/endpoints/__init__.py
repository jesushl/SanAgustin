from .panel_residente_endpoints import router as panel_residente_router
from .estacionamiento_endpoints import router as estacionamiento_router
from .area_comun_endpoints import router as area_comun_router
from .lugar_visita_endpoints import router as lugar_visita_router
from .reserva_area_comun_endpoints import router as reserva_area_comun_router
from .reserva_visita_endpoints import router as reserva_visita_router

__all__ = [
    'panel_residente_router',
    'estacionamiento_router',
    'area_comun_router',
    'lugar_visita_router',
    'reserva_area_comun_router',
    'reserva_visita_router'
]
