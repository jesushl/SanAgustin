# Tests - San Agustín Backend

Este directorio contiene todos los tests del proyecto San Agustín, organizados por tipo y funcionalidad.

## 📁 Estructura de Tests

```
tests/
├── conftest.py                    # Configuración y fixtures de pytest
├── unit/                          # Tests unitarios
│   ├── test_panel_residente_service.py
│   ├── test_estacionamiento_service.py
│   └── test_reserva_area_comun_service.py
├── integration/                   # Tests de integración
│   ├── test_panel_residente_endpoints.py
│   └── test_reserva_area_comun_endpoints.py
├── fixtures/                      # Datos de prueba (futuro)
└── README.md                      # Esta documentación
```

## 🧪 Tipos de Tests

### **Tests Unitarios (`tests/unit/`)**
- **Propósito**: Probar la lógica de negocio de forma aislada
- **Alcance**: Servicios individuales con mocks de dependencias
- **Ejecución**: Rápida, sin dependencias externas
- **Cobertura**: Lógica de negocio, validaciones, manejo de errores

### **Tests de Integración (`tests/integration/`)**
- **Propósito**: Probar la integración entre capas
- **Alcance**: Endpoints completos con mocks de servicios
- **Ejecución**: Media velocidad, simula peticiones HTTP
- **Cobertura**: Flujo completo de request/response, validaciones de API

## 🚀 Ejecución de Tests

### **Ejecutar todos los tests**
```bash
python run_tests.py
```

### **Ejecutar tests unitarios**
```bash
pytest tests/unit/ -v
```

### **Ejecutar tests de integración**
```bash
pytest tests/integration/ -v
```

### **Ejecutar tests específicos**
```bash
# Test específico
pytest tests/unit/test_panel_residente_service.py::TestPanelResidenteService::test_get_panel_residente_success -v

# Tests con marcador específico
pytest -m unit -v
pytest -m integration -v
```

### **Con cobertura de código**
```bash
pytest tests/ --cov=services --cov=repositories --cov=models --cov-report=term-missing --cov-report=html:htmlcov
```

## 📊 Cobertura de Código

Los tests incluyen reportes de cobertura que muestran:

- **Cobertura por línea**: Qué líneas de código se ejecutan
- **Cobertura por función**: Qué funciones se prueban
- **Cobertura por módulo**: Qué módulos se cubren

### **Ver reporte de cobertura**
```bash
# Abrir en navegador
open htmlcov/index.html

# Ver en terminal
pytest --cov=services --cov-report=term-missing
```

## 🔧 Configuración

### **pytest.ini**
Configuración principal de pytest:
- Patrones de archivos de test
- Marcadores personalizados
- Opciones de cobertura
- Configuración de salida

### **conftest.py**
Fixtures compartidas para todos los tests:
- Configuración de base de datos de prueba
- Fixtures de datos de ejemplo
- Mocks de dependencias
- Configuración de cliente HTTP

## 📋 Fixtures Disponibles

### **Datos de Ejemplo**
- `sample_departamento`: Departamento de prueba
- `sample_estacionamiento`: Estacionamiento de prueba
- `sample_area_comun`: Área común de prueba
- `sample_lugar_visita`: Lugar de visita de prueba
- `sample_adeudo`: Adeudo de prueba
- `sample_reserva_area_comun`: Reserva de área común de prueba
- `sample_reserva_visita`: Reserva de visita de prueba

### **Mocks**
- `mock_current_user`: Usuario autenticado mock
- `mock_auth_dependency`: Dependencia de autenticación mock
- `mock_db_dependency`: Dependencia de base de datos mock

### **Configuración**
- `db_engine`: Engine de base de datos de prueba
- `db_session`: Sesión de base de datos para cada test
- `client`: Cliente HTTP para tests de integración

## 🎯 Casos de Prueba Cubiertos

### **Panel de Residente**
- ✅ Obtener panel con datos completos
- ✅ Usuario sin departamento asociado
- ✅ Departamento sin estacionamiento
- ✅ Departamento sin adeudos
- ✅ Departamento con múltiples adeudos
- ✅ Usuario no autenticado

### **Estacionamiento**
- ✅ Actualizar datos del vehículo
- ✅ Usuario sin departamento
- ✅ Departamento sin estacionamiento
- ✅ ID de estacionamiento incorrecto
- ✅ Actualización parcial de datos
- ✅ Datos de actualización vacíos

### **Reservas de Área Común**
- ✅ Verificar disponibilidad (disponible)
- ✅ Verificar disponibilidad (no disponible)
- ✅ Crear reserva exitosa
- ✅ Usuario sin departamento
- ✅ Usuario con adeudos pendientes
- ✅ Área común no disponible
- ✅ Obtener reservas del usuario
- ✅ Usuario no autenticado

## 📝 Convenciones de Nomenclatura

### **Archivos de Test**
- `test_*.py`: Archivos de test
- `test_*_service.py`: Tests de servicios
- `test_*_endpoints.py`: Tests de endpoints

### **Clases de Test**
- `Test*Service`: Tests de servicios
- `Test*Endpoints`: Tests de endpoints

### **Métodos de Test**
- `test_*_success`: Casos exitosos
- `test_*_failure`: Casos de fallo
- `test_*_edge_case`: Casos límite
- `test_*_unauthorized`: Casos sin autenticación

## 🔍 Debugging de Tests

### **Ejecutar test específico con más detalle**
```bash
pytest tests/unit/test_panel_residente_service.py::TestPanelResidenteService::test_get_panel_residente_success -v -s
```

### **Ver logs detallados**
```bash
pytest tests/ -v -s --log-cli-level=DEBUG
```

### **Ejecutar tests fallidos**
```bash
pytest tests/ --lf -v
```

## 🛠️ Agregar Nuevos Tests

### **1. Test Unitario de Servicio**
```python
# tests/unit/test_nuevo_service.py
import pytest
from unittest.mock import Mock
from services.nuevo_service import NuevoService

class TestNuevoService:
    def setup_method(self):
        self.service = NuevoService()
        self.mock_db = Mock()
    
    def test_nuevo_metodo_success(self, sample_data):
        # Configurar mocks
        self.service.repo.get.return_value = sample_data
        
        # Ejecutar método
        result = self.service.nuevo_metodo(self.mock_db, 1)
        
        # Verificar resultado
        assert result == sample_data
        self.service.repo.get.assert_called_once_with(self.mock_db, 1)
```

### **2. Test de Integración de Endpoint**
```python
# tests/integration/test_nuevo_endpoints.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from main import app

class TestNuevoEndpoints:
    def setup_method(self):
        self.client = TestClient(app)
    
    @patch('services.endpoints.nuevo_endpoints.get_current_user')
    @patch('services.endpoints.nuevo_endpoints.get_db')
    def test_nuevo_endpoint_success(self, mock_get_db, mock_get_current_user):
        # Configurar mocks
        mock_user = Mock()
        mock_user.id = 1
        mock_get_current_user.return_value = mock_user
        
        # Mock del servicio
        with patch('services.endpoints.nuevo_endpoints.NuevoService') as mock_service_class:
            mock_service = Mock()
            mock_service_class.return_value = mock_service
            mock_service.nuevo_metodo.return_value = {"result": "success"}
            
            # Realizar petición
            response = self.client.get("/nuevo-endpoint")
            
            # Verificar respuesta
            assert response.status_code == 200
            assert response.json()["result"] == "success"
```

## 📚 Recursos Adicionales

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)
