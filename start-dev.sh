#!/bin/bash

# Script para iniciar el entorno de desarrollo completo
# San Agustín - Sistema de Gestión de Servicios

echo "🚀 Iniciando entorno de desarrollo San Agustín..."

# Función para verificar si un puerto está en uso
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️  Puerto $1 ya está en uso"
        return 1
    else
        return 0
    fi
}

# Verificar puertos
echo "🔍 Verificando puertos disponibles..."
if ! check_port 8000; then
    echo "❌ Puerto 8000 (backend) no está disponible"
    exit 1
fi

if ! check_port 5173; then
    echo "❌ Puerto 5173 (frontend) no está disponible"
    exit 1
fi

echo "✅ Puertos disponibles"

# Iniciar backend
echo "🐍 Iniciando backend (FastAPI)..."
cd sanAgustinBackend

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias si no están instaladas
if [ ! -f "venv/lib/python*/site-packages/fastapi" ]; then
    echo "📥 Instalando dependencias del backend..."
    pip install -r requirements.txt
fi

# Iniciar backend en background
echo "🚀 Iniciando servidor backend en http://localhost:8000"
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Volver al directorio raíz
cd ..

# Iniciar frontend
echo "⚛️  Iniciando frontend (React)..."
cd san-agustin-frontend

# Instalar dependencias si no están instaladas
if [ ! -d "node_modules" ]; then
    echo "📥 Instalando dependencias del frontend..."
    npm install
fi

# Limpiar dependencias de Tailwind que ya no son necesarias
echo "🧹 Limpiando dependencias innecesarias..."
npm uninstall tailwindcss postcss autoprefixer --save-dev 2>/dev/null || true

# Iniciar frontend en background
echo "🚀 Iniciando servidor frontend en http://localhost:5173"
npm run dev &
FRONTEND_PID=$!

# Volver al directorio raíz
cd ..

echo ""
echo "🎉 ¡Entorno de desarrollo iniciado!"
echo ""
echo "📱 Frontend: http://localhost:5173"
echo "🔧 Backend:  http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Presiona Ctrl+C para detener ambos servicios"

# Función para limpiar procesos al salir
cleanup() {
    echo ""
    echo "🛑 Deteniendo servicios..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Servicios detenidos"
    exit 0
}

# Capturar señal de interrupción
trap cleanup SIGINT

# Mantener el script ejecutándose
wait
