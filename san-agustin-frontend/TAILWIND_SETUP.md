# Configuración de Tailwind CSS v4

Este proyecto utiliza **Tailwind CSS v4** a través del CDN oficial, lo que simplifica significativamente la configuración y el mantenimiento.

## Configuración Actual

### 1. CDN en HTML
```html
<!-- En index.html -->
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
```

### 2. Archivo de Estilos Personalizados
```css
/* En src/tailwind.css */
/* Clases personalizadas para San Agustín */
.btn-primary {
  background-color: rgb(37 99 235);
  color: white;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  transition: background-color 0.2s;
}

.btn-primary:hover {
  background-color: rgb(29 78 216);
}

.btn-secondary {
  background-color: rgb(229 231 235);
  color: rgb(31 41 55);
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  transition: background-color 0.2s;
}

.btn-secondary:hover {
  background-color: rgb(209 213 219);
}

.card {
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  padding: 1.5rem;
  border: 1px solid rgb(229 231 235);
}

.input-field {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid rgb(209 213 219);
  border-radius: 0.375rem;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.input-field:focus {
  border-color: transparent;
  box-shadow: 0 0 0 2px rgb(59 130 246);
}

/* Configuración de fuente */
html {
  font-family: 'Inter', system-ui, sans-serif;
}
```

## Ventajas de usar Tailwind CSS v4 CDN

### ✅ **Simplicidad**
- No requiere configuración de PostCSS
- No necesita archivos de configuración
- Instalación automática en el navegador

### ✅ **Rendimiento**
- Carga optimizada desde CDN
- Cache del navegador
- Solo carga las clases utilizadas

### ✅ **Mantenimiento**
- Actualizaciones automáticas
- Sin dependencias locales
- Menos archivos de configuración

### ✅ **Desarrollo**
- Hot reload automático
- Sintaxis simplificada
- Mejor integración con Vite

## Clases Personalizadas Disponibles

### Botones
- `.btn-primary` - Botón principal azul
- `.btn-secondary` - Botón secundario gris

### Contenedores
- `.card` - Tarjeta con sombra y borde
- `.input-field` - Campo de entrada estilizado

## Uso en Componentes

```tsx
// Ejemplo de uso
<button className="btn-primary">
  Botón Principal
</button>

<div className="card">
  <input className="input-field" placeholder="Texto..." />
</div>

// También puedes usar clases de Tailwind directamente
<div className="bg-blue-500 text-white p-4 rounded-lg">
  Contenido con Tailwind
</div>
```

## Solución de Problemas

### Error: `[postcss] ENOENT: no such file or directory, open 'tailwindcss'`

**Causa**: Vite intenta procesar archivos CSS con PostCSS cuando no está configurado correctamente.

**Solución**: 
1. Eliminar archivos de configuración de Tailwind (`tailwind.config.js`, `postcss.config.js`)
2. Usar solo el CDN de Tailwind v4
3. Crear clases personalizadas con CSS puro (sin `@apply`)
4. Simplificar la configuración de Vite

### Archivos Eliminados
- `tailwind.config.js`
- `postcss.config.js`
- Dependencias: `tailwindcss`, `postcss`, `autoprefixer`

## Migración desde Tailwind CSS v3

### Cambios Principales
1. **CDN**: Uso del CDN oficial en lugar de instalación local
2. **Configuración**: Sin necesidad de archivos de configuración
3. **PostCSS**: No requiere configuración de PostCSS
4. **Clases personalizadas**: CSS puro en lugar de `@apply`

## Compatibilidad

- ✅ **Navegadores modernos**: Chrome, Firefox, Safari, Edge
- ✅ **React 18+**: Compatibilidad completa
- ✅ **TypeScript**: Soporte nativo
- ✅ **Vite**: Integración perfecta

## Recursos Adicionales

- [Documentación oficial de Tailwind CSS v4](https://tailwindcss.com/docs)
- [CDN de Tailwind CSS v4](https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4)
- [Guía de migración v3 a v4](https://tailwindcss.com/docs/upgrade-guide)
