import pytest
from unittest.mock import Mock
from datetime import datetime, timedelta

# Importar solo los modelos necesarios para los tests
from models.auth_models import Usuario
from models.database.departamento import Departamento
from models.database.estacionamiento import Estacionamiento
from models.database.area_comun import AreaComun
from models.database.lugar_visita import LugarVisita
from models.database.adeudo import Adeudo
from models.database.reserva_area_comun import ReservaAreaComun
from models.database.reserva_visita import ReservaVisita

@pytest.fixture
def mock_db():
    """Mock de base de datos para pruebas"""
    return Mock()

@pytest.fixture
def mock_current_user():
    """Usuario mock para pruebas"""
    user = Mock(spec=Usuario)
    user.id = 1
    user.email = "test@example.com"
    user.nombre = "Test"
    user.apellido = "User"
    user.is_admin = False
    user.is_active = True
    return user

@pytest.fixture
def sample_departamento():
    """Departamento de ejemplo para pruebas"""
    departamento = Departamento(
        id=1,
        numero="01",
        usuario_id=1
    )
    return departamento

@pytest.fixture
def sample_estacionamiento(sample_departamento):
    """Estacionamiento de ejemplo para pruebas"""
    estacionamiento = Estacionamiento(
        id=1,
        numero="E01",
        placa="ABC123",
        modelo_auto="Toyota Corolla",
        color_auto="Blanco",
        es_visita=False,
        departamento_id=sample_departamento.id
    )
    return estacionamiento

@pytest.fixture
def sample_area_comun():
    """Área común de ejemplo para pruebas"""
    area_comun = AreaComun(
        id=1,
        nombre="Palapa",
        descripcion="Área de recreación",
        ubicacion="Zona central",
        capacidad=20
    )
    return area_comun

@pytest.fixture
def sample_lugar_visita():
    """Lugar de visita de ejemplo para pruebas"""
    lugar_visita = LugarVisita(
        id=1,
        numero="V1",
        descripcion="Estacionamiento de visita 1",
        capacidad=1
    )
    return lugar_visita

@pytest.fixture
def sample_adeudo(sample_departamento):
    """Adeudo de ejemplo para pruebas"""
    adeudo = Adeudo(
        id=1,
        departamento_id=sample_departamento.id,
        monto=1500.0,
        descripcion="Mantenimiento mensual",
        fecha_vencimiento=datetime.now() + timedelta(days=30),
        fecha_creacion=datetime.now(),
        pagado=False
    )
    return adeudo

@pytest.fixture
def sample_reserva_area_comun(sample_departamento, sample_area_comun):
    """Reserva de área común de ejemplo para pruebas"""
    reserva = ReservaAreaComun(
        id=1,
        area_comun_id=sample_area_comun.id,
        departamento_id=sample_departamento.id,
        periodo_inicio=datetime.now() + timedelta(days=1),
        periodo_fin=datetime.now() + timedelta(days=1, hours=2),
        estado="activa"
    )
    return reserva

@pytest.fixture
def sample_reserva_visita(sample_departamento, sample_lugar_visita):
    """Reserva de visita de ejemplo para pruebas"""
    reserva = ReservaVisita(
        id=1,
        lugar_visita_id=sample_lugar_visita.id,
        departamento_id=sample_departamento.id,
        placa_visita="XYZ789",
        periodo_inicio=datetime.now() + timedelta(days=1),
        periodo_fin=datetime.now() + timedelta(days=1, hours=3),
        estado="activa"
    )
    return reserva

@pytest.fixture
def mock_auth_dependency():
    """Mock para la dependencia de autenticación"""
    def _mock_get_current_user():
        user = Mock(spec=Usuario)
        user.id = 1
        user.email = "test@example.com"
        user.nombre = "Test"
        user.apellido = "User"
        user.is_admin = False
        user.is_active = True
        return user
    
    return _mock_get_current_user

@pytest.fixture
def mock_db_dependency():
    """Mock para la dependencia de base de datos"""
    def _mock_get_db():
        # Crear una sesión mock
        mock_session = Mock()
        yield mock_session
    
    return _mock_get_db
