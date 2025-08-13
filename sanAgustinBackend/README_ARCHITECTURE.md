# San Agustín - Arquitectura Separada

Este documento describe la nueva arquitectura separada del proyecto San Agustín, que sigue los principios de Clean Architecture y separación de responsabilidades.

## 🏗️ Estructura de la Arquitectura

```
sanAgustinBackend/
├── main.py                          # Punto de entrada de la aplicación
├── core/                            # Configuración central
│   ├── __init__.py
│   ├── database.py                  # Configuración de base de datos
│   ├── auth.py                      # Configuración de autenticación
│   └── oauth_config.py              # Configuración OAuth
├── models/                          # Capa de modelos
│   ├── database/                    # Modelos de SQLAlchemy
│   │   ├── __init__.py
│   │   ├── base.py                  # Base declarativa
│   │   ├── departamento.py
│   │   ├── area_comun.py
│   │   ├── lugar_visita.py
│   │   ├── estacionamiento.py
│   │   ├── reserva_area_comun.py
│   │   ├── reserva_visita.py
│   │   └── adeudo.py
│   └── schemas/                     # Esquemas Pydantic
│       ├── __init__.py
│       ├── departamento.py
│       ├── estacionamiento.py
│       ├── area_comun.py
│       ├── lugar_visita.py
│       ├── reserva_area_comun.py
│       ├── reserva_visita.py
│       ├── adeudo.py
│       └── panel_residente.py
├── repositories/                    # Capa de acceso a datos
│   ├── __init__.py
│   ├── base_repository.py           # Repositorio base genérico
│   ├── departamento_repository.py
│   ├── estacionamiento_repository.py
│   ├── area_comun_repository.py
│   ├── lugar_visita_repository.py
│   ├── reserva_area_comun_repository.py
│   ├── reserva_visita_repository.py
│   └── adeudo_repository.py
├── services/                        # Capa de lógica de negocio
│   ├── __init__.py
│   ├── panel_residente_service.py
│   ├── estacionamiento_service.py
│   ├── area_comun_service.py
│   ├── lugar_visita_service.py
│   ├── reserva_area_comun_service.py
│   ├── reserva_visita_service.py
│   └── endpoints/                   # Endpoints de la API
│       ├── __init__.py
│       ├── panel_residente_endpoints.py
│       ├── estacionamiento_endpoints.py
│       ├── area_comun_endpoints.py
│       ├── lugar_visita_endpoints.py
│       ├── reserva_area_comun_endpoints.py
│       └── reserva_visita_endpoints.py
├── api/                            # Rutas de autenticación
│   └── auth_routes.py
└── test_architecture.py            # Script de pruebas de arquitectura
```

## 📋 Principios de la Arquitectura

### 1. **Separación de Responsabilidades**
- **Models**: Definición de estructuras de datos
- **Repositories**: Acceso y manipulación de datos
- **Services**: Lógica de negocio
- **Endpoints**: Controladores de la API
- **Core**: Configuración central

### 2. **Inversión de Dependencias**
- Los servicios dependen de abstracciones (repositorios)
- Los endpoints dependen de servicios
- No hay dependencias circulares

### 3. **Principio de Responsabilidad Única**
- Cada clase tiene una sola responsabilidad
- Cada módulo tiene un propósito específico

### 4. **Reutilización de Código**
- Repositorio base genérico para operaciones CRUD comunes
- Servicios especializados para lógica de negocio específica

## 🔧 Componentes de la Arquitectura

### **Models (Modelos)**

#### Database Models (SQLAlchemy)
```python
# models/database/departamento.py
class Departamento(Base):
    __tablename__ = "departamentos"
    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String, index=True, unique=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="departamento")
    estacionamientos = relationship("Estacionamiento", back_populates="departamento")
```

#### Schemas (Pydantic)
```python
# models/schemas/departamento.py
class DepartamentoResponse(BaseModel):
    id: int
    numero: str
    usuario_id: Optional[int] = None
    
    model_config = {
        "from_attributes": True
    }
```

### **Repositories (Repositorios)**

#### Base Repository
```python
# repositories/base_repository.py
class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def create(self, db: Session, *, obj_in: Dict[str, Any]) -> ModelType:
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
```

#### Specialized Repositories
```python
# repositories/departamento_repository.py
class DepartamentoRepository(BaseRepository[Departamento]):
    def get_by_usuario_id(self, db: Session, usuario_id: int) -> Optional[Departamento]:
        return db.query(Departamento).filter(Departamento.usuario_id == usuario_id).first()
```

### **Services (Servicios)**

```python
# services/panel_residente_service.py
class PanelResidenteService:
    def __init__(self):
        self.departamento_repo = DepartamentoRepository()
        self.estacionamiento_repo = EstacionamientoRepository()
        self.adeudo_repo = AdeudoRepository()

    def get_panel_residente(self, db: Session, usuario_id: int) -> PanelResidenteResponse:
        # Lógica de negocio aquí
        departamento = self.departamento_repo.get_by_usuario_id(db, usuario_id)
        if not departamento:
            raise HTTPException(status_code=404, detail="No se encontró departamento")
        
        # Más lógica de negocio...
        return PanelResidenteResponse(...)
```

### **Endpoints (Controladores)**

```python
# services/endpoints/panel_residente_endpoints.py
@router.get("/", response_model=PanelResidenteResponse)
def obtener_panel_residente(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene toda la información del panel de residente"""
    service = PanelResidenteService()
    return service.get_panel_residente(db, current_user.id)
```

### **Core (Configuración Central)**

```python
# core/database.py
SQLALCHEMY_DATABASE_URL = "sqlite:///./comunidad.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## 🚀 Ventajas de la Nueva Arquitectura

### 1. **Mantenibilidad**
- Código organizado y fácil de navegar
- Cambios localizados en módulos específicos
- Fácil identificación de responsabilidades

### 2. **Testabilidad**
- Cada capa puede ser probada independientemente
- Fácil mockeo de dependencias
- Pruebas unitarias más simples

### 3. **Escalabilidad**
- Fácil agregar nuevas funcionalidades
- Reutilización de código común
- Separación clara de responsabilidades

### 4. **Legibilidad**
- Código más limpio y organizado
- Nombres descriptivos y consistentes
- Documentación clara de cada componente

## 🧪 Pruebas de la Arquitectura

Para verificar que la arquitectura funciona correctamente:

```bash
python test_architecture.py
```

Este script prueba:
- ✅ Importaciones de todos los módulos
- ✅ Conexión a la base de datos
- ✅ Instanciación de servicios
- ✅ Instanciación de repositorios

## 📝 Convenciones de Nomenclatura

### **Archivos y Directorios**
- `models/database/`: Modelos SQLAlchemy
- `models/schemas/`: Esquemas Pydantic
- `repositories/`: Repositorios de acceso a datos
- `services/`: Lógica de negocio
- `services/endpoints/`: Controladores de la API
- `core/`: Configuración central

### **Clases**
- **Models**: `Departamento`, `AreaComun`, `Estacionamiento`
- **Schemas**: `DepartamentoResponse`, `EstacionamientoUpdate`
- **Repositories**: `DepartamentoRepository`, `EstacionamientoRepository`
- **Services**: `PanelResidenteService`, `EstacionamientoService`
- **Endpoints**: `panel_residente_router`, `estacionamiento_router`

### **Métodos**
- **Repositories**: `get()`, `create()`, `update()`, `get_by_field()`
- **Services**: `get_panel_residente()`, `update_estacionamiento()`
- **Endpoints**: `obtener_panel_residente()`, `actualizar_estacionamiento()`

## 🔄 Flujo de Datos

```
Request → Endpoint → Service → Repository → Database
Response ← Endpoint ← Service ← Repository ← Database
```

1. **Request** llega al endpoint
2. **Endpoint** valida datos y llama al servicio
3. **Service** implementa lógica de negocio y usa repositorios
4. **Repository** accede a la base de datos
5. **Response** se construye y retorna al cliente

## 🛠️ Agregar Nuevas Funcionalidades

Para agregar una nueva funcionalidad:

1. **Crear el modelo** en `models/database/`
2. **Crear el esquema** en `models/schemas/`
3. **Crear el repositorio** en `repositories/`
4. **Crear el servicio** en `services/`
5. **Crear el endpoint** en `services/endpoints/`
6. **Registrar el router** en `main.py`

## 📚 Recursos Adicionales

- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Repository Pattern](https://martinfowler.com/eaaCatalog/repository.html)
- [Dependency Injection](https://martinfowler.com/articles/injection.html)
- [FastAPI Best Practices](https://fastapi.tiangolo.com/tutorial/best-practices/)
