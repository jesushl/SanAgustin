# San Agustín - Sistema de Gestión de Servicios

Sistema completo para la gestión de servicios en la privada San Agustín, incluyendo backend en FastAPI y frontend en React.

## Estructura del Proyecto

```
SanAgustin/
├── sanAgustinBackend/          # Backend en FastAPI
│   ├── main.py                 # Aplicación principal
│   ├── config.py               # Configuración
│   ├── requirements.txt        # Dependencias de Python
│   └── ...
└── san-agustin-frontend/       # Frontend en React + TypeScript
    ├── src/
    │   ├── components/         # Componentes React
    │   ├── pages/             # Páginas de la aplicación
    │   ├── services/          # Servicios de API
    │   ├── types/             # Tipos TypeScript
    │   └── config/            # Configuración
    ├── package.json           # Dependencias de Node.js
    └── ...
```

## Características

### Backend (FastAPI)
- ✅ Gestión de estacionamientos
- ✅ Sistema de reservas de áreas comunes
- ✅ Registro de visitas
- ✅ Gestión de contactos
- ✅ Sistema de adeudos
- ✅ Generación de códigos QR
- ✅ Base de datos SQLite
- ✅ API REST completa

### Frontend (React + TypeScript + Tailwind CSS v4 CDN)
- ✅ Diseño responsivo
- ✅ Navegación moderna
- ✅ Dashboard interactivo
- ✅ Gestión de estacionamientos
- ✅ Formularios de reserva
- ✅ Interfaz intuitiva
- ✅ Tailwind CSS v4 via CDN (configuración simplificada)
- ✅ Clases personalizadas con CSS puro

## Instalación y Configuración

### Backend

1. **Navegar al directorio del backend:**
   ```bash
   cd sanAgustinBackend
   ```

2. **Crear entorno virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno:**
   Crear un archivo `.env` en `sanAgustinBackend/` con:
   ```env
   DATABASE_URL=sqlite:///./comunidad.db
   HOST=0.0.0.0
   PORT=8000
   DEBUG=True
   SECRET_KEY=tu_clave_secreta_aqui
   ```

5. **Ejecutar el servidor:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

### Frontend

1. **Navegar al directorio del frontend:**
   ```bash
   cd san-agustin-frontend
   ```

2. **Instalar dependencias:**
   ```bash
   npm install
   ```

3. **Configurar variables de entorno:**
   Crear un archivo `.env.local` en `san-agustin-frontend/` con:
   ```env
   VITE_API_BASE_URL=http://localhost:8000
   VITE_APP_NAME=San Agustín - Gestión de Servicios
   VITE_APP_VERSION=1.0.0
   ```

4. **Ejecutar el servidor de desarrollo:**
   ```bash
   npm run dev
   ```

## Uso

1. **Iniciar el backend** en `http://localhost:8000`
2. **Iniciar el frontend** en `http://localhost:5173`
3. **Acceder a la aplicación** en el navegador

## API Endpoints

### Estacionamientos
- `GET /estacionamientos/{numero}` - Obtener estacionamiento por número
- `GET /placas/{placa}` - Validar placa
- `POST /reservas_visitas/` - Registrar visita

### Áreas Comunes
- `GET /reservas_area_comun/` - Obtener todas las reservas
- `POST /reservas_area_comun/` - Crear nueva reserva

### Contactos
- `GET /contactos_residente/` - Obtener todos los contactos
- `POST /contactos_residente/` - Crear nuevo contacto

### Adeudos
- `GET /adeudos/` - Obtener todos los adeudos
- `GET /adeudos/{departamento_id}` - Obtener adeudos por departamento
- `POST /adeudos/` - Crear nuevo adeudo

## Tecnologías Utilizadas

### Backend
- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para base de datos
- **Pydantic** - Validación de datos
- **SQLite** - Base de datos ligera
- **Uvicorn** - Servidor ASGI

### Frontend
- **React 18** - Biblioteca de interfaz de usuario
- **TypeScript** - Tipado estático
- **Tailwind CSS v4** - Framework de CSS utilitario (via CDN)
- **React Router** - Enrutamiento
- **Axios** - Cliente HTTP
- **Lucide React** - Iconos
- **Vite** - Herramienta de construcción

## Desarrollo

### Estructura de Componentes

```
src/
├── components/
│   └── Navbar.tsx              # Navegación principal
├── pages/
│   ├── Home.tsx                # Dashboard principal
│   └── Estacionamientos.tsx    # Gestión de estacionamientos
├── services/
│   └── api.ts                  # Servicios de API
├── types/
│   └── index.ts                # Tipos TypeScript
└── config/
    └── api.ts                  # Configuración de API
```

### Estilos

El proyecto utiliza Tailwind CSS con clases personalizadas:
- `.btn-primary` - Botón primario
- `.btn-secondary` - Botón secundario
- `.card` - Contenedor de tarjeta
- `.input-field` - Campo de entrada

## Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Contacto

Para preguntas o soporte, contactar al equipo de desarrollo.
