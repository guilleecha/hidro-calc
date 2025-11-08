# 🔌 Configuración de MCP Servers para HidroCalc

**Fecha:** 2025-11-08
**Estado:** ✅ Instalado

---

## 📋 MCP Servers Instalados

Se han configurado **5 MCP servers** para mejorar las capacidades de desarrollo:

### 1. **Playwright** (`@playwright/mcp`)
**Propósito:** Automatización de navegador y testing E2E

**Capacidades:**
- Ejecutar tests de navegador automatizados
- Scraping de páginas web
- Tomar screenshots
- Interactuar con elementos del DOM
- Testing de flujos de usuario

**Uso en HidroCalc:**
- Testing automatizado de calculadoras
- Testing del flujo completo de análisis hidrológico
- Validación de exportación de reportes PDF
- Testing de gráficos interactivos

---

### 2. **Filesystem** (`@modelcontextprotocol/server-filesystem`)
**Propósito:** Acceso avanzado al sistema de archivos

**Capacidades:**
- Leer/escribir archivos con permisos avanzados
- Búsqueda recursiva de archivos
- Operaciones batch en múltiples archivos
- Gestión de directorios

**Configuración:**
- Path raíz: `C:\myprojects\hidro-calc`
- Solo tiene acceso a este directorio y subdirectorios

**Uso en HidroCalc:**
- Gestión de templates de reportes
- Procesamiento de archivos de datos hidrológicos
- Gestión de exports (PDF, Excel)

---

### 3. **GitHub** (`@modelcontextprotocol/server-github`)
**Propósito:** Integración con GitHub

**Capacidades:**
- Crear/leer issues
- Gestionar pull requests
- Acceder a código de repositorios
- Ver historial de commits
- Gestionar branches

**⚠️ Requiere configuración:**
```json
"GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_tu_token_aqui"
```

**Cómo obtener el token:**
1. https://github.com/settings/tokens
2. "Generate new token (classic)"
3. Permisos: `repo`, `read:org`, `read:user`

**Uso en HidroCalc:**
- Gestión de issues y bugs
- Code reviews
- Deployment automation
- Documentación colaborativa

---

### 4. **PostgreSQL** (`@modelcontextprotocol/server-postgres`)
**Propósito:** Interacción directa con bases de datos PostgreSQL

**Capacidades:**
- Ejecutar queries SQL
- Análisis de esquema de BD
- Optimización de queries
- Gestión de migraciones

**Configuración actual:**
```
postgresql://localhost/hidrocal
```

**⚠️ Nota:** Actualmente usamos SQLite. PostgreSQL es para producción.

**Uso futuro en HidroCalc:**
- Migración a PostgreSQL en producción
- Análisis de performance de queries
- Gestión de datos de múltiples proyectos
- Backups y restore

---

### 5. **Context7** (`@upstash/context7-mcp`)
**Propósito:** Documentación contextual de librerías y APIs

**Capacidades:**
- Acceso a documentación actualizada de librerías
- Ejemplos de código contextuales
- Mejores prácticas de frameworks
- API references en tiempo real

**⚠️ Requiere configuración:**
```json
"CONTEXT7_API_KEY": "ctx7_tu_key_aqui"
```

**Cómo obtener la key:**
1. https://context7.com o https://upstash.com
2. Crear cuenta
3. Generar API key

**Uso en HidroCalc:**
- Documentación de Django
- Documentación de Django Rest Framework
- Referencia de Plotly.js
- Guías de NumPy/SciPy
- Best practices de Python

---

## 📁 Ubicación del Archivo de Configuración

**Windows:**
```
C:\Users\guill\AppData\Roaming\Claude\claude_desktop_config.json
```

**Contenido actual:**
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest"],
      "env": {}
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:\\myprojects\\hidro-calc"],
      "env": {}
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": ""
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/hidrocal"],
      "env": {}
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"],
      "env": {
        "CONTEXT7_API_KEY": ""
      }
    }
  }
}
```

---

## 🚀 Pasos para Activar

### 1. Instalar dependencias (✅ YA HECHO)
```bash
npm install -g @playwright/mcp @modelcontextprotocol/server-filesystem @modelcontextprotocol/server-github @modelcontextprotocol/server-postgres @upstash/context7-mcp
```

### 2. Obtener API Keys

#### GitHub Token
1. Ve a: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Nombre: "Claude MCP"
4. Permisos:
   - ✅ `repo` (Full control)
   - ✅ `read:org` (Read org)
   - ✅ `read:user` (Read user)
5. Click "Generate token"
6. Copia el token (empieza con `ghp_`)

#### Context7 API Key
1. Ve a: https://context7.com
2. Regístrate o inicia sesión
3. Ve a "API Keys" o "Settings"
4. Crea una nueva API key
5. Copia la key (empieza con `ctx7_`)

### 3. Actualizar Configuración

Edita el archivo:
```
C:\Users\guill\AppData\Roaming\Claude\claude_desktop_config.json
```

Reemplaza:
```json
"GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_tu_token_real_aqui"
"CONTEXT7_API_KEY": "ctx7_tu_key_real_aqui"
```

### 4. Reiniciar Claude Desktop

Cierra y vuelve a abrir Claude Desktop para que tome los cambios.

### 5. Verificar Instalación

Los MCP servers deberían aparecer en la interfaz de Claude Desktop.
Verifica que puedas:
- ✅ Ejecutar comandos de Playwright
- ✅ Acceder a archivos del proyecto
- ✅ Ver documentación de Context7
- ✅ (Opcional) Interactuar con GitHub

---

## 🧪 Testing de MCP Servers

### Test Playwright
```javascript
// Pedir a Claude:
// "Usa Playwright para abrir localhost:8000 y tomar un screenshot"
```

### Test Filesystem
```
// Pedir a Claude:
// "Lista todos los archivos Python en el proyecto"
```

### Test Context7
```
// Pedir a Claude:
// "Dame ejemplos de uso de Django Rest Framework ViewSets"
```

### Test GitHub (requiere token)
```
// Pedir a Claude:
// "Muéstrame los últimos issues del repositorio"
```

---

## ⚠️ Troubleshooting

### MCP no aparece en Claude Desktop
- Verifica que el archivo de configuración esté en la ubicación correcta
- Reinicia Claude Desktop completamente
- Verifica que Node.js esté instalado: `node --version`

### "Command not found" al ejecutar MCP
- Instala las dependencias globalmente:
  ```bash
  npm install -g [paquete-mcp]
  ```

### GitHub MCP no funciona
- Verifica que el token tenga los permisos correctos
- El token debe estar activo (no expirado)
- Formato correcto en JSON (con comillas)

### Context7 retorna error
- Verifica que la API key sea válida
- Puede tener límites de uso en plan free
- Contacta soporte si es necesario

---

## 📚 Referencias

- **MCP Protocol:** https://modelcontextprotocol.io
- **Playwright:** https://playwright.dev
- **Context7:** https://context7.com
- **Django Docs:** https://docs.djangoproject.com
- **DRF Docs:** https://www.django-rest-framework.org

---

## 🎯 Próximos Pasos con MCP

1. **Testing automatizado con Playwright**
   - Crear suite de tests E2E
   - Testing de calculadoras
   - Validación de flujos

2. **Optimización de código con Context7**
   - Consultar best practices de Django
   - Optimizar queries de DRF
   - Mejorar estructura de código

3. **Integración con GitHub**
   - Automatizar issues de bugs encontrados
   - Gestión de pull requests
   - Code reviews automatizados

4. **Preparar migración a PostgreSQL**
   - Testing de queries
   - Optimización de índices
   - Plan de migración

---

**Instalación completada:** ✅
**Configuración pendiente:** GitHub Token, Context7 API Key
**Estado:** Listo para usar (excepto GitHub y Context7 que requieren keys)
