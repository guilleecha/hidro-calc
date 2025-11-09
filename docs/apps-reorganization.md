# 🏗️ Plan de Reorganización en Apps - HidroCalc

**Fecha:** 2025-11-09
**Estado:** 📝 Documentado - Pendiente implementación
**Inspirado en:** [HydroML](https://github.com/guilleecha/HydroML) arquitectura multi-app

---

## 🎯 Objetivo

Dividir el proyecto de una **arquitectura monolítica** (todo en `core/`) a una **arquitectura multi-app** con separación clara de responsabilidades, siguiendo el patrón de HydroML.

---

## 📊 Análisis de Situación Actual

### **Estructura Actual de HidroCalc**

```
hidro-calc/
├── core/              # ❌ TODO mezclado aquí
│   ├── models.py      # 5 modelos hidrológicos
│   ├── admin.py       # Admin de todos los modelos
│   └── management/commands/seed_database.py
├── api/               # ✅ API REST separada (correcto)
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── calculators/       # ✅ Calculadoras separadas (correcto)
│   ├── views.py
│   ├── services/
│   └── utils/
└── studio/            # ⚠️ Vacío - no implementado
```

### **Problemas**

1. ❌ **Modelos mezclados** - Project + Watershed + Storm en la misma app
2. ❌ **Difícil escalar** - agregar features requiere modificar core/
3. ❌ **Acoplamiento alto** - todo depende de core
4. ❌ **Testing complicado** - tests mezclados
5. ❌ **Responsabilidades poco claras** - ¿qué va en core?

---

## 🎨 Estructura de HydroML (Referencia)

### **Apps de HydroML**

```
HydroML/
├── core/              # Funcionalidades compartidas básicas
├── accounts/          # Autenticación y usuarios
├── projects/          # Gestión de proyectos
├── data_tools/        # Herramientas de análisis de datos
├── connectors/        # Integraciones externas
└── experiments/       # Tracking de experimentos ML
```

**Patrón:**
- Cada app tiene **una responsabilidad clara**
- Apps son **independientes** entre sí
- Pueden **reutilizarse** en otros proyectos

---

## 🚀 Propuesta para HidroCalc

### **Nueva Estructura de Apps**

```
hidro-calc/
├── core/              # Modelos base y utilidades compartidas
│   ├── models/
│   │   └── base.py    # TimeStampedModel, etc.
│   ├── utils/
│   │   ├── conversions.py
│   │   └── validators.py
│   └── mixins/
│       └── audit.py
│
├── projects/          # 🆕 Gestión de proyectos hidrológicos
│   ├── models/
│   │   └── project.py
│   ├── admin.py
│   ├── views.py
│   └── serializers.py
│
├── watersheds/        # 🆕 Cuencas y subcuencas
│   ├── models/
│   │   ├── watershed.py
│   │   └── catchment.py  # Futuro
│   ├── admin.py
│   ├── services/
│   │   └── watershed_calculations.py
│   └── serializers.py
│
├── hydrology/         # 🆕 Análisis hidrológico (storms, hydrographs)
│   ├── models/
│   │   ├── design_storm.py
│   │   ├── hydrograph.py
│   │   └── rainfall_data.py
│   ├── services/
│   │   ├── scs_method.py
│   │   ├── rational_method.py
│   │   └── hydrograph_generator.py
│   ├── admin.py
│   └── serializers.py
│
├── calculators/       # ✅ Calculadoras rápidas (ya existe, mejorar)
│   ├── services/
│   │   ├── rational.py
│   │   ├── idf.py
│   │   └── tc.py  # Tiempo de concentración (futuro)
│   ├── views.py
│   └── templates/
│
├── data_import/       # 🆕 Importación de datos (futuro)
│   ├── importers/
│   │   ├── csv_importer.py
│   │   ├── excel_importer.py
│   │   └── dnm_importer.py  # Datos DNM Uruguay
│   └── validators/
│
├── studio/            # 🆕 HidroStudio Professional
│   ├── views.py       # Dashboard, workflow completo
│   ├── templates/
│   └── static/
│
├── api/               # ✅ API REST (ya existe, mantener)
│   ├── v1/
│   │   ├── projects/
│   │   ├── watersheds/
│   │   └── hydrology/
│   └── serializers.py
│
└── accounts/          # 🆕 Usuarios y autenticación (futuro)
    ├── models/
    ├── views.py
    └── forms.py
```

---

## 📋 Descripción de Apps

### **1. core/** - Funcionalidades compartidas

**Responsabilidad:** Base classes, utilidades, mixins

**Contenido:**
- Abstract models (TimeStampedModel)
- Utilidades de conversión (ha → m², L/s → m³/s)
- Validadores compartidos
- Constantes globales

**NO contiene:** Modelos concretos de dominio

**Ejemplo:**
```python
# core/models/base.py
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```

---

### **2. projects/** - Gestión de proyectos

**Responsabilidad:** CRUD de proyectos hidrológicos

**Modelos:**
- `Project` - Proyecto hidrológico

**Features:**
- Crear/editar/eliminar proyectos
- Asociar owner (usuario)
- Metadatos de ubicación
- Estado activo/inactivo

**Dependencias:**
- `core` (base classes)
- `accounts` (User) - futuro

---

### **3. watersheds/** - Cuencas hidrográficas

**Responsabilidad:** Gestión de cuencas y subcuencas

**Modelos:**
- `Watershed` - Cuenca principal
- `SubWatershed` - Subcuenca (futuro)
- `Catchment` - Zona de captación (futuro)

**Features:**
- Parámetros físicos (área, pendiente, etc.)
- Tiempo de concentración
- Curva número SCS
- Coeficiente de escorrentía
- Coordenadas geográficas

**Servicios:**
- Cálculo de Tc (múltiples métodos)
- Validación de parámetros
- Análisis morfométrico

**Dependencias:**
- `projects` (ForeignKey a Project)

---

### **4. hydrology/** - Análisis hidrológico

**Responsabilidad:** Tormentas, hidrogramas, datos de lluvia

**Modelos:**
- `DesignStorm` - Tormenta de diseño
- `Hydrograph` - Hidrograma
- `RainfallData` - Datos observados

**Features:**
- Generación de hidrogramas (SCS, Racional, Snyder)
- Distribución de tormentas (SCS Tipo I, II, III, IA)
- Importación de datos de lluvia
- Análisis de eventos

**Servicios:**
- `SCSHydrographGenerator`
- `RationalMethodCalculator`
- `RainfallAnalyzer`

**Dependencias:**
- `watersheds` (ForeignKey a Watershed)

---

### **5. calculators/** - Calculadoras rápidas

**Responsabilidad:** Calculadoras web sin login

**Ya existe, pero mejorar:**
- ✅ Método Racional
- ✅ Curvas IDF Uruguay
- 🆕 Tiempo de Concentración
- 🆕 Coeficiente ponderado
- 🆕 Número de curva SCS

**Features:**
- Sin autenticación
- Resultados no persisten
- Export PDF/Excel
- Templates responsive

**Dependencias:**
- Ninguna (standalone)

---

### **6. data_import/** - Importación de datos

**Responsabilidad:** Importar datos desde archivos/APIs

**Features:**
- CSV/Excel/Parquet import
- Validación de datos
- Detección de calidad
- Conexión a APIs externas (DNM, INUMET)

**Importers:**
- `CSVRainfallImporter`
- `DNMDataFetcher`
- `ExcelStationsImporter`

**Dependencias:**
- `hydrology` (crear RainfallData)
- `watersheds` (asociar a cuenca)

---

### **7. studio/** - HidroStudio Professional

**Responsabilidad:** Workflow completo con login

**Features:**
- Dashboard de proyectos
- Flujo integrado de análisis
- Gestión de cuencas + tormentas + hidrogramas
- Comparación de escenarios
- Reportes profesionales
- Gráficos interactivos

**Dependencias:**
- `projects`
- `watersheds`
- `hydrology`
- `accounts`

---

### **8. api/** - API REST

**Responsabilidad:** Endpoints REST para todas las apps

**Estructura:**
```
api/
├── v1/
│   ├── projects/
│   │   ├── views.py
│   │   ├── serializers.py
│   │   └── urls.py
│   ├── watersheds/
│   ├── hydrology/
│   └── calculators/
└── urls.py
```

**Features:**
- CRUD para todos los modelos
- Filtros avanzados
- Paginación
- Documentación Swagger/ReDoc

**Dependencias:**
- Todas las apps de dominio

---

### **9. accounts/** - Usuarios

**Responsabilidad:** Autenticación y perfiles

**Features:**
- Login/Logout/Register
- Perfil de usuario
- Permisos y roles
- OAuth (futuro)

**Dependencias:**
- `core`

---

## 🔄 Plan de Migración

### **Fase 1: Crear nuevas apps (10 min)**

```bash
# Crear apps vacías
python manage.py startapp projects
python manage.py startapp watersheds
python manage.py startapp hydrology
python manage.py startapp data_import
python manage.py startapp accounts
```

### **Fase 2: Configurar apps en settings.py (5 min)**

```python
# hidrocal_project/settings.py

INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    ...

    # Third party
    'rest_framework',

    # HidroCalc apps
    'core',              # Base y utilidades
    'projects',          # 🆕 Proyectos
    'watersheds',        # 🆕 Cuencas
    'hydrology',         # 🆕 Análisis hidrológico
    'calculators',       # Calculadoras (ya existe)
    'data_import',       # 🆕 Importación de datos
    'studio',            # HidroStudio (ya existe)
    'api',               # API REST (ya existe)
    'accounts',          # 🆕 Usuarios
]
```

### **Fase 3: Mover modelos (30 min)**

#### **3.1. projects/models/project.py**

Mover `Project` de `core/models.py` a `projects/models/project.py`

#### **3.2. watersheds/models/watershed.py**

Mover `Watershed` de `core/models.py` a `watersheds/models/watershed.py`

**Cambiar import:**
```python
# Antes
from .project import Project

# Después
from projects.models import Project
```

#### **3.3. hydrology/models/**

Crear 3 archivos:
- `design_storm.py`
- `hydrograph.py`
- `rainfall_data.py`

**Cambiar imports:**
```python
from watersheds.models import Watershed
```

### **Fase 4: Actualizar imports en serializers y views (20 min)**

```python
# Antes (api/serializers.py)
from core.models import Project, Watershed

# Después
from projects.models import Project
from watersheds.models import Watershed
from hydrology.models import DesignStorm, Hydrograph
```

### **Fase 5: Migraciones (10 min)**

```bash
# Crear migraciones para nuevas apps
python manage.py makemigrations projects
python manage.py makemigrations watersheds
python manage.py makemigrations hydrology

# Ejecutar migraciones
python manage.py migrate
```

**⚠️ IMPORTANTE:** Si Django detecta cambios en las tablas, usar `--fake` para indicar que las tablas ya existen:

```bash
python manage.py migrate projects --fake-initial
python manage.py migrate watersheds --fake-initial
python manage.py migrate hydrology --fake-initial
```

### **Fase 6: Actualizar admin.py (15 min)**

Distribuir admin de modelos en cada app:

**projects/admin.py:**
```python
from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'owner', 'is_active')
    # ... resto del admin
```

### **Fase 7: Testing (20 min)**

```bash
# Ejecutar todos los tests
python -m pytest

# Verificar que APIs funcionan
curl http://localhost:8000/api/projects/
curl http://localhost:8000/api/watersheds/

# Verificar admin
python manage.py runserver
# Visitar http://localhost:8000/admin
```

---

## 📊 Comparación: Antes vs Después

| Aspecto | Antes (Monolítico) | Después (Multi-App) |
|---------|-------------------|---------------------|
| **Apps** | 4 (core, api, calculators, studio) | 9 apps especializadas |
| **Models** | Todo en core/models.py | 1 app por dominio |
| **Responsabilidades** | Mezcladas | Clara separación |
| **Escalabilidad** | Difícil | Fácil (agregar apps) |
| **Testing** | Tests mezclados | Tests por app |
| **Reutilización** | Baja | Alta (apps independientes) |
| **Mantenibilidad** | Media | Alta |
| **Onboarding** | Confuso | Claro (cada app = feature) |

---

## 🎯 Ventajas de Multi-App

### **1. Separación de Responsabilidades**
Cada app tiene un propósito claro y único.

### **2. Escalabilidad**
Agregar features = crear nueva app, sin tocar existentes.

### **3. Testing Aislado**
Tests por app, más rápidos y enfocados.

### **4. Reutilización**
Apps pueden usarse en otros proyectos Django.

### **5. Equipo Distribuido**
Diferentes devs pueden trabajar en diferentes apps sin conflictos.

### **6. Claridad Conceptual**
Nueva persona entiende rápido:
- `projects/` = gestión de proyectos
- `watersheds/` = cuencas
- `hydrology/` = análisis hidrológico

### **7. Deploy Modular**
Posibilidad de escalar apps individualmente (microservicios futuro).

---

## 🔒 Checklist de Implementación

- [ ] Crear 5 nuevas apps (projects, watersheds, hydrology, data_import, accounts)
- [ ] Agregar apps a INSTALLED_APPS
- [ ] Mover modelo Project a projects/
- [ ] Mover modelo Watershed a watersheds/
- [ ] Mover modelos DesignStorm, Hydrograph, RainfallData a hydrology/
- [ ] Actualizar imports en api/serializers.py
- [ ] Actualizar imports en api/views.py
- [ ] Distribuir admin.py en cada app
- [ ] Crear migraciones (--fake-initial si es necesario)
- [ ] Ejecutar tests (151/151 passing)
- [ ] Verificar Django admin
- [ ] Verificar API endpoints
- [ ] Actualizar documentación

---

## ⚠️ Consideraciones y Riesgos

### **Riesgos Bajos:**
- **Imports rotos** - Fácil de detectar y arreglar
- **Admin duplicado** - Verificar que cada modelo está registrado en UNA app
- **Migraciones confusas** - Usar --fake-initial si es necesario

### **Riesgos Medios:**
- **Dependencias circulares** - Cuidado con ForeignKeys entre apps
  - ✅ CORRECTO: `hydrology → watersheds → projects`
  - ❌ INCORRECTO: `projects → watersheds → projects` (circular)

### **Mitigación:**
- Seguir jerarquía clara de dependencias
- `accounts` no depende de nadie
- `core` no depende de nadie
- `projects` depende solo de accounts
- `watersheds` depende de projects
- `hydrology` depende de watersheds

---

## 📚 Jerarquía de Dependencias

```
Nivel 0 (Base):
  ├── core           # Utilidades compartidas
  └── accounts       # Usuarios

Nivel 1 (Proyectos):
  └── projects       # Depende de accounts

Nivel 2 (Cuencas):
  └── watersheds     # Depende de projects

Nivel 3 (Análisis):
  ├── hydrology      # Depende de watersheds
  └── data_import    # Depende de watersheds + hydrology

Nivel 4 (Presentación):
  ├── calculators    # Independiente (no usa BD)
  ├── studio         # Usa projects + watersheds + hydrology
  └── api            # Expone todas las apps
```

**Regla:** Apps de nivel superior pueden importar de niveles inferiores, NUNCA al revés.

---

## 🚀 Orden de Implementación Recomendado

### **Sprint 1: Core Refactoring (Ahora)**
1. ✅ Reorganizar models en carpetas (ya documentado)
2. 🔄 Dividir en apps (este documento)

### **Sprint 2: Nuevas Apps Base (Próxima sesión)**
3. Implementar `projects/`
4. Implementar `watersheds/`
5. Implementar `hydrology/`

### **Sprint 3: Features Avanzadas**
6. Implementar `data_import/`
7. Mejorar `calculators/`
8. Desarrollar `studio/`

### **Sprint 4: Usuarios y Autenticación**
9. Implementar `accounts/`
10. Login/Logout/Register
11. Permisos por app

---

## 📖 Referencias

- **HydroML:** https://github.com/guilleecha/HydroML
- **Two Scoops of Django:** Capítulo sobre apps
- **Django Docs:** https://docs.djangoproject.com/en/5.2/ref/applications/
- **Cookiecutter Django:** Estructura de apps

---

## 💡 Siguiente Paso

**Después de reorganizar models** (docs/models-reorganization.md):

1. Implementar esta división en apps
2. Empezar por crear las 3 apps principales: `projects`, `watersheds`, `hydrology`
3. Mover modelos siguiendo el plan
4. Actualizar imports y admin
5. Testing completo

---

**Última actualización:** 2025-11-09
**Estado:** 📝 Documentado - Listo para implementar después de models refactor
**Estimado de tiempo:** 2-3 horas
**Riesgo:** Medio (requiere actualizar imports, pero es manejable)
**Prioridad:** Alta (mejora significativa en arquitectura)
