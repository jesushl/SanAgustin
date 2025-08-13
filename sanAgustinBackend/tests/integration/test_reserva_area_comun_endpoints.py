import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from datetime import datetime, timedelta

from main import app
from models.schemas.reserva_area_comun import ReservaAreaComunCreate, ReservaAreaComunResponse
from models.database.departamento import Departamento
from models.database.area_comun import AreaComun
from models.database.reserva_area_comun import ReservaAreaComun

class TestReservaAreaComunEndpoints:
    """Tests de integración para endpoints de reservas de área común"""
    
    def setup_method(self):
        """Configuración inicial para cada test"""
        self.client = TestClient(app)
        self.base_url = "/reservas-area-comun"
        self.fecha_inicio = datetime.now() + timedelta(days=1)
        self.fecha_fin = datetime.now() + timedelta(days=1, hours=2)
    
    @patch('services.endpoints.reserva_area_comun_endpoints.get_db')
    def test_get_areas_comunes_success(self, mock_get_db, sample_area_comun):
        """Test exitoso para obtener áreas comunes"""
        # Configurar mocks
        mock_db = Mock()
        mock_get_db.return_value = mock_db
        
        # Mock del servicio
        with patch('services.endpoints.reserva_area_comun_endpoints.AreaComunService') as mock_service_class:
            mock_service = Mock()
            mock_service_class.return_value = mock_service
            
            # Crear respuesta esperada
            expected_response = [sample_area_comun]
            mock_service.get_all_areas_comunes.return_value = expected_response
            
            # Realizar petición
            response = self.client.get("/areas-comunes")
            
            # Verificar respuesta
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 1
            assert data[0]["id"] == sample_area_comun.id
            assert data[0]["nombre"] == sample_area_comun.nombre
            
            # Verificar que se llamó el servicio
            mock_service.get_all_areas_comunes.assert_called_once_with(mock_db)
    
    @patch('services.endpoints.reserva_area_comun_endpoints.get_db')
    def test_check_availability_success(self, mock_get_db, sample_area_comun):
        """Test exitoso para verificar disponibilidad"""
        # Configurar mocks
        mock_db = Mock()
        mock_get_db.return_value = mock_db
        
        # Mock del servicio
        with patch('services.endpoints.reserva_area_comun_endpoints.ReservaAreaComunService') as mock_service_class:
            mock_service = Mock()
            mock_service_class.return_value = mock_service
            
            # Crear respuesta esperada
            expected_response = {
                "disponible": True,
                "reservas_existentes": 0
            }
            mock_service.check_availability.return_value = expected_response
            
            # Parámetros de la petición
            params = {
                "area_comun_id": sample_area_comun.id,
                "fecha_inicio": self.fecha_inicio.isoformat(),
                "fecha_fin": self.fecha_fin.isoformat()
            }
            
            # Realizar petición
            response = self.client.get(f"{self.base_url}/disponibilidad", params=params)
            
            # Verificar respuesta
            assert response.status_code == 200
            data = response.json()
            assert data["disponible"] == True
            assert data["reservas_existentes"] == 0
            
            # Verificar que se llamó el servicio
            mock_service.check_availability.assert_called_once_with(
                mock_db, sample_area_comun.id, self.fecha_inicio, self.fecha_fin
            )
    
    @patch('services.endpoints.reserva_area_comun_endpoints.get_current_user')
    @patch('services.endpoints.reserva_area_comun_endpoints.get_db')
    def test_create_reserva_success(self, mock_get_db, mock_get_current_user,
                                  sample_departamento, sample_area_comun):
        """Test exitoso para crear reserva de área común"""
        # Configurar mocks
        mock_user = Mock()
        mock_user.id = 1
        mock_get_current_user.return_value = mock_user
        
        mock_db = Mock()
        mock_get_db.return_value = mock_db
        
        # Mock del servicio
        with patch('services.endpoints.reserva_area_comun_endpoints.ReservaAreaComunService') as mock_service_class:
            mock_service = Mock()
            mock_service_class.return_value = mock_service
            
            # Crear reserva esperada
            expected_reserva = ReservaAreaComunResponse(
                id=1,
                area_comun_id=sample_area_comun.id,
                departamento_id=sample_departamento.id,
                periodo_inicio=self.fecha_inicio,
                periodo_fin=self.fecha_fin,
                estado="activa",
                area_comun=sample_area_comun.__dict__
            )
            mock_service.create_reserva.return_value = expected_reserva
            
            # Datos de la reserva
            reserva_data = {
                "area_comun_id": sample_area_comun.id,
                "periodo_inicio": self.fecha_inicio.isoformat(),
                "periodo_fin": self.fecha_fin.isoformat()
            }
            
            # Realizar petición
            response = self.client.post(f"{self.base_url}/", json=reserva_data)
            
            # Verificar respuesta
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == 1
            assert data["area_comun_id"] == sample_area_comun.id
            assert data["departamento_id"] == sample_departamento.id
            assert data["estado"] == "activa"
            
            # Verificar que se llamó el servicio
            mock_service.create_reserva.assert_called_once()
    
    @patch('services.endpoints.reserva_area_comun_endpoints.get_current_user')
    @patch('services.endpoints.reserva_area_comun_endpoints.get_db')
    def test_create_reserva_with_adeudos(self, mock_get_db, mock_get_current_user,
                                       sample_departamento):
        """Test cuando el usuario tiene adeudos pendientes"""
        # Configurar mocks
        mock_user = Mock()
        mock_user.id = 1
        mock_get_current_user.return_value = mock_user
        
        mock_db = Mock()
        mock_get_db.return_value = mock_db
        
        # Mock del servicio que lanza excepción
        with patch('services.endpoints.reserva_area_comun_endpoints.ReservaAreaComunService') as mock_service_class:
            mock_service = Mock()
            mock_service_class.return_value = mock_service
            
            from fastapi import HTTPException
            mock_service.create_reserva.side_effect = HTTPException(
                status_code=400,
                detail="No puede realizar reservas mientras tenga adeudos pendientes"
            )
            
            # Datos de la reserva
            reserva_data = {
                "area_comun_id": 1,
                "periodo_inicio": self.fecha_inicio.isoformat(),
                "periodo_fin": self.fecha_fin.isoformat()
            }
            
            # Realizar petición
            response = self.client.post(f"{self.base_url}/", json=reserva_data)
            
            # Verificar respuesta
            assert response.status_code == 400
            data = response.json()
            assert "No puede realizar reservas mientras tenga adeudos pendientes" in data["detail"]
    
    @patch('services.endpoints.reserva_area_comun_endpoints.get_current_user')
    @patch('services.endpoints.reserva_area_comun_endpoints.get_db')
    def test_create_reserva_not_available(self, mock_get_db, mock_get_current_user,
                                        sample_departamento):
        """Test cuando el área común no está disponible"""
        # Configurar mocks
        mock_user = Mock()
        mock_user.id = 1
        mock_get_current_user.return_value = mock_user
        
        mock_db = Mock()
        mock_get_db.return_value = mock_db
        
        # Mock del servicio que lanza excepción
        with patch('services.endpoints.reserva_area_comun_endpoints.ReservaAreaComunService') as mock_service_class:
            mock_service = Mock()
            mock_service_class.return_value = mock_service
            
            from fastapi import HTTPException
            mock_service.create_reserva.side_effect = HTTPException(
                status_code=400,
                detail="El área común no está disponible en el periodo solicitado"
            )
            
            # Datos de la reserva
            reserva_data = {
                "area_comun_id": 1,
                "periodo_inicio": self.fecha_inicio.isoformat(),
                "periodo_fin": self.fecha_fin.isoformat()
            }
            
            # Realizar petición
            response = self.client.post(f"{self.base_url}/", json=reserva_data)
            
            # Verificar respuesta
            assert response.status_code == 400
            data = response.json()
            assert "El área común no está disponible en el periodo solicitado" in data["detail"]
    
    @patch('services.endpoints.reserva_area_comun_endpoints.get_current_user')
    @patch('services.endpoints.reserva_area_comun_endpoints.get_db')
    def test_get_user_reservas_success(self, mock_get_db, mock_get_current_user,
                                     sample_departamento):
        """Test exitoso para obtener reservas del usuario"""
        # Configurar mocks
        mock_user = Mock()
        mock_user.id = 1
        mock_get_current_user.return_value = mock_user
        
        mock_db = Mock()
        mock_get_db.return_value = mock_db
        
        # Mock del servicio
        with patch('services.endpoints.reserva_area_comun_endpoints.ReservaAreaComunService') as mock_service_class:
            mock_service = Mock()
            mock_service_class.return_value = mock_service
            
            # Crear reservas esperadas
            reserva1 = ReservaAreaComunResponse(
                id=1,
                area_comun_id=1,
                departamento_id=sample_departamento.id,
                periodo_inicio=self.fecha_inicio,
                periodo_fin=self.fecha_fin,
                estado="activa",
                area_comun={"id": 1, "nombre": "Palapa"}
            )
            reserva2 = ReservaAreaComunResponse(
                id=2,
                area_comun_id=2,
                departamento_id=sample_departamento.id,
                periodo_inicio=self.fecha_inicio + timedelta(days=2),
                periodo_fin=self.fecha_fin + timedelta(days=2),
                estado="activa",
                area_comun={"id": 2, "nombre": "Roof Gardens"}
            )
            expected_reservas = [reserva1, reserva2]
            mock_service.get_user_reservas.return_value = expected_reservas
            
            # Realizar petición
            response = self.client.get(f"{self.base_url}/usuario")
            
            # Verificar respuesta
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2
            assert data[0]["id"] == 1
            assert data[1]["id"] == 2
            assert data[0]["estado"] == "activa"
            assert data[1]["estado"] == "activa"
            
            # Verificar que se llamó el servicio
            mock_service.get_user_reservas.assert_called_once_with(mock_db, mock_user.id)
    
    def test_create_reserva_unauthorized(self):
        """Test cuando el usuario no está autenticado"""
        # Datos de la reserva
        reserva_data = {
            "area_comun_id": 1,
            "periodo_inicio": self.fecha_inicio.isoformat(),
            "periodo_fin": self.fecha_fin.isoformat()
        }
        
        # Realizar petición sin autenticación
        response = self.client.post(f"{self.base_url}/", json=reserva_data)
        
        # Verificar respuesta
        assert response.status_code == 422  # FastAPI validation error for missing dependency
    
    def test_get_user_reservas_unauthorized(self):
        """Test cuando el usuario no está autenticado"""
        # Realizar petición sin autenticación
        response = self.client.get(f"{self.base_url}/usuario")
        
        # Verificar respuesta
        assert response.status_code == 422  # FastAPI validation error for missing dependency
