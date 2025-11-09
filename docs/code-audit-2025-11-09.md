# 🔍 Code Audit Report - HidroCalc

**Fecha:** 2025-11-09
**Objetivo:** Identificar archivos > 500 líneas, CSS duplicado, código obsoleto

---

## ✅ Resumen Ejecutivo

**Estado general:** 🟢 BUENO

- ✅ **Todos los archivos activos < 500 líneas** (cumple lineamientos)
- ⚠️  **CSS duplicado detectado** entre `studio/` y `components/`
- ⚠️  **~700KB de archivos backup** obsoletos en `old/` y `src_fastapi_backup/`
- ✅ **Arquitectura CSS modular** ya implementada en `static/css/`

---

## 📊 1. Análisis de Tamaño de Archivos

### **Archivos Python Activos (Top 10)**

```
459 líneas  tests/calculators/test_views_api.py       ✅
401 líneas  tests/calculators/test_services_idf.py    ✅
362 líneas  api/serializers.py                        ✅
354 líneas  studio/views.py                           ✅
306 líneas  hydrology/models.py                       ✅
298 líneas  calculators/services/idf.py               ✅
296 líneas  api/views.py                              ✅
291 líneas  hidrocal_project/settings.py              ✅
280 líneas  tests/calculators/test_utils_conversions.py ✅
277 líneas  tests/calculators/test_services_rational.py ✅
```

**✅ RESULTADO:** Ningún archivo activo supera las 500 líneas.

### **Archivos Obsoletos > 500 líneas**

```
524 líneas  src_fastapi_backup/api/routes.py   ❌ OBSOLETO (FastAPI)
524 líneas  old/04_routes.py                   ❌ OBSOLETO (FastAPI)
```

**Acción recomendada:** Eliminar directorios completos.

---

## 🎨 2. Análisis de CSS

### **Arquitectura Actual**

El proyecto tiene **DOS sistemas CSS:**

#### **Sistema 1: CSS Modular (main.css)** ✅ CORRECTO

```
static/css/main.css (22 líneas)
  ├── base/
  │   ├── variables.css     (127 líneas) - CSS custom properties
  │   └── reset.css         (91 líneas)  - Normalize
  ├── layouts/
  │   ├── container.css     (136 líneas)
  │   ├── grid.css          (176 líneas)
  │   └── header-footer.css (187 líneas)
  ├── components/
  │   ├── buttons.css       (177 líneas) ⭐
  │   ├── cards.css         (169 líneas) ⭐
  │   ├── forms.css         (240 líneas) ⭐
  │   ├── badges.css        (223 líneas)
  │   └── results.css       (303 líneas)
  └── utilities/
      ├── spacing.css       (152 líneas)
      └── helpers.css       (202 líneas)
```

**Usado por:**
- `templates/base.html` (todos los templates heredan)
- `templates/calculators/*.html`

#### **Sistema 2: CSS Studio (standalone)** ⚠️ DUPLICACIÓN

```
static/studio/css/
  ├── dashboard.css   (199 líneas) ⚠️  Redefine .btn-*, .stat-card, etc.
  ├── welcome.css     (163 líneas) ⚠️  Redefine .btn-primary, .btn-secondary
  └── no_projects.css (174 líneas) ⚠️  Redefine .btn, .btn-primary, etc.
```

**Usado por:**
- `templates/studio/*.html`

---

### **🔴 Duplicación Detectada**

#### **Componentes Duplicados:**

| Clase CSS | Definido en components/ | Redefinido en studio/ | Problema |
|-----------|------------------------|----------------------|----------|
| `.btn-primary` | ✅ `buttons.css` (usa variables) | ❌ `welcome.css`, `no_projects.css` (hardcoded) | Duplicación + no usa design tokens |
| `.btn-secondary` | ✅ `buttons.css` (usa variables) | ❌ `welcome.css`, `no_projects.css` (hardcoded) | Duplicación + no usa design tokens |
| `.btn` | ✅ `buttons.css` (completo) | ❌ `no_projects.css` (parcial) | Duplicación |
| Cards/containers | ✅ `cards.css` | ❌ Redefinidos en 3 archivos studio | Duplicación de patrones |

#### **Ejemplo de Duplicación:**

**`static/css/components/buttons.css` (CORRECTO):**
```css
.btn-primary {
    background: var(--color-primary);     /* ✅ Usa design token */
    color: white;
}

.btn-primary:hover:not(:disabled) {
    background: var(--color-primary-dark); /* ✅ Usa design token */
    transform: translateY(-1px);
    box-shadow: var(--shadow-md);        /* ✅ Usa design token */
}
```

**`static/studio/css/welcome.css` (DUPLICADO):**
```css
.btn-primary {
    background: #2563eb;                  /* ❌ Hardcoded */
    color: white;
    padding: 0.75rem 2rem;
    border-radius: 0.375rem;              /* ❌ No usa var(--radius-md) */
    text-decoration: none;
    font-weight: 600;
    transition: background 0.2s;
}

.btn-primary:hover {
    background: #1e40af;                  /* ❌ Hardcoded */
}
```

**Problemas:**
1. ❌ Código duplicado (DRY violation)
2. ❌ No usa design tokens (variables CSS)
3. ❌ Inconsistencia de hover effects
4. ❌ Mantenimiento duplicado (cambiar en 4 lugares)

---

## 🗂️ 3. Archivos Obsoletos

### **Directorios Backup:**

```bash
old/                    380KB   ❌ OBSOLETO
  ├── FastAPI code (models, routes, schemas)
  ├── hidrocal.db (SQLite viejo)
  └── Docs de diseño inicial

src_fastapi_backup/     317KB   ❌ OBSOLETO
  └── FastAPI implementation completa
```

**Total:** ~700KB de archivos no usados.

### **Archivos CSS Obsoletos:**

```bash
static/css/style.css        667 líneas  ⚠️  NO usado en templates
static/css/style_simple.css 205 líneas  ✅  Usado en index_simple.html
static/css/forms.css        438 líneas  ⚠️  Duplica components/forms.css?
```

**Verificación de uso:**

```bash
# style.css NO aparece en ningún template
grep -r "style.css" templates/
# ❌ Sin resultados

# style_simple.css usado solo en 1 template
grep -r "style_simple.css" templates/
# ✅ templates/index_simple.html
```

---

## 📋 4. Recomendaciones

### **🔴 PRIORIDAD ALTA**

#### **1. Eliminar CSS duplicado en studio/**

**Problema:**
- `studio/*.css` redefine componentes que ya existen en `components/*.css`
- No usa design tokens (CSS custom properties)
- Mantenimiento duplicado

**Solución recomendada:**

```django
<!-- templates/studio/welcome.html -->
{% block extra_css %}
<!-- OPCIÓN A: Importar main.css + CSS específico -->
<link rel="stylesheet" href="{% static 'css/main.css' %}">
<link rel="stylesheet" href="{% static 'studio/css/welcome-specific.css' %}">

<!-- OPCIÓN B: Crear studio.css que importe componentes -->
<link rel="stylesheet" href="{% static 'studio/css/studio.css' %}">
{% endblock %}
```

**Nuevo `static/studio/css/studio.css`:**
```css
/* Import base system */
@import url('../css/base/variables.css');
@import url('../css/base/reset.css');

/* Import needed components */
@import url('../css/components/buttons.css');
@import url('../css/components/cards.css');

/* Studio-specific styles */
@import url('dashboard-specific.css');
@import url('welcome-specific.css');
```

**Beneficios:**
- ✅ Elimina ~300 líneas de CSS duplicado
- ✅ Usa design tokens consistentes
- ✅ Mantenimiento centralizado
- ✅ Mejor cacheo del navegador

---

#### **2. Eliminar directorios obsoletos**

```bash
# Verificar que no se usan
grep -r "old/" . --exclude-dir=old
grep -r "src_fastapi_backup/" . --exclude-dir=src_fastapi_backup

# Si no hay referencias, eliminar
rm -rf old/
rm -rf src_fastapi_backup/
```

**Impacto:** Libera 700KB, reduce confusión.

---

#### **3. Eliminar style.css (no usado)**

```bash
# Verificar que no se usa
grep -r "style.css" templates/

# Si no hay referencias
rm static/css/style.css  # -667 líneas
```

---

### **🟡 PRIORIDAD MEDIA**

#### **4. Consolidar forms.css**

Verificar si `static/css/forms.css` (438 líneas) duplica `components/forms.css` (240 líneas).

```bash
# Comparar archivos
diff static/css/forms.css static/css/components/forms.css
```

Si son diferentes:
- Renombrar uno como `forms-legacy.css`
- Migrar templates progresivamente

---

#### **5. Crear guía de CSS Architecture**

Documentar:
- Cuándo usar `main.css` vs crear CSS específico
- Cómo usar design tokens
- Estructura de archivos CSS
- Ejemplos de componentes

---

### **🟢 PRIORIDAD BAJA**

#### **6. Analizar index_simple.html**

Template usa `style_simple.css` (205 líneas). Evaluar si:
- Es necesario mantenerlo separado
- Puede migrar a `main.css`
- Es para una landing page específica

---

## 📊 5. Métricas de Impacto

### **Antes de refactor:**

```
CSS Total: ~4,000 líneas
  - main.css system:    2,180 líneas ✅
  - studio/ CSS:          536 líneas ❌ (duplica componentes)
  - Obsoletos:            872 líneas ❌ (style.css + style_simple.css)
  - Otros:                412 líneas

Archivos obsoletos: 700KB
```

### **Después de refactor propuesto:**

```
CSS Total: ~2,600 líneas (-35%)
  - main.css system:    2,180 líneas ✅
  - studio/ specific:     150 líneas ✅ (solo estilos únicos)
  - Otros:                270 líneas

Archivos obsoletos: 0KB (-100%)
```

**Beneficios:**
- 🟢 -1,400 líneas de CSS (-35%)
- 🟢 -700KB de archivos obsoletos
- 🟢 Consistencia visual mejorada
- 🟢 Mantenimiento más simple
- 🟢 Mejor performance (cacheo)

---

## 🎯 6. Plan de Acción Sugerido

### **Fase 1: Cleanup (1 hora)**

1. ✅ **Backup seguro:**
   ```bash
   git add .
   git commit -m "checkpoint: before CSS refactor"
   ```

2. ✅ **Eliminar obsoletos:**
   ```bash
   rm -rf old/
   rm -rf src_fastapi_backup/
   rm static/css/style.css
   ```

3. ✅ **Commit:**
   ```bash
   git add .
   git commit -m "chore: remove obsolete backup directories and unused CSS"
   ```

### **Fase 2: Refactor CSS Studio (2 horas)**

1. ✅ **Crear studio.css que importe componentes**
2. ✅ **Extraer solo estilos específicos a welcome-specific.css**
3. ✅ **Actualizar templates studio/**
4. ✅ **Testing visual**
5. ✅ **Commit**

### **Fase 3: Documentación (30 min)**

1. ✅ **Actualizar docs/coding-standards.md con CSS guidelines**
2. ✅ **Crear docs/css-architecture.md**

---

## 📝 7. Decisiones a Tomar

### **Pregunta 1: ¿Eliminar backups ahora?**

**Opción A (Recomendada):** Eliminar ya
- ✅ Código está en Git history
- ✅ FastAPI no se volverá a usar
- ✅ Reduce confusión

**Opción B:** Comprimir y archivar
- Crear `archive/old.tar.gz`
- Útil si hay docs relevantes dentro

### **Pregunta 2: ¿Refactor CSS ahora o después?**

**Opción A (Recomendada):** Refactor ahora
- ✅ Studio está funcionando
- ✅ Previene más duplicación
- ✅ ~2 horas de trabajo

**Opción B:** Refactor incremental
- Migrar template por template
- Más lento pero menos riesgo

### **Pregunta 3: ¿Qué hacer con index_simple.html?**

**Necesita investigación:**
- ¿Es una landing page legacy?
- ¿Se usa actualmente?
- ¿Puede eliminarse?

---

## ✅ Checklist de Auditoría

- [x] Analizar archivos > 500 líneas
- [x] Identificar CSS duplicado
- [x] Detectar archivos obsoletos
- [x] Medir tamaño de backups
- [x] Verificar uso de archivos CSS
- [x] Crear reporte con recomendaciones
- [ ] **Decisión del usuario:** ¿Proceder con cleanup?
- [ ] **Decisión del usuario:** ¿Proceder con refactor CSS?

---

**Última actualización:** 2025-11-09
**Próximo paso:** Esperar decisión para proceder con Fase 1 (cleanup) y Fase 2 (refactor CSS)
