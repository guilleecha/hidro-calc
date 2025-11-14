# 🏗️ Studio Modular Architecture - HidroCalc

**Fecha de Implementación:** 2025-11-09
**Estado:** ✅ Implementado
**Apps Afectadas:** `studio/`

---

## 🎯 Objetivo

Implementar arquitectura modular en la app `studio/` dividiendo código monolítico en módulos especializados siguiendo el principio de Single Responsibility.

---

## 📊 Antes vs Después

### **Antes (Arquitectura Monolítica):**
```
studio/
├── views.py              # 383 líneas - TODAS las views
├── forms.py              # 68 líneas - TODOS los forms
├── urls.py
└── templates/
```

### **Después (Arquitectura Modular):**
```
studio/
├── views/                    # 🆕 Módulo de vistas
│   ├── __init__.py           # Re-exports (31 líneas)
│   ├── dashboard_views.py    # Index + Dashboard (122 líneas)
│   ├── project_views.py      # CRUD Proyectos (32 líneas)
│   ├── watershed_views.py    # CRUD Cuencas (24 líneas)
│   ├── hydrograph_views.py   # Visualizaciones (45 líneas)
│   └── chart_helpers.py      # Funciones auxiliares (180 líneas)
├── forms/                    # 🆕 Módulo de formularios
│   ├── __init__.py           # Re-exports (10 líneas)
│   └── project_form.py       # ProjectCreateForm (68 líneas)
├── urls.py                   # Sin cambios
└── templates/
```

---

## ✅ Beneficios Obtenidos

### 1. **Cumplimiento de Coding Standards**
- ✅ Todos los archivos < 500 líneas
- ✅ Archivo más grande: `chart_helpers.py` (180 líneas)
- ✅ Promedio: ~75 líneas por archivo

### 2. **Separación de Responsabilidades**
| Archivo | Responsabilidad | Líneas |
|---------|----------------|--------|
| `dashboard_views.py` | Vista principal + Dashboard | 122 |
| `project_views.py` | CRUD de Proyectos | 32 |
| `watershed_views.py` | CRUD de Cuencas | 24 |
| `hydrograph_views.py` | Visualización de datos | 45 |
| `chart_helpers.py` | Generación de gráficos | 180 |

### 3. **Facilidad de Navegación**
- Antes: "¿Dónde está `project_create`?" → Buscar en 383 líneas
- Después: "¿Dónde está `project_create`?" → `project_views.py`

### 4. **Preparado para Crecimiento**
- Fácil agregar `watershed_create`, `storm_create`, etc.
- Cada archivo tiene espacio para crecer (< 200 líneas actuales)
- Pattern establecido para futuros módulos

### 5. **Testing más Fácil**
- Tests específicos por módulo
- Mock más sencillo (imports selectivos)
- Menor acoplamiento entre componentes

---

## 📁 Estructura Detallada

### **studio/views/__init__.py**
```python
"""Re-exports all views"""
from .dashboard_views import studio_index, dashboard
from .watershed_views import watershed_detail
from .hydrograph_views import hyetograph_view, hydrograph_compare
from .project_views import project_create
from .chart_helpers import (
    calculate_optimal_timestep,
    generate_hyetograph_data,
    generate_hydrograph_data
)
```

### **studio/views/dashboard_views.py**
**Funciones:**
- `studio_index(request)` - Entry point de HidroStudio
- `dashboard(request, project_id)` - Dashboard principal con gráficos

**Dependencias:**
- `projects.models.Project`
- `watersheds.models.Watershed`
- `hydrology.models.DesignStorm`, `Hydrograph`
- `.chart_helpers`

### **studio/views/project_views.py**
**Funciones:**
- `project_create(request)` - Crear proyecto con form

**Dependencias:**
- `studio.forms.ProjectCreateForm`
- `@login_required` decorator

### **studio/views/watershed_views.py**
**Funciones:**
- `watershed_detail(request, watershed_id)` - Detalle de cuenca

**Futuro:**
- `watershed_create(request)` - Crear cuenca
- `watershed_edit(request, watershed_id)` - Editar cuenca
- `watershed_delete(request, watershed_id)` - Eliminar cuenca

### **studio/views/hydrograph_views.py**
**Funciones:**
- `hyetograph_view(request, storm_id)` - Vista de hietograma
- `hydrograph_compare(request, project_id)` - Comparación de hidrogramas

**Futuro:**
- `hydrograph_detail(request, hydrograph_id)` - Detalle de hidrograma
- `storm_create(request)` - Crear tormenta de diseño

### **studio/views/chart_helpers.py**
**Funciones auxiliares (no son views):**
- `calculate_optimal_timestep(storm, custom_timestep)` - Cálculo de Δt óptimo
- `generate_hyetograph_data(storm, custom_timestep)` - Datos para gráfico de lluvia
- `generate_hydrograph_data(hydrograph)` - Datos para gráfico de caudal

**Nota:** Estas funciones NO son views de Django, son helpers puros.

---

## 🔗 Imports y Compatibilidad

### **URLs no necesitan cambios:**
```python
# studio/urls.py
from . import views

urlpatterns = [
    path('', views.studio_index, name='index'),
    path('dashboard/<int:project_id>/', views.dashboard, name='dashboard'),
    # ... etc
]
```

✅ **Funciona automáticamente** porque `views/__init__.py` re-exporta todo.

### **Imports desde otras apps:**
```python
# Opción 1: Import específico
from studio.views import project_create, dashboard

# Opción 2: Import de módulo (para testing)
from studio.views.project_views import project_create
from studio.views.dashboard_views import dashboard

# Opción 3: Import del paquete (para URLs)
from studio import views
views.project_create(request)
```

---

## 🎨 Pattern: Forms Modular

### **Implementado en paralelo:**
```
studio/forms/
├── __init__.py
└── project_form.py
```

### **Re-export en __init__.py:**
```python
from .project_form import ProjectCreateForm

__all__ = ['ProjectCreateForm']
```

### **Import desde views:**
```python
from studio.forms import ProjectCreateForm  # ✅ Clean import
```

---

## 🚀 Plan de Expansión Futura

### **Cuando se agreguen más views:**

#### 1. **CRUD Completo de Proyectos:**
Agregar a `project_views.py`:
```python
def project_list(request)          # Listar proyectos
def project_detail(request, id)    # Ver detalle
def project_edit(request, id)      # Editar
def project_delete(request, id)    # Eliminar
```

#### 2. **CRUD Completo de Cuencas:**
Expandir `watershed_views.py`:
```python
def watershed_create(request, project_id)
def watershed_edit(request, watershed_id)
def watershed_delete(request, watershed_id)
```

#### 3. **Gestión de Tormentas:**
Crear `storm_views.py`:
```python
def storm_create(request, watershed_id)
def storm_edit(request, storm_id)
def storm_list(request)
```

#### 4. **Cálculo de Hidrogramas:**
Crear `calculation_views.py`:
```python
def calculate_hydrograph(request, storm_id)
def hydrograph_results(request, hydrograph_id)
```

---

## 📏 Reglas y Convenciones

### **Cuando crear un nuevo archivo en views/:**
1. Archivo actual > 200 líneas → Considerar split
2. Funcionalidad completamente nueva → Nuevo archivo
3. Funcionalidad relacionada → Agregar a archivo existente

### **Naming Conventions:**
- Archivos: `{entity}_views.py` (snake_case)
- Módulos helpers: `{purpose}_helpers.py`
- Functions: Django view functions (snake_case)

### **Import Order (en cada view file):**
```python
# 1. Standard library
import json
from datetime import datetime

# 2. Django imports
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

# 3. Local app imports
from projects.models import Project
from studio.forms import ProjectCreateForm

# 4. Relative imports (same module)
from .chart_helpers import generate_hyetograph_data
```

---

## 🧪 Testing Strategy

### **Unit Tests por Módulo:**
```
tests/studio/
├── test_dashboard_views.py
├── test_project_views.py
├── test_watershed_views.py
├── test_hydrograph_views.py
└── test_chart_helpers.py
```

### **Ventajas:**
- Tests aislados por responsabilidad
- Fácil identificar qué rompió
- Menor tiempo de ejecución (tests granulares)

---

## 📊 Métricas

### **Antes de Refactor:**
- **Archivos:** 2 (`views.py`, `forms.py`)
- **Líneas totales:** 451
- **Líneas por archivo:** 226 (promedio)
- **Archivo más grande:** 383 líneas

### **Después de Refactor:**
- **Archivos:** 11 (6 views/ + 2 forms/ + 2 __init__.py + urls.py)
- **Líneas totales:** ~512 (incluye __init__.py y docs)
- **Líneas por archivo:** ~75 (promedio, excluyendo __init__.py)
- **Archivo más grande:** 180 líneas (`chart_helpers.py`)

### **Mejora:**
- ✅ Reducción 54% en tamaño del archivo más grande (383 → 180)
- ✅ Mejor distribución de responsabilidades
- ✅ Cumplimiento 100% de coding standards (< 500 líneas)

---

## 🔄 Migration Path (para otras apps)

### **Apps candidatas para refactor similar:**
1. **api/** - Si `serializers.py` o `views.py` > 300 líneas
2. **calculators/** - Cuando se agreguen más calculadoras
3. **hydrology/** - Ya usa modular para models, considerar para services

### **Cuándo NO refactorizar:**
- App pequeña (< 200 líneas totales)
- Funcionalidad muy acoplada (difícil separar)
- Sin planes de expansión

---

## 📝 Checklist de Implementación

Para replicar este pattern en otra app:

- [ ] Crear directorio `{app}/views/`
- [ ] Dividir views por entidad o funcionalidad
- [ ] Crear `__init__.py` con re-exports
- [ ] Actualizar imports si es necesario
- [ ] Eliminar archivo viejo `views.py`
- [ ] Probar imports: `python manage.py shell -c "from {app}.views import ..."`
- [ ] Verificar que URLs siguen funcionando
- [ ] Actualizar documentación

---

## 🔗 Referencias

- **Work Log:** `work_log/09_HYETOGRAPH_PEAK_POSITION_PROJECT_FORMS.md` - Sesión de implementación
- **Coding Standards:** `docs/coding-standards.md` - Reglas de tamaño de archivos
- **Apps Reorganization:** `docs/apps-reorganization.md` - Plan general de arquitectura

---

**Última actualización:** 2025-11-09
**Implementado por:** Claude Code Session #9
**Status:** ✅ Productivo - Pattern establecido para futuras expansiones
