#!/bin/bash

# Script para iniciar el entorno de desarrollo de San Agustín
# Sistema de Gestión de Residencias

echo "🏠 San Agustín - Sistema de Gestión de Residencias"
echo "=================================================="
echo ""

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no está instalado"
    exit 1
fi

# Verificar si Node.js está instalado
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js no está instalado"
    exit 1
fi

# Verificar si npm está instalado
if ! command -v npm &> /dev/null; then
    echo "❌ Error: npm no está instalado"
    exit 1
fi

echo "✅ Prerrequisitos verificados"
echo ""

# Función para manejar la interrupción
cleanup() {
    echo ""
    echo "🛑 Deteniendo servidores..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Capturar interrupción
trap cleanup SIGINT

# Backend
echo "🐍 Configurando Backend..."
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
    echo "📥 Instalando dependencias de Python..."
    pip install -r requirements.txt
fi

# Verificar si la base de datos existe
if [ ! -f "comunidad.db" ]; then
    echo "🗄️ Creando base de datos..."
    python poblar_simple.py
    python asociar_usuario.py
fi

echo "🚀 Iniciando servidor backend..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Esperar un momento para que el backend se inicie
sleep 3

# Frontend
echo ""
echo "⚛️ Configurando Frontend..."
cd ../san-agustin-frontend

# Instalar dependencias si no están instaladas
if [ ! -d "node_modules" ]; then
    echo "📥 Instalando dependencias de Node.js..."
    npm install
fi

echo "🚀 Iniciando servidor frontend..."
npm run dev &
FRONTEND_PID=$!

echo ""
echo "🎉 ¡Servidores iniciados exitosamente!"
echo ""
echo "📱 Frontend: http://localhost:5173"
echo "🔧 Backend:  http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "👤 Usuarios de prueba:"
echo "   - Residente: residente@test.com"
echo "   - Admin: admin@test.com"
echo ""
echo "💡 Presiona Ctrl+C para detener los servidores"
echo ""

# Esperar a que se presione Ctrl+C
wait
