# Sistema de Autenticación OAuth2.0 - San Agustín

## Configuración

### 1. Variables de Entorno

Crea un archivo `.env` en el directorio `sanAgustinBackend/` con las siguientes variables:

```env
# OAuth Configuration
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
FACEBOOK_CLIENT_ID=your_facebook_client_id
FACEBOOK_CLIENT_SECRET=your_facebook_client_secret

# JWT Configuration
SECRET_KEY=your_secret_key_here_change_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL=sqlite:///./comunidad.db

# Frontend URL
FRONTEND_URL=http://localhost:5173
```

### 2. Configurar Google OAuth

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita la API de Google+ 
4. Ve a "Credentials" y crea un "OAuth 2.0 Client ID"
5. Configura las URLs de redirección:
   - `http://localhost:8000/auth/google/callback`
6. Copia el Client ID y Client Secret a tu archivo `.env`

### 3. Configurar Facebook OAuth

1. Ve a [Facebook Developers](https://developers.facebook.com/)
2. Crea una nueva aplicación
3. Agrega el producto "Facebook Login"
4. Configura las URLs de redirección:
   - `http://localhost:8000/auth/facebook/callback`
5. Copia el App ID y App Secret a tu archivo `.env`

### 4. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 5. Crear Tablas de Base de Datos

```bash
python crear_tablas_auth.py
```

### 6. Crear Usuario Administrador

```bash
python crear_admin.py
```

## Flujo de Autenticación

### 1. Login con OAuth
- El usuario hace clic en "Login con Google" o "Login con Facebook"
- Se redirige al proveedor OAuth
- Después de la autenticación, se redirige de vuelta a la aplicación

### 2. Verificación de Usuario
- Si el usuario ya existe en la base de datos → Se genera un token JWT y se redirige al dashboard
- Si el usuario no existe → Se redirige al formulario de registro

### 3. Registro de Usuario Nuevo
- El usuario completa el formulario con datos adicionales (teléfono, dirección, departamento)
- Se crea un registro pendiente en la tabla `registros_pendientes`
- El usuario espera la aprobación del administrador

### 4. Aprobación por Administrador
- El administrador ve la lista de registros pendientes
- Aprueba o rechaza cada registro
- Al aprobar, se crea automáticamente el usuario y su contacto

## Endpoints de la API

### Autenticación
- `GET /auth/google/login` - Inicia login con Google
- `GET /auth/google/callback` - Callback de Google OAuth
- `GET /auth/facebook/login` - Inicia login con Facebook
- `GET /auth/facebook/callback` - Callback de Facebook OAuth
- `POST /auth/register` - Registra usuario pendiente
- `GET /auth/me` - Obtiene información del usuario actual

### Administración (solo admin)
- `GET /auth/pending-registrations` - Lista registros pendientes
- `POST /auth/approve-registration/{reg_id}` - Aprueba un registro

## Estructura de Base de Datos

### Tabla: usuarios
- `id` - ID único del usuario
- `email` - Email del usuario (único)
- `nombre` - Nombre del usuario
- `apellido` - Apellido del usuario
- `provider` - Proveedor OAuth ('google', 'facebook', 'manual')
- `provider_id` - ID del usuario en el proveedor
- `is_active` - Si el usuario está activo
- `is_admin` - Si el usuario es administrador
- `created_at` - Fecha de creación
- `updated_at` - Fecha de última actualización

### Tabla: registros_pendientes
- `id` - ID único del registro
- `email` - Email del usuario
- `nombre` - Nombre del usuario
- `apellido` - Apellido del usuario
- `provider` - Proveedor OAuth
- `provider_id` - ID del usuario en el proveedor
- `telefono` - Teléfono del usuario
- `direccion` - Dirección del usuario
- `departamento` - Departamento del usuario
- `notas_adicionales` - Notas adicionales
- `is_approved` - Si el registro fue aprobado
- `approved_by` - ID del administrador que aprobó
- `approved_at` - Fecha de aprobación
- `created_at` - Fecha de creación

### Tabla: contactos
- `id` - ID único del contacto
- `usuario_id` - ID del usuario (relación 1:1)
- `telefono` - Teléfono del contacto
- `direccion` - Dirección del contacto
- `departamento` - Departamento del contacto
- `created_at` - Fecha de creación
- `updated_at` - Fecha de última actualización

## Seguridad

- Los tokens JWT tienen una duración de 30 minutos por defecto
- Las rutas de administración requieren permisos de admin
- Los datos sensibles se almacenan en variables de entorno
- Las contraseñas no se almacenan (se usa OAuth)

## Notas Importantes

1. **Cambiar SECRET_KEY**: En producción, cambia la SECRET_KEY por una clave segura
2. **HTTPS**: En producción, usa HTTPS para las URLs de redirección
3. **Dominios**: Actualiza las URLs de redirección con tu dominio de producción
4. **Backup**: Haz backup regular de la base de datos
5. **Logs**: Implementa logging para auditoría de accesos
