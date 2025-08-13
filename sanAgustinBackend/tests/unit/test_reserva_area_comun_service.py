import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException
from datetime import datetime, timedelta

from services.reserva_area_comun_service import ReservaAreaComunService
from models.schemas.reserva_area_comun import ReservaAreaComunCreate, ReservaAreaComunResponse
from models.database.departamento import Departamento
from models.database.area_comun import AreaComun
from models.database.adeudo import Adeudo
from models.database.reserva_area_comun import ReservaAreaComun

class TestReservaAreaComunService:
    """Tests unitarios para ReservaAreaComunService"""
    
    def setup_method(self):
        """Configuración inicial para cada test"""
        self.service = ReservaAreaComunService()
        self.mock_db = Mock()
        self.usuario_id = 1
        self.area_comun_id = 1
        self.fecha_inicio = datetime.now() + timedelta(days=1)
        self.fecha_fin = datetime.now() + timedelta(days=1, hours=2)
    
    def test_check_availability_available(self, sample_area_comun):
        """Test para verificar disponibilidad cuando está disponible"""
        # Configurar mock para retornar lista vacía (sin reservas existentes)
        self.service.reserva_repo.check_availability.return_value = []
        
        # Ejecutar método
        result = self.service.check_availability(self.mock_db, self.area_comun_id, self.fecha_inicio, self.fecha_fin)
        
        # Verificar llamadas
        self.service.reserva_repo.check_availability.assert_called_once_with(
            self.mock_db, self.area_comun_id, self.fecha_inicio, self.fecha_fin
        )
        
        # Verificar resultado
        assert result["disponible"] == True
        assert result["reservas_existentes"] == 0
    
    def test_check_availability_not_available(self, sample_area_comun):
        """Test para verificar disponibilidad cuando no está disponible"""
        # Crear reserva existente
        reserva_existente = ReservaAreaComun(
            id=1,
            area_comun_id=self.area_comun_id,
            departamento_id=1,
            periodo_inicio=self.fecha_inicio,
            periodo_fin=self.fecha_fin,
            estado="activa"
        )
        
        # Configurar mock para retornar reserva existente
        self.service.reserva_repo.check_availability.return_value = [reserva_existente]
        
        # Ejecutar método
        result = self.service.check_availability(self.mock_db, self.area_comun_id, self.fecha_inicio, self.fecha_fin)
        
        # Verificar resultado
        assert result["disponible"] == False
        assert result["reservas_existentes"] == 1
    
    def test_create_reserva_success(self, sample_departamento, sample_area_comun):
        """Test exitoso para crear reserva de área común"""
        # Configurar mocks
        self.service.departamento_repo.get_by_usuario_id.return_value = sample_departamento
        self.service.adeudo_repo.get_pendientes_by_departamento_id.return_value = []
        self.service.reserva_repo.check_availability.return_value = []
        
        # Crear datos de reserva
        reserva_data = ReservaAreaComunCreate(
            area_comun_id=self.area_comun_id,
            periodo_inicio=self.fecha_inicio,
            periodo_fin=self.fecha_fin
        )
        
        # Mock de la nueva reserva
        nueva_reserva = ReservaAreaComun(
            id=1,
            area_comun_id=self.area_comun_id,
            departamento_id=sample_departamento.id,
            periodo_inicio=self.fecha_inicio,
            periodo_fin=self.fecha_fin,
            estado="activa"
        )
        self.service.reserva_repo.create.return_value = nueva_reserva
        self.service.area_comun_repo.get.return_value = sample_area_comun
        
        # Ejecutar método
        result = self.service.create_reserva(self.mock_db, self.usuario_id, reserva_data)
        
        # Verificar llamadas
        self.service.departamento_repo.get_by_usuario_id.assert_called_once_with(self.mock_db, self.usuario_id)
        self.service.adeudo_repo.get_pendientes_by_departamento_id.assert_called_once_with(self.mock_db, sample_departamento.id)
        self.service.reserva_repo.check_availability.assert_called_once_with(self.mock_db, self.area_comun_id, self.fecha_inicio, self.fecha_fin)
        self.service.reserva_repo.create.assert_called_once()
        
        # Verificar resultado
        assert isinstance(result, ReservaAreaComunResponse)
        assert result.area_comun_id == self.area_comun_id
        assert result.departamento_id == sample_departamento.id
    
    def test_create_reserva_no_departamento(self):
        """Test cuando el usuario no tiene departamento asociado"""
        # Configurar mock para retornar None
        self.service.departamento_repo.get_by_usuario_id.return_value = None
        
        reserva_data = ReservaAreaComunCreate(
            area_comun_id=self.area_comun_id,
            periodo_inicio=self.fecha_inicio,
            periodo_fin=self.fecha_fin
        )
        
        # Verificar que se lanza la excepción correcta
        with pytest.raises(HTTPException) as exc_info:
            self.service.create_reserva(self.mock_db, self.usuario_id, reserva_data)
        
        assert exc_info.value.status_code == 404
        assert "No se encontró departamento asociado al usuario" in str(exc_info.value.detail)
    
    def test_create_reserva_with_adeudos(self, sample_departamento):
        """Test cuando el usuario tiene adeudos pendientes"""
        # Configurar mocks
        self.service.departamento_repo.get_by_usuario_id.return_value = sample_departamento
        
        # Crear adeudo pendiente
        adeudo = Adeudo(
            id=1,
            departamento_id=sample_departamento.id,
            monto=1500.0,
            descripcion="Mantenimiento",
            fecha_vencimiento=datetime.now() + timedelta(days=30),
            fecha_creacion=datetime.now(),
            pagado=False
        )
        self.service.adeudo_repo.get_pendientes_by_departamento_id.return_value = [adeudo]
        
        reserva_data = ReservaAreaComunCreate(
            area_comun_id=self.area_comun_id,
            periodo_inicio=self.fecha_inicio,
            periodo_fin=self.fecha_fin
        )
        
        # Verificar que se lanza la excepción correcta
        with pytest.raises(HTTPException) as exc_info:
            self.service.create_reserva(self.mock_db, self.usuario_id, reserva_data)
        
        assert exc_info.value.status_code == 400
        assert "No puede realizar reservas mientras tenga adeudos pendientes" in str(exc_info.value.detail)
    
    def test_create_reserva_not_available(self, sample_departamento):
        """Test cuando el área común no está disponible"""
        # Configurar mocks
        self.service.departamento_repo.get_by_usuario_id.return_value = sample_departamento
        self.service.adeudo_repo.get_pendientes_by_departamento_id.return_value = []
        
        # Crear reserva existente
        reserva_existente = ReservaAreaComun(
            id=1,
            area_comun_id=self.area_comun_id,
            departamento_id=2,  # Otro departamento
            periodo_inicio=self.fecha_inicio,
            periodo_fin=self.fecha_fin,
            estado="activa"
        )
        self.service.reserva_repo.check_availability.return_value = [reserva_existente]
        
        reserva_data = ReservaAreaComunCreate(
            area_comun_id=self.area_comun_id,
            periodo_inicio=self.fecha_inicio,
            periodo_fin=self.fecha_fin
        )
        
        # Verificar que se lanza la excepción correcta
        with pytest.raises(HTTPException) as exc_info:
            self.service.create_reserva(self.mock_db, self.usuario_id, reserva_data)
        
        assert exc_info.value.status_code == 400
        assert "El área común no está disponible en el periodo solicitado" in str(exc_info.value.detail)
    
    def test_get_user_reservas_success(self, sample_departamento):
        """Test exitoso para obtener reservas del usuario"""
        # Configurar mocks
        self.service.departamento_repo.get_by_usuario_id.return_value = sample_departamento
        
        # Crear reservas de ejemplo
        reserva1 = ReservaAreaComun(
            id=1,
            area_comun_id=1,
            departamento_id=sample_departamento.id,
            periodo_inicio=self.fecha_inicio,
            periodo_fin=self.fecha_fin,
            estado="activa"
        )
        reserva2 = ReservaAreaComun(
            id=2,
            area_comun_id=2,
            departamento_id=sample_departamento.id,
            periodo_inicio=self.fecha_inicio + timedelta(days=2),
            periodo_fin=self.fecha_fin + timedelta(days=2),
            estado="activa"
        )
        self.service.reserva_repo.get_by_departamento_id.return_value = [reserva1, reserva2]
        
        # Ejecutar método
        result = self.service.get_user_reservas(self.mock_db, self.usuario_id)
        
        # Verificar llamadas
        self.service.departamento_repo.get_by_usuario_id.assert_called_once_with(self.mock_db, self.usuario_id)
        self.service.reserva_repo.get_by_departamento_id.assert_called_once_with(self.mock_db, sample_departamento.id)
        
        # Verificar resultado
        assert len(result) == 2
        assert all(isinstance(r, ReservaAreaComunResponse) for r in result)
    
    def test_get_user_reservas_no_departamento(self):
        """Test cuando el usuario no tiene departamento asociado"""
        # Configurar mock para retornar None
        self.service.departamento_repo.get_by_usuario_id.return_value = None
        
        # Ejecutar método
        result = self.service.get_user_reservas(self.mock_db, self.usuario_id)
        
        # Verificar resultado
        assert result == []
