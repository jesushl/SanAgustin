# 🏠 San Agustín - Ambiente de Desarrollo

Guía completa para configurar y usar el ambiente de desarrollo del Sistema de Gestión de Residencias San Agustín.

## 📋 Prerrequisitos

- **Python 3.8+**
- **Node.js 16+**
- **npm 8+**
- **curl** (para testing)
- **Git**

## 🚀 Inicio Rápido

### Opción 1: Script Automatizado (Recomendado)

```bash
# Dar permisos de ejecución
chmod +x dev-environment.sh

# Ejecutar ambiente completo
./dev-environment.sh
```

### Opción 2: Inicio Manual

#### Backend (Terminal 1)
```bash
cd sanAgustinBackend
source venv/bin/activate
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend (Terminal 2)
```bash
cd san-agustin-frontend
npm run dev
```

## 🧪 Testing de Endpoints

### Script de Testing Automatizado

```bash
# Dar permisos de ejecución
chmod +x test-endpoints.sh

# Ejecutar tests
./test-endpoints.sh
```

### Testing Manual con curl

```bash
# Health check
curl http://localhost:8000/health

# API Documentation
curl http://localhost:8000/docs

# Panel de residente (requiere token)
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8000/panel-residente

# Áreas comunes
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8000/areas-comunes

# Crear reserva de área común
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"area_comun_id":1,"periodo_inicio":"2024-01-01T10:00:00","periodo_fin":"2024-01-01T12:00:00"}' \
  http://localhost:8000/reservas-area-comun
```

## 📊 Endpoints Disponibles

### 🔧 Backend API (http://localhost:8000)

#### Endpoints Públicos
- `GET /health` - Health check
- `GET /` - Root endpoint
- `GET /docs` - API Documentation (Swagger UI)
- `GET /openapi.json` - OpenAPI Schema

#### Autenticación
- `GET /auth/google/login` - Google OAuth
- `GET /auth/facebook/login` - Facebook OAuth
- `POST /auth/register` - Registro de usuario
- `GET /auth/pending-registrations` - Registros pendientes (admin)
- `POST /auth/approve-registration/{id}` - Aprobar registro (admin)
- `GET /auth/me` - Información del usuario actual

#### Panel de Residente
- `GET /panel-residente` - Datos del panel del residente

#### Áreas Comunes
- `GET /areas-comunes` - Lista de áreas comunes
- `GET /reservas-area-comun/disponibilidad` - Verificar disponibilidad
- `POST /reservas-area-comun` - Crear reserva
- `GET /reservas-area-comun/usuario` - Reservas del usuario

#### Lugares de Visita
- `GET /lugares-visita` - Lista de lugares de visita
- `GET /reservas-visita/disponibilidad` - Verificar disponibilidad
- `POST /reservas-visita` - Crear reserva
- `GET /reservas-visita/usuario` - Reservas del usuario

#### Estacionamiento
- `PUT /estacionamiento/{id}` - Actualizar información

### 🌐 Frontend (http://localhost:5173)

#### Páginas Principales
- `/` - Página de inicio
- `/login` - Inicio de sesión
- `/register` - Registro
- `/panel-residente` - Panel del residente
- `/admin` - Panel de administrador

#### Servicios
- `/reserva-area-comun` - Reserva de áreas comunes
- `/reserva-visita` - Reserva de lugares de visita
- `/editar-vehiculo` - Edición de vehículo

## 🔐 Usuarios de Prueba

### Residente
- **Email:** residente@test.com
- **Rol:** Residente
- **Acceso:** Panel de residente, reservas

### Administrador
- **Email:** admin@test.com
- **Rol:** Administrador
- **Acceso:** Panel de admin, aprobación de registros

## 🛠️ Herramientas de Testing

### 1. Postman/Insomnia Collection

Importa el archivo `postman-collection.json` en Postman o Insomnia para tener acceso a todos los endpoints organizados.

### 2. Variables de Entorno

```bash
# Backend
export BACKEND_URL="http://localhost:8000"
export FRONTEND_URL="http://localhost:5173"

# Para testing con token
export AUTH_TOKEN="your_jwt_token_here"
```

### 3. Testing con curl

```bash
# Ejemplo: Obtener panel de residente
curl -H "Authorization: Bearer $AUTH_TOKEN" \
  "$BACKEND_URL/panel-residente"

# Ejemplo: Crear reserva
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -d '{"area_comun_id":1,"periodo_inicio":"2024-01-01T10:00:00","periodo_fin":"2024-01-01T12:00:00"}' \
  "$BACKEND_URL/reservas-area-comun"
```

## 📁 Estructura del Proyecto

```
SanAgustin/
├── dev-environment.sh          # Script principal de desarrollo
├── test-endpoints.sh           # Script de testing
├── postman-collection.json     # Colección de Postman
├── test-config.json           # Configuración de testing
├── sanAgustinBackend/         # Backend (FastAPI)
│   ├── main.py
│   ├── requirements.txt
│   ├── api/
│   ├── core/
│   ├── models/
│   └── services/
└── san-agustin-frontend/      # Frontend (React)
    ├── package.json
    ├── src/
    │   ├── pages/
    │   ├── components/
    │   ├── services/
    │   └── types/
    └── public/
```

## 🔍 Debugging

### Backend

```bash
# Ver logs en tiempo real
tail -f sanAgustinBackend/logs/app.log

# Ejecutar con debug
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 --log-level debug
```

### Frontend

```bash
# Ver logs de desarrollo
npm run dev

# Build de producción
npm run build
```

## 🚨 Troubleshooting

### Problema: Puerto en uso
```bash
# Verificar puertos
lsof -i :8000
lsof -i :5173

# Matar procesos
kill -9 <PID>
```

### Problema: Dependencias no instaladas
```bash
# Backend
cd sanAgustinBackend
source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd san-agustin-frontend
npm install
```

### Problema: Base de datos corrupta
```bash
cd sanAgustinBackend
rm comunidad.db
python poblar_simple.py
python asociar_usuario.py
```

## 📚 Recursos Adicionales

- **API Documentation:** http://localhost:8000/docs
- **OpenAPI Schema:** http://localhost:8000/openapi.json
- **Frontend:** http://localhost:5173
- **Health Check:** http://localhost:8000/health

## 🤝 Contribución

1. Asegúrate de que todos los tests pasen
2. Verifica que el código funcione en el ambiente de desarrollo
3. Documenta cualquier cambio en los endpoints
4. Actualiza esta documentación si es necesario

---

**¡Disfruta desarrollando en San Agustín! 🏠✨**
