#!/bin/bash

# Script de Testing de Endpoints - San Agustín
# Sistema de Gestión de Residencias

echo "🧪 Testing de Endpoints - San Agustín"
echo "====================================="
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables
BASE_URL="http://localhost:8000"
FRONTEND_URL="http://localhost:5173"
TEST_TOKEN=""

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

# Función para hacer requests HTTP
make_request() {
    local method=$1
    local endpoint=$2
    local data=$3
    local description=$4
    
    echo -n "Testing $description... "
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "%{http_code}" "$BASE_URL$endpoint")
    elif [ "$method" = "POST" ]; then
        response=$(curl -s -w "%{http_code}" -X POST -H "Content-Type: application/json" -d "$data" "$BASE_URL$endpoint")
    elif [ "$method" = "PUT" ]; then
        response=$(curl -s -w "%{http_code}" -X PUT -H "Content-Type: application/json" -d "$data" "$BASE_URL$endpoint")
    fi
    
    http_code="${response: -3}"
    body="${response%???}"
    
    if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
        print_success "OK ($http_code)"
    else
        print_error "FAILED ($http_code)"
        echo "Response: $body"
    fi
}

# Función para hacer requests con autenticación
make_auth_request() {
    local method=$1
    local endpoint=$2
    local data=$3
    local description=$4
    
    echo -n "Testing $description... "
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "%{http_code}" -H "Authorization: Bearer $TEST_TOKEN" "$BASE_URL$endpoint")
    elif [ "$method" = "POST" ]; then
        response=$(curl -s -w "%{http_code}" -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $TEST_TOKEN" -d "$data" "$BASE_URL$endpoint")
    elif [ "$method" = "PUT" ]; then
        response=$(curl -s -w "%{http_code}" -X PUT -H "Content-Type: application/json" -H "Authorization: Bearer $TEST_TOKEN" -d "$data" "$BASE_URL$endpoint")
    fi
    
    http_code="${response: -3}"
    body="${response%???}"
    
    if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
        print_success "OK ($http_code)"
    else
        print_error "FAILED ($http_code)"
        echo "Response: $body"
    fi
}

# Verificar que los servicios estén corriendo
print_status "Verificando que los servicios estén corriendo..."

if ! curl -s "$BASE_URL/health" > /dev/null; then
    print_error "Backend no está corriendo en $BASE_URL"
    exit 1
fi

if ! curl -s "$FRONTEND_URL" > /dev/null; then
    print_error "Frontend no está corriendo en $FRONTEND_URL"
    exit 1
fi

print_success "Servicios verificados"
echo ""

# Test 1: Endpoints públicos del backend
print_status "🔧 Testing Endpoints Públicos del Backend"
echo ""

make_request "GET" "/health" "" "Health Check"
make_request "GET" "/" "" "Root Endpoint"
make_request "GET" "/docs" "" "API Documentation"
make_request "GET" "/openapi.json" "" "OpenAPI Schema"

echo ""

# Test 2: Endpoints de autenticación
print_status "🔐 Testing Endpoints de Autenticación"
echo ""

make_request "GET" "/auth/google/login" "" "Google OAuth Login"
make_request "GET" "/auth/facebook/login" "" "Facebook OAuth Login"

# Test de registro (sin autenticación)
register_data='{"email":"test@example.com","nombre":"Test","apellido":"User","provider":"test","provider_id":"123"}'
make_request "POST" "/auth/register" "$register_data" "User Registration"

echo ""

# Test 3: Endpoints que requieren autenticación
print_status "👤 Testing Endpoints con Autenticación"
echo ""

print_warning "Nota: Algunos endpoints requieren autenticación. Los tests pueden fallar sin token válido."
echo ""

# Panel de residente
make_auth_request "GET" "/panel-residente" "" "Panel Residente"

# Áreas comunes
make_auth_request "GET" "/areas-comunes" "" "Get Areas Comunes"

# Verificar disponibilidad de área común
disponibilidad_params="?area_comun_id=1&fecha_inicio=2024-01-01T10:00:00&fecha_fin=2024-01-01T12:00:00"
make_auth_request "GET" "/reservas-area-comun/disponibilidad$disponibilidad_params" "" "Check Area Común Availability"

# Crear reserva de área común
reserva_area_data='{"area_comun_id":1,"periodo_inicio":"2024-01-01T10:00:00","periodo_fin":"2024-01-01T12:00:00"}'
make_auth_request "POST" "/reservas-area-comun" "$reserva_area_data" "Create Area Común Reservation"

# Obtener reservas del usuario
make_auth_request "GET" "/reservas-area-comun/usuario" "" "Get User Area Común Reservations"

# Lugares de visita
make_auth_request "GET" "/lugares-visita" "" "Get Lugares Visita"

# Verificar disponibilidad de lugar de visita
disponibilidad_visita_params="?lugar_visita_id=1&fecha_inicio=2024-01-01T10:00:00&fecha_fin=2024-01-01T12:00:00"
make_auth_request "GET" "/reservas-visita/disponibilidad$disponibilidad_visita_params" "" "Check Lugar Visita Availability"

# Crear reserva de visita
reserva_visita_data='{"lugar_visita_id":1,"placa_visita":"ABC123","periodo_inicio":"2024-01-01T10:00:00","periodo_fin":"2024-01-01T12:00:00"}'
make_auth_request "POST" "/reservas-visita" "$reserva_visita_data" "Create Visita Reservation"

# Obtener reservas del usuario
make_auth_request "GET" "/reservas-visita/usuario" "" "Get User Visita Reservations"

echo ""

# Test 4: Endpoints de administración
print_status "👨‍💼 Testing Endpoints de Administración"
echo ""

make_auth_request "GET" "/auth/pending-registrations" "" "Get Pending Registrations"

echo ""

# Test 5: Endpoints del frontend
print_status "🌐 Testing Endpoints del Frontend"
echo ""

echo -n "Testing Frontend Home Page... "
if curl -s "$FRONTEND_URL" | grep -q "San Agustín"; then
    print_success "OK"
else
    print_error "FAILED"
fi

echo -n "Testing Frontend Login Page... "
if curl -s "$FRONTEND_URL/login" | grep -q "login"; then
    print_success "OK"
else
    print_error "FAILED"
fi

echo -n "Testing Frontend Register Page... "
if curl -s "$FRONTEND_URL/register" | grep -q "register"; then
    print_success "OK"
else
    print_error "FAILED"
fi

echo ""

# Test 6: Endpoints legacy (si existen)
print_status "🔄 Testing Endpoints Legacy"
echo ""

make_auth_request "GET" "/estacionamientos/1" "" "Get Estacionamiento by ID"
make_auth_request "GET" "/placas/ABC123" "" "Validate Placa"
make_auth_request "GET" "/contactos_residente/" "" "Get Contactos Residente"
make_auth_request "GET" "/adeudos/" "" "Get Adeudos"

echo ""

# Resumen
print_status "📊 Resumen de Testing"
echo ""
print_success "✅ Testing completado"
echo ""
print_status "Para más detalles, revisa:"
echo "  - API Documentation: $BASE_URL/docs"
echo "  - OpenAPI Schema: $BASE_URL/openapi.json"
echo "  - Frontend: $FRONTEND_URL"
echo ""
print_status "Para testing manual con curl:"
echo "  curl -H 'Authorization: Bearer YOUR_TOKEN' $BASE_URL/panel-residente"
echo ""
