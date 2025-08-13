#!/bin/bash

# Script de Ambiente de Desarrollo - San Agustín
# Sistema de Gestión de Residencias

echo "🏠 San Agustín - Ambiente de Desarrollo"
echo "========================================"
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir con colores
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar prerrequisitos
print_status "Verificando prerrequisitos..."

# Verificar Python
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 no está instalado"
    exit 1
fi

# Verificar Node.js
if ! command -v node &> /dev/null; then
    print_error "Node.js no está instalado"
    exit 1
fi

# Verificar npm
if ! command -v npm &> /dev/null; then
    print_error "npm no está instalado"
    exit 1
fi

# Verificar curl
if ! command -v curl &> /dev/null; then
    print_warning "curl no está instalado - algunas funciones de testing no estarán disponibles"
fi

print_success "Prerrequisitos verificados"
echo ""

# Función para manejar la interrupción
cleanup() {
    echo ""
    print_status "Deteniendo servidores..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    print_success "Servidores detenidos"
    exit 0
}

# Capturar interrupción
trap cleanup SIGINT

# Función para verificar si un puerto está en uso
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        return 0
    else
        return 1
    fi
}

# Función para esperar a que un servicio esté disponible
wait_for_service() {
    local url=$1
    local service_name=$2
    local max_attempts=30
    local attempt=1
    
    print_status "Esperando a que $service_name esté disponible..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s "$url" > /dev/null 2>&1; then
            print_success "$service_name está disponible"
            return 0
        fi
        
        echo -n "."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    print_error "$service_name no está disponible después de $max_attempts intentos"
    return 1
}

# Función para ejecutar tests básicos
run_basic_tests() {
    print_status "Ejecutando tests básicos..."
    echo ""
    
    # Test del backend
    print_status "Testing Backend API..."
    
    # Health check
    if curl -s http://localhost:8000/health | grep -q "healthy"; then
        print_success "✅ Backend health check: OK"
    else
        print_error "❌ Backend health check: FAILED"
    fi
    
    # API docs
    if curl -s http://localhost:8000/docs > /dev/null; then
        print_success "✅ API Documentation: OK"
    else
        print_error "❌ API Documentation: FAILED"
    fi
    
    # Test del frontend
    print_status "Testing Frontend..."
    
    if curl -s http://localhost:5173 | grep -q "San Agustín"; then
        print_success "✅ Frontend: OK"
    else
        print_error "❌ Frontend: FAILED"
    fi
    
    echo ""
}

# Función para mostrar información de endpoints
show_endpoints_info() {
    echo ""
    print_status "📋 Información de Endpoints:"
    echo ""
    echo "🌐 Frontend (React):"
    echo "   - URL: http://localhost:5173"
    echo "   - Rutas principales: /, /login, /register, /panel-residente, /admin"
    echo "   - Reservas: /reserva-area-comun, /reserva-visita"
    echo ""
    echo "🔧 Backend (FastAPI):"
    echo "   - URL: http://localhost:8000"
    echo "   - Health: http://localhost:8000/health"
    echo "   - API Docs: http://localhost:8000/docs"
    echo "   - OpenAPI: http://localhost:8000/openapi.json"
    echo ""
    echo "🔐 Autenticación:"
    echo "   - Google OAuth: http://localhost:8000/auth/google/login"
    echo "   - Facebook OAuth: http://localhost:8000/auth/facebook/login"
    echo ""
    echo "👤 Usuarios de prueba:"
    echo "   - Residente: residente@test.com"
    echo "   - Admin: admin@test.com"
    echo ""
}

# Función para crear archivo de configuración de testing
create_test_config() {
    print_status "Creando configuración de testing..."
    
    cat > test-config.json << EOF
{
  "backend": {
    "base_url": "http://localhost:8000",
    "health_endpoint": "/health",
    "docs_endpoint": "/docs"
  },
  "frontend": {
    "base_url": "http://localhost:5173"
  },
  "auth": {
    "test_users": {
      "residente": "residente@test.com",
      "admin": "admin@test.com"
    },
    "oauth": {
      "google": "/auth/google/login",
      "facebook": "/auth/facebook/login"
    }
  },
  "endpoints": {
    "panel_residente": "/panel-residente",
    "areas_comunes": "/areas-comunes",
    "reservas_area_comun": "/reservas-area-comun",
    "lugares_visita": "/lugares-visita",
    "reservas_visita": "/reservas-visita",
    "estacionamiento": "/estacionamiento"
  }
}
EOF
    
    print_success "Configuración de testing creada: test-config.json"
}

# Backend
print_status "Configurando Backend..."
cd sanAgustinBackend

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    print_status "Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
print_status "Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias si no están instaladas
if [ ! -f "venv/lib/python*/site-packages/fastapi" ]; then
    print_status "Instalando dependencias de Python..."
    pip install -r requirements.txt
fi

# Verificar si la base de datos existe
if [ ! -f "comunidad.db" ]; then
    print_status "Creando base de datos..."
    python poblar_simple.py
    python asociar_usuario.py
fi

print_status "Iniciando servidor backend..."
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Esperar a que el backend se inicie
sleep 3

# Frontend
print_status "Configurando Frontend..."
cd ../san-agustin-frontend

# Instalar dependencias si no están instaladas
if [ ! -d "node_modules" ]; then
    print_status "Instalando dependencias de Node.js..."
    npm install
fi

print_status "Iniciando servidor frontend..."
npm run dev &
FRONTEND_PID=$!

# Esperar a que los servicios estén disponibles
wait_for_service "http://localhost:8000/health" "Backend"
wait_for_service "http://localhost:5173" "Frontend"

# Crear configuración de testing
create_test_config

# Ejecutar tests básicos
run_basic_tests

# Mostrar información de endpoints
show_endpoints_info

print_success "🎉 Ambiente de desarrollo iniciado exitosamente!"
echo ""
print_status "Comandos útiles:"
echo "  - Ver logs del backend: tail -f sanAgustinBackend/logs/app.log"
echo "  - Test de endpoints: curl http://localhost:8000/health"
echo "  - Abrir API docs: xdg-open http://localhost:8000/docs"
echo "  - Abrir frontend: xdg-open http://localhost:5173"
echo ""
print_status "Presiona Ctrl+C para detener los servidores"
echo ""

# Esperar a que se presione Ctrl+C
wait
