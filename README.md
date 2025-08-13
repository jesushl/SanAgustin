# San Agustín - Sistema de Gestión de Residencias

Sistema completo para la gestión de servicios de la privada San Agustín, incluyendo autenticación OAuth, panel de residentes, reservas de áreas comunes y lugares de visita.

## 🚀 Características Principales

### Autenticación y Registro
- **OAuth con Google y Facebook**: Autenticación segura mediante proveedores externos
- **Registro de usuarios**: Sistema de registro pendiente de aprobación por administradores
- **Roles diferenciados**: Usuarios residentes y administradores con permisos específicos

### Panel de Residente
- **Información del departamento**: Visualización del número de departamento asignado
- **Gestión de vehículos**: Información y edición de datos del vehículo registrado
- **Control de adeudos**: Visualización de adeudos pendientes con números en rojo
- **Estado de reservas**: Bloqueo de reservas de áreas comunes si hay adeudos pendientes

### Reservas de Áreas Comunes
- **Calendario interactivo**: Visualización de disponibilidad en tiempo real
- **Validación de adeudos**: Bloqueo automático si el residente tiene adeudos pendientes
- **Múltiples áreas**: Palapa, Roof Gardens, Sala de Eventos, Gimnasio
- **Gestión de reservas**: Creación, visualización y seguimiento de reservas activas

### Reservas de Lugares de Visita
- **Límite de 24 horas**: Validación automática de duración máxima
- **Placa opcional**: Registro opcional de placa del vehículo visitante
- **Calendario de disponibilidad**: Verificación de conflictos de horarios
- **Gestión de reservas**: Seguimiento de todas las reservas de visita

## 🏗️ Arquitectura del Proyecto

### Backend (FastAPI + SQLAlchemy)
```
sanAgustinBackend/
├── main.py                 # Aplicación principal con endpoints
├── models/                 # Modelos de datos
│   ├── auth_models.py     # Modelos de autenticación
│   └── auth_schemas.py    # Esquemas Pydantic
├── api/                   # Rutas de la API
│   └── auth_routes.py     # Rutas de autenticación OAuth
├── services/              # Lógica de negocio
│   └── auth_service.py    # Servicio de autenticación
├── core/                  # Configuración central
│   └── oauth_config.py    # Configuración OAuth
└── poblar_simple.py       # Script de población de datos
```

### Frontend (React + TypeScript + Tailwind CSS)
```
san-agustin-frontend/
├── src/
│   ├── pages/             # Páginas principales
│   │   ├── PanelResidente.tsx
│   │   ├── ReservaAreaComun.tsx
│   │   ├── ReservaVisita.tsx
│   │   ├── EditarVehiculo.tsx
│   │   ├── AuthSuccess.tsx
│   │   └── AuthError.tsx
│   ├── components/        # Componentes reutilizables
│   │   └── Navbar.tsx
│   ├── contexts/          # Contextos de React
│   │   └── AuthContext.tsx
│   ├── services/          # Servicios de API
│   │   └── api.ts
│   └── types/             # Tipos TypeScript
│       └── index.ts
```

## 🛠️ Instalación y Configuración

### Prerrequisitos
- Python 3.8+
- Node.js 16+
- npm o yarn

### Backend

1. **Clonar y configurar el entorno**:
```bash
cd sanAgustinBackend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configurar variables de entorno**:
```bash
# Crear archivo .env con las siguientes variables:
GOOGLE_CLIENT_ID=tu_google_client_id
GOOGLE_CLIENT_SECRET=tu_google_client_secret
FACEBOOK_CLIENT_ID=tu_facebook_client_id
FACEBOOK_CLIENT_SECRET=tu_facebook_client_secret
SECRET_KEY=tu_secret_key_super_seguro
```

3. **Poblar la base de datos**:
```bash
python poblar_simple.py
python asociar_usuario.py
```

4. **Ejecutar el servidor**:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

1. **Instalar dependencias**:
```bash
cd san-agustin-frontend
npm install
```

2. **Ejecutar en modo desarrollo**:
```bash
npm run dev
```

## 🔐 Flujo de Autenticación

1. **Registro/Login**: El usuario accede mediante Google o Facebook OAuth
2. **Verificación**: El sistema verifica si el usuario existe en la base de datos
3. **Registro pendiente**: Si es nuevo, se crea un registro pendiente de aprobación
4. **Aprobación**: Los administradores aprueban los registros pendientes
5. **Acceso**: Una vez aprobado, el usuario puede acceder al panel correspondiente

## 📱 Flujo de Usuario Residente

### Panel Principal
- **Información del departamento**: Número y datos básicos
- **Estado de vehículo**: Placa, modelo, color con opción de edición
- **Adeudos pendientes**: Visualización con números en rojo
- **Estado de reservas**: Indicador de si puede realizar reservas

### Reservas de Áreas Comunes
- **Validación automática**: Bloqueo si hay adeudos pendientes
- **Selección de área**: Palapa, Roof Gardens, Sala de Eventos, Gimnasio
- **Calendario**: Selección de fecha y hora de inicio/fin
- **Confirmación**: Creación de reserva con validación de conflictos

### Reservas de Visita
- **Selección de lugar**: Lugares de visita disponibles (V1-V5)
- **Configuración de tiempo**: Fecha/hora de inicio y fin
- **Validación de 24 horas**: Límite automático de duración
- **Placa opcional**: Registro opcional del vehículo visitante

## 🔧 Endpoints Principales

### Autenticación
- `GET /auth/google/login` - Inicio de login con Google
- `GET /auth/facebook/login` - Inicio de login con Facebook
- `POST /auth/register` - Registro de usuario pendiente
- `GET /auth/me` - Información del usuario actual

### Panel de Residente
- `GET /panel-residente` - Información completa del panel
- `PUT /estacionamiento/{id}` - Actualizar datos del vehículo

### Áreas Comunes
- `GET /areas-comunes` - Listar áreas disponibles
- `GET /reservas-area-comun/disponibilidad` - Verificar disponibilidad
- `POST /reservas-area-comun` - Crear reserva
- `GET /reservas-area-comun/usuario` - Reservas del usuario

### Lugares de Visita
- `GET /lugares-visita` - Listar lugares disponibles
- `GET /reservas-visita/disponibilidad` - Verificar disponibilidad
- `POST /reservas-visita` - Crear reserva
- `GET /reservas-visita/usuario` - Reservas del usuario

## 🎨 Características de la UI

- **Diseño responsivo**: Adaptable a dispositivos móviles y desktop
- **Tailwind CSS**: Estilos modernos y consistentes
- **Indicadores visuales**: Colores rojos para adeudos, estados de reserva
- **Validaciones en tiempo real**: Feedback inmediato al usuario
- **Navegación intuitiva**: Flujo claro entre secciones

## 🔒 Seguridad

- **OAuth 2.0**: Autenticación segura con proveedores externos
- **JWT Tokens**: Manejo seguro de sesiones
- **Validación de permisos**: Control de acceso basado en roles
- **Validación de datos**: Verificación de entrada en frontend y backend
- **Protección CSRF**: Headers de seguridad configurados

## 📊 Base de Datos

### Tablas Principales
- **usuarios**: Información de usuarios autenticados
- **departamentos**: Departamentos de la residencia
- **estacionamientos**: Vehículos registrados
- **areas_comunes**: Áreas disponibles para reserva
- **lugares_visita**: Lugares de visita
- **reservas_area_comun**: Reservas de áreas comunes
- **reservas_visita**: Reservas de lugares de visita
- **adeudos**: Control de adeudos por departamento

## 🚀 Despliegue

### Backend (Producción)
```bash
# Usar Gunicorn para producción
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend (Producción)
```bash
npm run build
# Servir archivos estáticos desde dist/
```

## 🤝 Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

Para soporte técnico o preguntas sobre el proyecto, contactar a través de los issues del repositorio.
