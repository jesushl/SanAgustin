import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException
from datetime import datetime, timedelta

from services.panel_residente_service import PanelResidenteService
from models.schemas.panel_residente import PanelResidenteResponse
from models.database.departamento import Departamento
from models.database.estacionamiento import Estacionamiento
from models.database.adeudo import Adeudo

class TestPanelResidenteService:
    """Tests unitarios para PanelResidenteService"""
    
    def setup_method(self):
        """Configuración inicial para cada test"""
        self.service = PanelResidenteService()
        self.mock_db = Mock()
        self.usuario_id = 1
    
    def test_get_panel_residente_success(self, sample_departamento, sample_estacionamiento, sample_adeudo):
        """Test exitoso para obtener panel de residente"""
        # Configurar mocks
        self.service.departamento_repo.get_by_usuario_id.return_value = sample_departamento
        self.service.estacionamiento_repo.get_by_departamento_id.return_value = sample_estacionamiento
        self.service.adeudo_repo.get_pendientes_by_departamento_id.return_value = [sample_adeudo]
        self.service.adeudo_repo.get_total_adeudos_by_departamento_id.return_value = 1500.0
        
        # Ejecutar método
        result = self.service.get_panel_residente(self.mock_db, self.usuario_id)
        
        # Verificar llamadas
        self.service.departamento_repo.get_by_usuario_id.assert_called_once_with(self.mock_db, self.usuario_id)
        self.service.estacionamiento_repo.get_by_departamento_id.assert_called_once_with(self.mock_db, sample_departamento.id, es_visita=False)
        self.service.adeudo_repo.get_pendientes_by_departamento_id.assert_called_once_with(self.mock_db, sample_departamento.id)
        self.service.adeudo_repo.get_total_adeudos_by_departamento_id.assert_called_once_with(self.mock_db, sample_departamento.id)
        
        # Verificar resultado
        assert isinstance(result, PanelResidenteResponse)
        assert result.departamento == sample_departamento
        assert result.estacionamiento == sample_estacionamiento
        assert result.adeudos_pendientes == [sample_adeudo]
        assert result.total_adeudos == 1500.0
        assert result.puede_reservar == False  # Tiene adeudos
    
    def test_get_panel_residente_no_departamento(self):
        """Test cuando el usuario no tiene departamento asociado"""
        # Configurar mock para retornar None
        self.service.departamento_repo.get_by_usuario_id.return_value = None
        
        # Verificar que se lanza la excepción correcta
        with pytest.raises(HTTPException) as exc_info:
            self.service.get_panel_residente(self.mock_db, self.usuario_id)
        
        assert exc_info.value.status_code == 404
        assert "No se encontró departamento asociado al usuario" in str(exc_info.value.detail)
    
    def test_get_panel_residente_no_estacionamiento(self, sample_departamento):
        """Test cuando el departamento no tiene estacionamiento"""
        # Configurar mocks
        self.service.departamento_repo.get_by_usuario_id.return_value = sample_departamento
        self.service.estacionamiento_repo.get_by_departamento_id.return_value = None
        self.service.adeudo_repo.get_pendientes_by_departamento_id.return_value = []
        self.service.adeudo_repo.get_total_adeudos_by_departamento_id.return_value = 0.0
        
        # Ejecutar método
        result = self.service.get_panel_residente(self.mock_db, self.usuario_id)
        
        # Verificar resultado
        assert result.estacionamiento is None
        assert result.puede_reservar == True  # No tiene adeudos
    
    def test_get_panel_residente_no_adeudos(self, sample_departamento, sample_estacionamiento):
        """Test cuando el departamento no tiene adeudos pendientes"""
        # Configurar mocks
        self.service.departamento_repo.get_by_usuario_id.return_value = sample_departamento
        self.service.estacionamiento_repo.get_by_departamento_id.return_value = sample_estacionamiento
        self.service.adeudo_repo.get_pendientes_by_departamento_id.return_value = []
        self.service.adeudo_repo.get_total_adeudos_by_departamento_id.return_value = 0.0
        
        # Ejecutar método
        result = self.service.get_panel_residente(self.mock_db, self.usuario_id)
        
        # Verificar resultado
        assert result.adeudos_pendientes == []
        assert result.total_adeudos == 0.0
        assert result.puede_reservar == True
    
    def test_get_panel_residente_multiple_adeudos(self, sample_departamento, sample_estacionamiento):
        """Test cuando el departamento tiene múltiples adeudos"""
        # Crear múltiples adeudos
        adeudo1 = Adeudo(id=1, departamento_id=sample_departamento.id, monto=1000.0, descripcion="Adeudo 1", 
                        fecha_vencimiento=datetime.now(), fecha_creacion=datetime.now(), pagado=False)
        adeudo2 = Adeudo(id=2, departamento_id=sample_departamento.id, monto=500.0, descripcion="Adeudo 2", 
                        fecha_vencimiento=datetime.now(), fecha_creacion=datetime.now(), pagado=False)
        
        # Configurar mocks
        self.service.departamento_repo.get_by_usuario_id.return_value = sample_departamento
        self.service.estacionamiento_repo.get_by_departamento_id.return_value = sample_estacionamiento
        self.service.adeudo_repo.get_pendientes_by_departamento_id.return_value = [adeudo1, adeudo2]
        self.service.adeudo_repo.get_total_adeudos_by_departamento_id.return_value = 1500.0
        
        # Ejecutar método
        result = self.service.get_panel_residente(self.mock_db, self.usuario_id)
        
        # Verificar resultado
        assert len(result.adeudos_pendientes) == 2
        assert result.total_adeudos == 1500.0
        assert result.puede_reservar == False
