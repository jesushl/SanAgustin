from .departamento import DepartamentoResponse
from .estacionamiento import EstacionamientoResponse, EstacionamientoUpdate
from .area_comun import AreaComunResponse
from .lugar_visita import LugarVisitaResponse
from .reserva_area_comun import ReservaAreaComunCreate, ReservaAreaComunResponse
from .reserva_visita import ReservaVisitaCreate, ReservaVisitaResponse
from .adeudo import AdeudoResponse
from .panel_residente import PanelResidenteResponse

__all__ = [
    'DepartamentoResponse',
    'EstacionamientoResponse',
    'EstacionamientoUpdate',
    'AreaComunResponse',
    'LugarVisitaResponse',
    'ReservaAreaComunCreate',
    'ReservaAreaComunResponse',
    'ReservaVisitaCreate',
    'ReservaVisitaResponse',
    'AdeudoResponse',
    'PanelResidenteResponse'
]
