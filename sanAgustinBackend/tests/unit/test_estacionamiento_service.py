import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException

from services.estacionamiento_service import EstacionamientoService
from models.schemas.estacionamiento import EstacionamientoResponse, EstacionamientoUpdate
from models.database.departamento import Departamento
from models.database.estacionamiento import Estacionamiento

class TestEstacionamientoService:
    """Tests unitarios para EstacionamientoService"""
    
    def setup_method(self):
        """Configuración inicial para cada test"""
        self.service = EstacionamientoService()
        self.mock_db = Mock()
        self.usuario_id = 1
        self.estacionamiento_id = 1
    
    def test_update_estacionamiento_success(self, sample_departamento, sample_estacionamiento):
        """Test exitoso para actualizar estacionamiento"""
        # Configurar mocks
        self.service.departamento_repo.get_by_usuario_id.return_value = sample_departamento
        self.service.estacionamiento_repo.get_by_departamento_id.return_value = sample_estacionamiento
        
        # Crear datos de actualización
        update_data = EstacionamientoUpdate(
            placa="XYZ789",
            modelo_auto="Honda Civic",
            color_auto="Negro"
        )
        
        # Mock del estacionamiento actualizado
        updated_estacionamiento = Estacionamiento(
            id=sample_estacionamiento.id,
            numero=sample_estacionamiento.numero,
            placa="XYZ789",
            modelo_auto="Honda Civic",
            color_auto="Negro",
            es_visita=False,
            departamento_id=sample_departamento.id
        )
        self.service.estacionamiento_repo.update.return_value = updated_estacionamiento
        
        # Ejecutar método
        result = self.service.update_estacionamiento(self.mock_db, self.estacionamiento_id, self.usuario_id, update_data)
        
        # Verificar llamadas
        self.service.departamento_repo.get_by_usuario_id.assert_called_once_with(self.mock_db, self.usuario_id)
        self.service.estacionamiento_repo.get_by_departamento_id.assert_called_once_with(self.mock_db, sample_departamento.id, es_visita=False)
        self.service.estacionamiento_repo.update.assert_called_once()
        
        # Verificar resultado
        assert isinstance(result, EstacionamientoResponse)
        assert result.placa == "XYZ789"
        assert result.modelo_auto == "Honda Civic"
        assert result.color_auto == "Negro"
    
    def test_update_estacionamiento_no_departamento(self):
        """Test cuando el usuario no tiene departamento asociado"""
        # Configurar mock para retornar None
        self.service.departamento_repo.get_by_usuario_id.return_value = None
        
        update_data = EstacionamientoUpdate(placa="XYZ789")
        
        # Verificar que se lanza la excepción correcta
        with pytest.raises(HTTPException) as exc_info:
            self.service.update_estacionamiento(self.mock_db, self.estacionamiento_id, self.usuario_id, update_data)
        
        assert exc_info.value.status_code == 404
        assert "No se encontró departamento asociado al usuario" in str(exc_info.value.detail)
    
    def test_update_estacionamiento_no_estacionamiento(self, sample_departamento):
        """Test cuando el departamento no tiene estacionamiento"""
        # Configurar mocks
        self.service.departamento_repo.get_by_usuario_id.return_value = sample_departamento
        self.service.estacionamiento_repo.get_by_departamento_id.return_value = None
        
        update_data = EstacionamientoUpdate(placa="XYZ789")
        
        # Verificar que se lanza la excepción correcta
        with pytest.raises(HTTPException) as exc_info:
            self.service.update_estacionamiento(self.mock_db, self.estacionamiento_id, self.usuario_id, update_data)
        
        assert exc_info.value.status_code == 404
        assert "Estacionamiento no encontrado" in str(exc_info.value.detail)
    
    def test_update_estacionamiento_wrong_id(self, sample_departamento, sample_estacionamiento):
        """Test cuando el ID del estacionamiento no coincide"""
        # Configurar mocks
        self.service.departamento_repo.get_by_usuario_id.return_value = sample_departamento
        self.service.estacionamiento_repo.get_by_departamento_id.return_value = sample_estacionamiento
        
        update_data = EstacionamientoUpdate(placa="XYZ789")
        wrong_estacionamiento_id = 999
        
        # Verificar que se lanza la excepción correcta
        with pytest.raises(HTTPException) as exc_info:
            self.service.update_estacionamiento(self.mock_db, wrong_estacionamiento_id, self.usuario_id, update_data)
        
        assert exc_info.value.status_code == 404
        assert "Estacionamiento no encontrado" in str(exc_info.value.detail)
    
    def test_update_estacionamiento_partial_data(self, sample_departamento, sample_estacionamiento):
        """Test para actualización parcial de datos"""
        # Configurar mocks
        self.service.departamento_repo.get_by_usuario_id.return_value = sample_departamento
        self.service.estacionamiento_repo.get_by_departamento_id.return_value = sample_estacionamiento
        
        # Crear datos de actualización parcial
        update_data = EstacionamientoUpdate(placa="XYZ789")  # Solo placa
        
        # Mock del estacionamiento actualizado
        updated_estacionamiento = Estacionamiento(
            id=sample_estacionamiento.id,
            numero=sample_estacionamiento.numero,
            placa="XYZ789",
            modelo_auto=sample_estacionamiento.modelo_auto,  # Sin cambios
            color_auto=sample_estacionamiento.color_auto,    # Sin cambios
            es_visita=False,
            departamento_id=sample_departamento.id
        )
        self.service.estacionamiento_repo.update.return_value = updated_estacionamiento
        
        # Ejecutar método
        result = self.service.update_estacionamiento(self.mock_db, self.estacionamiento_id, self.usuario_id, update_data)
        
        # Verificar resultado
        assert result.placa == "XYZ789"
        assert result.modelo_auto == sample_estacionamiento.modelo_auto
        assert result.color_auto == sample_estacionamiento.color_auto
    
    def test_update_estacionamiento_empty_data(self, sample_departamento, sample_estacionamiento):
        """Test para actualización con datos vacíos"""
        # Configurar mocks
        self.service.departamento_repo.get_by_usuario_id.return_value = sample_departamento
        self.service.estacionamiento_repo.get_by_departamento_id.return_value = sample_estacionamiento
        
        # Crear datos de actualización vacíos
        update_data = EstacionamientoUpdate()
        
        # Mock del estacionamiento sin cambios
        self.service.estacionamiento_repo.update.return_value = sample_estacionamiento
        
        # Ejecutar método
        result = self.service.update_estacionamiento(self.mock_db, self.estacionamiento_id, self.usuario_id, update_data)
        
        # Verificar que no se llamó update porque no hay datos para actualizar
        self.service.estacionamiento_repo.update.assert_called_once()
        assert result == sample_estacionamiento
