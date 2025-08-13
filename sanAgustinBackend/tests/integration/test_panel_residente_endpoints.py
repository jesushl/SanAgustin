import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from datetime import datetime, timedelta

from main import app
from models.schemas.panel_residente import PanelResidenteResponse
from models.database.departamento import Departamento
from models.database.estacionamiento import Estacionamiento
from models.database.adeudo import Adeudo

class TestPanelResidenteEndpoints:
    """Tests de integración para endpoints del panel de residente"""
    
    def setup_method(self):
        """Configuración inicial para cada test"""
        self.client = TestClient(app)
        self.base_url = "/panel-residente"
    
    @patch('services.endpoints.panel_residente_endpoints.get_current_user')
    @patch('services.endpoints.panel_residente_endpoints.get_db')
    def test_get_panel_residente_success(self, mock_get_db, mock_get_current_user, 
                                        sample_departamento, sample_estacionamiento, sample_adeudo):
        """Test exitoso para obtener panel de residente"""
        # Configurar mocks
        mock_user = Mock()
        mock_user.id = 1
        mock_get_current_user.return_value = mock_user
        
        mock_db = Mock()
        mock_get_db.return_value = mock_db
        
        # Mock del servicio
        with patch('services.endpoints.panel_residente_endpoints.PanelResidenteService') as mock_service_class:
            mock_service = Mock()
            mock_service_class.return_value = mock_service
            
            # Crear respuesta esperada
            expected_response = PanelResidenteResponse(
                departamento=sample_departamento,
                estacionamiento=sample_estacionamiento,
                adeudos_pendientes=[sample_adeudo],
                total_adeudos=1500.0,
                puede_reservar=False
            )
            mock_service.get_panel_residente.return_value = expected_response
            
            # Realizar petición
            response = self.client.get(self.base_url)
            
            # Verificar respuesta
            assert response.status_code == 200
            data = response.json()
            assert data["departamento"]["id"] == sample_departamento.id
            assert data["estacionamiento"]["id"] == sample_estacionamiento.id
            assert data["total_adeudos"] == 1500.0
            assert data["puede_reservar"] == False
            
            # Verificar que se llamó el servicio
            mock_service.get_panel_residente.assert_called_once_with(mock_db, mock_user.id)
    
    @patch('services.endpoints.panel_residente_endpoints.get_current_user')
    @patch('services.endpoints.panel_residente_endpoints.get_db')
    def test_get_panel_residente_no_departamento(self, mock_get_db, mock_get_current_user):
        """Test cuando el usuario no tiene departamento asociado"""
        # Configurar mocks
        mock_user = Mock()
        mock_user.id = 1
        mock_get_current_user.return_value = mock_user
        
        mock_db = Mock()
        mock_get_db.return_value = mock_db
        
        # Mock del servicio que lanza excepción
        with patch('services.endpoints.panel_residente_endpoints.PanelResidenteService') as mock_service_class:
            mock_service = Mock()
            mock_service_class.return_value = mock_service
            
            from fastapi import HTTPException
            mock_service.get_panel_residente.side_effect = HTTPException(
                status_code=404, 
                detail="No se encontró departamento asociado al usuario"
            )
            
            # Realizar petición
            response = self.client.get(self.base_url)
            
            # Verificar respuesta
            assert response.status_code == 404
            data = response.json()
            assert "No se encontró departamento asociado al usuario" in data["detail"]
    
    @patch('services.endpoints.panel_residente_endpoints.get_current_user')
    @patch('services.endpoints.panel_residente_endpoints.get_db')
    def test_get_panel_residente_no_estacionamiento(self, mock_get_db, mock_get_current_user, 
                                                   sample_departamento):
        """Test cuando el departamento no tiene estacionamiento"""
        # Configurar mocks
        mock_user = Mock()
        mock_user.id = 1
        mock_get_current_user.return_value = mock_user
        
        mock_db = Mock()
        mock_get_db.return_value = mock_db
        
        # Mock del servicio
        with patch('services.endpoints.panel_residente_endpoints.PanelResidenteService') as mock_service_class:
            mock_service = Mock()
            mock_service_class.return_value = mock_service
            
            # Crear respuesta esperada sin estacionamiento
            expected_response = PanelResidenteResponse(
                departamento=sample_departamento,
                estacionamiento=None,
                adeudos_pendientes=[],
                total_adeudos=0.0,
                puede_reservar=True
            )
            mock_service.get_panel_residente.return_value = expected_response
            
            # Realizar petición
            response = self.client.get(self.base_url)
            
            # Verificar respuesta
            assert response.status_code == 200
            data = response.json()
            assert data["departamento"]["id"] == sample_departamento.id
            assert data["estacionamiento"] is None
            assert data["total_adeudos"] == 0.0
            assert data["puede_reservar"] == True
    
    @patch('services.endpoints.panel_residente_endpoints.get_current_user')
    @patch('services.endpoints.panel_residente_endpoints.get_db')
    def test_get_panel_residente_multiple_adeudos(self, mock_get_db, mock_get_current_user,
                                                 sample_departamento, sample_estacionamiento):
        """Test cuando el departamento tiene múltiples adeudos"""
        # Configurar mocks
        mock_user = Mock()
        mock_user.id = 1
        mock_get_current_user.return_value = mock_user
        
        mock_db = Mock()
        mock_get_db.return_value = mock_db
        
        # Crear múltiples adeudos
        adeudo1 = Adeudo(
            id=1,
            departamento_id=sample_departamento.id,
            monto=1000.0,
            descripcion="Mantenimiento",
            fecha_vencimiento=datetime.now() + timedelta(days=30),
            fecha_creacion=datetime.now(),
            pagado=False
        )
        adeudo2 = Adeudo(
            id=2,
            departamento_id=sample_departamento.id,
            monto=500.0,
            descripcion="Servicios",
            fecha_vencimiento=datetime.now() + timedelta(days=15),
            fecha_creacion=datetime.now(),
            pagado=False
        )
        
        # Mock del servicio
        with patch('services.endpoints.panel_residente_endpoints.PanelResidenteService') as mock_service_class:
            mock_service = Mock()
            mock_service_class.return_value = mock_service
            
            # Crear respuesta esperada con múltiples adeudos
            expected_response = PanelResidenteResponse(
                departamento=sample_departamento,
                estacionamiento=sample_estacionamiento,
                adeudos_pendientes=[adeudo1, adeudo2],
                total_adeudos=1500.0,
                puede_reservar=False
            )
            mock_service.get_panel_residente.return_value = expected_response
            
            # Realizar petición
            response = self.client.get(self.base_url)
            
            # Verificar respuesta
            assert response.status_code == 200
            data = response.json()
            assert len(data["adeudos_pendientes"]) == 2
            assert data["total_adeudos"] == 1500.0
            assert data["puede_reservar"] == False
    
    def test_get_panel_residente_unauthorized(self):
        """Test cuando el usuario no está autenticado"""
        # Realizar petición sin autenticación
        response = self.client.get(self.base_url)
        
        # Verificar respuesta
        assert response.status_code == 422  # FastAPI validation error for missing dependency
