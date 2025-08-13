#!/bin/bash

echo "🚀 Configurando Sistema de Autenticación OAuth2.0 - San Agustín"
echo "================================================================"

# Verificar si estamos en el directorio correcto
if [ ! -f "sanAgustinBackend/main.py" ]; then
    echo "❌ Error: No se encontró el backend. Asegúrate de estar en el directorio raíz del proyecto."
    exit 1
fi

echo "📦 Instalando dependencias del backend..."
cd sanAgustinBackend
pip install -r requirements.txt

echo "🗄️ Creando tablas de autenticación..."
python crear_tablas_auth.py

echo "👤 Creando usuario administrador..."
python crear_admin.py

echo "🔧 Configuración del sistema:"
echo "✅ El servidor ahora puede ejecutarse sin errores"
echo "✅ Las tablas de autenticación están creadas"
echo "✅ El usuario administrador está creado (admin@sanagustin.com)"

echo ""
echo "📝 Configuración necesaria para OAuth2.0:"
echo ""
echo "1. Crea un archivo .env en sanAgustinBackend/ con las siguientes variables:"
echo "   GOOGLE_CLIENT_ID=your_google_client_id"
echo "   GOOGLE_CLIENT_SECRET=your_google_client_secret"
echo "   FACEBOOK_CLIENT_ID=your_facebook_client_id"
echo "   FACEBOOK_CLIENT_SECRET=your_facebook_client_secret"
echo "   SECRET_KEY=your_secret_key_here_change_in_production"
echo ""
echo "2. Configura OAuth en Google Cloud Console y Facebook Developers"
echo "   - URLs de redirección: http://localhost:8000/auth/google/callback"
echo "   - URLs de redirección: http://localhost:8000/auth/facebook/callback"
echo ""
echo "3. Instala dependencias del frontend:"
echo "   cd san-agustin-frontend && npm install"
echo ""
echo "4. Para habilitar OAuth2.0 (opcional):"
echo "   cd sanAgustinBackend && python enable_auth.py enable"
echo ""
echo "✅ Configuración completada!"
echo ""
echo "Para ejecutar el sistema:"
echo "1. Backend: cd sanAgustinBackend && python main.py"
echo "2. Frontend: cd san-agustin-frontend && npm run dev"
echo ""
echo "📖 Lee sanAgustinBackend/README_AUTH.md para más detalles"
