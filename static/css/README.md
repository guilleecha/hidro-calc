# 🎨 HidroCalc CSS Architecture

**Estructura CSS modular inspirada en HydroML y metodologías modernas**

---

## 📁 Estructura de Carpetas

```
static/css/
├── base/                  # Fundamentos y reset
│   ├── variables.css     # Variables CSS (colores, spacing, tipografía)
│   └── reset.css         # Reset y estilos base
│
├── layouts/              # Layouts y estructura de página
│   ├── container.css     # Containers y secciones
│   ├── grid.css          # Sistemas de grillas
│   └── header-footer.css # Header, footer, nav, breadcrumb
│
├── components/           # Componentes reutilizables
│   ├── buttons.css       # .btn, .btn-primary, .btn-secondary
│   ├── cards.css         # .card, .card-header, .card-content
│   ├── forms.css         # .form-input, .form-label, .form-error
│   ├── badges.css        # .badge, .badge-success, .badge-warning
│   └── results.css       # Componentes de resultados de cálculos
│
├── utilities/            # Utilidades y helpers
│   ├── spacing.css       # Margin, padding, gap utilities
│   └── helpers.css       # Display, flex, text, color utilities
│
├── main.css              # ⭐ Archivo principal (importa todo)
├── style.css             # ⚠️ LEGACY - mantener por compatibilidad
└── forms.css             # ⚠️ LEGACY - mantener por compatibilidad
```

---

## 🚀 Uso

### **Opción 1: Usar el nuevo sistema modular** ✅ RECOMENDADO

```html
<!-- En templates Django -->
{% load static %}
<link rel="stylesheet" href="{% static 'css/main.css' %}">
```

### **Opción 2: Importar componentes específicos**

Si solo necesitas ciertos componentes:

```html
<link rel="stylesheet" href="{% static 'css/base/variables.css' %}">
<link rel="stylesheet" href="{% static 'css/base/reset.css' %}">
<link rel="stylesheet" href="{% static 'css/components/buttons.css' %}">
<link rel="stylesheet" href="{% static 'css/components/cards.css' %}">
```

### **Opción 3: Sistema legacy** ⚠️

Para compatibilidad con templates existentes:

```html
<link rel="stylesheet" href="{% static 'css/style.css' %}">
<link rel="stylesheet" href="{% static 'css/forms.css' %}">
```

---

## 📦 Componentes Disponibles

### **BASE**

#### `variables.css`
Define el design system completo:

- **Colores:** `--color-primary`, `--color-success`, `--color-warning`, etc.
- **Spacing:** `--spacing-xs`, `--spacing-sm`, `--spacing-md`, `--spacing-lg`, etc.
- **Tipografía:** `--font-sans`, `--font-mono`, `--font-xs` a `--font-5xl`
- **Bordes:** `--radius-sm`, `--radius-md`, `--radius-lg`
- **Sombras:** `--shadow-sm`, `--shadow-md`, `--shadow-lg`
- **Transiciones:** `--transition-fast`, `--transition-base`, `--transition-slow`

**Ejemplo:**
```css
.my-element {
    color: var(--color-primary);
    padding: var(--spacing-md);
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-md);
}
```

#### `reset.css`
Reset CSS moderno + estilos base de HTML, tipografía y links.

---

### **LAYOUTS**

#### `container.css`
Contenedores y secciones de página.

**Clases:**
- `.container` - Container centrado (max-width: 1200px)
- `.container-sm`, `.container-md`, `.container-lg`, `.container-xl`
- `.section` - Sección con padding vertical
- `.page-header` - Header de página con título centrado
- `.content-layout` - Layout 2 columnas (formulario + resultados)

**Ejemplo:**
```html
<div class="container">
    <div class="page-header">
        <h1>Mi Calculadora</h1>
        <p class="page-description">Descripción</p>
    </div>

    <div class="content-layout">
        <div class="form-section">...</div>
        <div class="results-section">...</div>
    </div>
</div>
```

#### `grid.css`
Sistema de grillas flexible.

**Clases:**
- `.grid` - Grid base
- `.grid-cols-1`, `.grid-cols-2`, `.grid-cols-3`, `.grid-cols-4`
- `.grid-auto-fit` - Grid responsive automático
- `.modules-grid` - Grid especial para módulos de home
- `.gap-xs`, `.gap-sm`, `.gap-md`, `.gap-lg`

**Ejemplo:**
```html
<div class="grid grid-cols-3 gap-lg">
    <div>Item 1</div>
    <div>Item 2</div>
    <div>Item 3</div>
</div>
```

#### `header-footer.css`
Header, footer, navegación, breadcrumb.

**Clases:**
- `.header`, `.header-content`
- `.logo`, `.nav`, `.nav-link`
- `.breadcrumb`
- `.footer`, `.footer-content`
- `.hero`, `.hero-title`, `.hero-subtitle`

---

### **COMPONENTS**

#### `buttons.css`
Sistema completo de botones.

**Variantes:**
- `.btn-primary` - Botón principal (azul)
- `.btn-secondary` - Botón secundario (gris)
- `.btn-outline` - Botón con borde
- `.btn-success`, `.btn-warning`, `.btn-error`
- `.btn-ghost`, `.btn-link`

**Tamaños:**
- `.btn-sm`, `.btn-lg`, `.btn-xl`

**Modificadores:**
- `.btn-block` - Ancho completo
- `.loading` - Estado de carga
- `:disabled` - Deshabilitado

**Ejemplo:**
```html
<button class="btn btn-primary">Calcular</button>
<button class="btn btn-secondary btn-sm">Limpiar</button>
<button class="btn btn-outline btn-lg btn-block">Exportar</button>
```

#### `cards.css`
Tarjetas y paneles.

**Variantes:**
- `.card` - Card base
- `.card-primary`, `.card-success`, `.card-warning`, `.card-error`, `.card-info` - Con borde coloreado
- `.card-primary-light`, `.card-success-light`, etc. - Con fondo coloreado
- `.card-interactive` - Con efecto hover
- `.card-empty` - Empty state

**Partes:**
- `.card-header`, `.card-content`, `.card-footer`

**Ejemplo:**
```html
<div class="card card-primary">
    <div class="card-header">
        <h2>Resultados</h2>
    </div>
    <div class="card-content">
        Contenido...
    </div>
</div>
```

#### `forms.css`
Formularios completos.

**Clases:**
- `.form-group` - Grupo de campo
- `.form-label` - Etiqueta
- `.form-input`, `.form-select`, `.form-textarea` - Inputs
- `.input-group`, `.input-unit` - Input con unidad
- `.form-help` - Texto de ayuda
- `.form-error`, `.form-error.active` - Mensajes de error
- `.form-actions` - Contenedor de botones

**Estados:**
- `.error`, `.success` - Estados de validación

**Ejemplo:**
```html
<form>
    <div class="form-group">
        <label class="form-label">Área (A)</label>
        <div class="input-group">
            <input type="number" class="form-input" />
            <span class="input-unit">ha</span>
        </div>
        <small class="form-help">Área de la cuenca</small>
        <div class="form-error" id="error-A"></div>
    </div>

    <div class="form-actions">
        <button type="submit" class="btn btn-primary">Calcular</button>
        <button type="reset" class="btn btn-secondary">Limpiar</button>
    </div>
</form>
```

#### `badges.css`
Badges y etiquetas.

**Variantes:**
- `.badge-primary`, `.badge-success`, `.badge-warning`, `.badge-error`
- `.badge-primary-light`, `.badge-success-light`, etc.
- `.badge-outline-primary`, etc.

**Especiales:**
- `.badge-available`, `.badge-upcoming`, `.badge-dev`, `.badge-beta`

**Ejemplo:**
```html
<span class="badge badge-success">Disponible</span>
<span class="badge badge-upcoming">Próximamente</span>
```

#### `results.css`
Componentes para mostrar resultados de cálculos.

**Clases:**
- `.results-grid` - Grid de resultados
- `.result-item` - Item de resultado
- `.result-item.highlight` - Resultado principal destacado
- `.result-value`, `.result-unit` - Valor y unidad
- `.factors-section`, `.parameters-section` - Secciones
- `.warnings` - Advertencias
- `.formula-box`, `.formula` - Caja de fórmula
- `.empty-state` - Estado vacío

**Ejemplo:**
```html
<div class="results-grid">
    <div class="result-item highlight">
        <label>Caudal (Q)</label>
        <div class="result-value">
            <span>722.28</span>
            <span class="result-unit">L/s</span>
        </div>
    </div>

    <div class="result-item">
        <label>Área</label>
        <div class="result-value">
            <span>5.0</span>
            <span class="result-unit">ha</span>
        </div>
    </div>
</div>

<div class="warnings">
    <h3>⚠️ Advertencias</h3>
    <ul>
        <li>Intensidad muy alta (>500 mm/h)</li>
    </ul>
</div>
```

---

### **UTILITIES**

#### `spacing.css`
Utilidades de espaciado (margin, padding, gap).

**Patrón:**
- `m{side}-{size}` - Margin
- `p{side}-{size}` - Padding
- `gap-{size}` - Gap

**Sides:** `t` (top), `r` (right), `b` (bottom), `l` (left), `x` (horizontal), `y` (vertical), o ninguno (all)

**Sizes:** `0`, `xs`, `sm`, `md`, `lg`, `xl`, `2xl`, `3xl`

**Ejemplos:**
```html
<div class="mt-lg mb-xl">Margin top large, bottom extra-large</div>
<div class="px-md py-sm">Padding horizontal medium, vertical small</div>
<div class="m-0">Sin margin</div>
```

#### `helpers.css`
Utilidades generales.

**Display:**
- `.block`, `.inline-block`, `.flex`, `.grid`, `.hidden`

**Flex:**
- `.flex-row`, `.flex-col`, `.flex-wrap`
- `.justify-center`, `.justify-between`, `.items-center`

**Text:**
- `.text-left`, `.text-center`, `.text-right`
- `.text-xs`, `.text-sm`, `.text-base`, `.text-lg`, `.text-xl`, `.text-2xl`, etc.
- `.text-primary`, `.text-success`, `.text-gray-600`, etc.
- `.font-normal`, `.font-medium`, `.font-semibold`, `.font-bold`

**Background:**
- `.bg-white`, `.bg-primary`, `.bg-gray-100`, etc.

**Otros:**
- `.rounded-sm`, `.rounded-md`, `.rounded-lg`, `.rounded-full`
- `.shadow-sm`, `.shadow-md`, `.shadow-lg`
- `.opacity-50`, `.opacity-75`, `.opacity-100`
- `.cursor-pointer`, `.cursor-not-allowed`

**Ejemplos:**
```html
<div class="flex items-center gap-md">
    <span class="text-lg font-bold text-primary">Título</span>
    <span class="badge badge-success">Nuevo</span>
</div>

<div class="bg-gray-100 rounded-lg shadow-md p-lg">
    <p class="text-center text-gray-600">Contenido</p>
</div>
```

---

## 🎯 Ejemplos de Uso Completo

### **Ejemplo 1: Página de Calculadora**

```html
{% load static %}
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="{% static 'css/main.css' %}">
</head>
<body>
    <div class="container">
        <div class="page-header">
            <h1>📊 Método Racional</h1>
            <p class="page-description">
                Cálculo de caudales de diseño
            </p>
        </div>

        <div class="content-layout">
            <!-- Formulario -->
            <div class="form-section">
                <div class="card">
                    <h2>Datos de Entrada</h2>
                    <form id="rationalForm">
                        <div class="form-group">
                            <label class="form-label">
                                Coeficiente de Escorrentía (C)
                            </label>
                            <input type="number" class="form-input"
                                   id="C" step="0.01" value="0.65">
                            <small class="form-help">
                                Entre 0 y 1
                            </small>
                            <div class="form-error" id="error-C"></div>
                        </div>

                        <div class="form-actions">
                            <button type="submit" class="btn btn-primary">
                                🧮 Calcular
                            </button>
                            <button type="reset" class="btn btn-secondary">
                                🔄 Limpiar
                            </button>
                        </div>
                    </form>
                </div>
            </div>

            <!-- Resultados -->
            <div class="results-section">
                <div class="card" id="resultsCard">
                    <h2>Resultados</h2>

                    <div class="results-grid">
                        <div class="result-item highlight">
                            <label>Caudal (Q)</label>
                            <div class="result-value">
                                <span id="result-Q">722.28</span>
                                <span class="result-unit">L/s</span>
                            </div>
                        </div>
                    </div>

                    <div class="warnings" style="display: none;">
                        <h3>⚠️ Advertencias</h3>
                        <ul id="warningsList"></ul>
                    </div>

                    <div class="formula-box">
                        <h3>Fórmula Utilizada</h3>
                        <div class="formula">
                            Q = C × I × A × 2.778
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
```

### **Ejemplo 2: Home Page con Grid de Módulos**

```html
<div class="container">
    <div class="hero">
        <h1 class="hero-title">🌊 HidroCalc</h1>
        <p class="hero-subtitle">
            Plataforma de cálculos hidrológicos
        </p>
    </div>

    <div class="modules-grid">
        <div class="module-card card-interactive">
            <div class="module-icon">📊</div>
            <h2>Método Racional</h2>
            <p>Cálculo de caudales de diseño</p>
            <div class="module-formula">Q = C × I × A</div>
            <span class="badge badge-available badge-top-right">
                Disponible
            </span>
        </div>

        <div class="module-card card-interactive upcoming">
            <div class="module-icon">⏱️</div>
            <h2>Tiempo de Concentración</h2>
            <p>Múltiples métodos de cálculo</p>
            <span class="badge badge-upcoming badge-top-right">
                Próximamente
            </span>
        </div>
    </div>
</div>
```

---

## 🔄 Migración desde CSS Legacy

Si tienes templates usando `style.css` y `forms.css`, puedes migrar gradualmente:

1. **Agregar `main.css` junto al legacy:**
   ```html
   <link rel="stylesheet" href="{% static 'css/style.css' %}">
   <link rel="stylesheet" href="{% static 'css/forms.css' %}">
   <link rel="stylesheet" href="{% static 'css/main.css' %}"> <!-- Nuevo -->
   ```

2. **Reemplazar clases progresivamente** en los templates

3. **Eventualmente eliminar** `style.css` y `forms.css` cuando todo esté migrado

---

## 🎨 Design System

### **Paleta de Colores**

| Color | Variable | Hex | Uso |
|-------|----------|-----|-----|
| 🔵 Primary | `--color-primary` | `#2563eb` | Acciones principales, links |
| ⚫ Secondary | `--color-secondary` | `#64748b` | Acciones secundarias |
| ✅ Success | `--color-success` | `#10b981` | Éxito, confirmación |
| ⚠️ Warning | `--color-warning` | `#f59e0b` | Advertencias |
| ❌ Error | `--color-error` | `#ef4444` | Errores, validación |
| ℹ️ Info | `--color-info` | `#06b6d4` | Información |

### **Escala de Spacing**

| Nombre | Variable | Valor | Píxeles |
|--------|----------|-------|---------|
| XS | `--spacing-xs` | 0.25rem | 4px |
| SM | `--spacing-sm` | 0.5rem | 8px |
| MD | `--spacing-md` | 1rem | 16px |
| LG | `--spacing-lg` | 1.5rem | 24px |
| XL | `--spacing-xl` | 2rem | 32px |
| 2XL | `--spacing-2xl` | 3rem | 48px |
| 3XL | `--spacing-3xl` | 4rem | 64px |

### **Tipografía**

- **Font Family:** System font stack (Segoe UI, Roboto, etc.)
- **Font Mono:** Courier New, Consolas, Monaco
- **Font Sizes:** xs (12px) → 5xl (48px)
- **Font Weights:** normal (400), medium (500), semibold (600), bold (700)

---

## 📝 Buenas Prácticas

1. **Usa variables CSS** en lugar de valores hardcodeados
2. **Combina utility classes** para estilos rápidos
3. **Crea componentes custom** solo cuando sea necesario
4. **Mantén la especificidad baja** - evita IDs y `!important`
5. **Usa clases semánticas** (`.result-item` en vez de `.blue-box`)
6. **Responsive by default** - todos los componentes son responsive

---

## 🚀 Performance

- **Modular:** Importa solo lo que necesites
- **CSS Variables:** Cambios de tema sin recompilar
- **Clases utility:** Evita CSS custom repetitivo
- **Sin JavaScript:** Puro CSS, sin dependencias

---

**Última actualización:** 2025-11-08
**Versión:** 1.0
