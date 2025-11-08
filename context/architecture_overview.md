# 🏗️ Overview de Arquitectura - HidroCalc

**Versión:** 3.0-django
**Fecha:** 2025-11-08
**Framework:** Django 5.2.8 + Django Rest Framework

---

## 📊 Stack Tecnológico

### **Backend**
- **Framework:** Django 5.2.8
- **API:** Django Rest Framework 3.16.1
- **Base de Datos:** SQLite (dev), PostgreSQL (producción futura)
- **Cache/Queue:** Redis 7.0.1, Celery 5.5.3
- **Autenticación:** Django Allauth + JWT (djangorestframework-simplejwt)

### **Frontend**
- **Templates:** Django Templates
- **CSS:** Custom Tailwind-like
- **JavaScript:** Vanilla JS + módulos
- **Gráficos:** Plotly.js 6.4.0, Matplotlib 3.10.7
- **Exportación:** ReportLab (PDF), OpenPyXL (Excel)

### **Datos y Análisis**
- **NumPy:** 2.3.4
- **Pandas:** 2.3.3
- **SciPy:** 1.16.3
- **Scikit-learn:** 1.7.2 (ML futuro)

### **Herramientas de Desarrollo**
- **MCP Servers:** Playwright, Filesystem, GitHub, PostgreSQL, Context7
- **Testing:** pytest-django (pendiente)
- **Linting:** Flake8, Black
- **Servidor:** Whitenoise (static), Gunicorn (producción)

---

## 📁 Estructura de Carpetas

```
hidro-calc/
│
├── 📋 CONTEXTO Y DOCUMENTACIÓN
│   ├── context/              Sistema de contexto de sesiones
│   │   ├── README.md
│   │   ├── current_session.md       ⭐ Estado actual
│   │   ├── completed_tasks.md
│   │   ├── next_steps.md
│   │   └── architecture_overview.md (este archivo)
│   ├── work_log/             Documentación de sesiones
│   │   ├── 00_INDICE_TRABAJO.md
│   │   ├── 01-07_*.md       Sesiones 1-7 documentadas
│   ├── docs/                 Documentación técnica detallada
│   │   ├── README.md        Guía de navegación
│   │   ├── coding-standards.md
│   │   ├── testing-guide.md
│   │   ├── error-handling.md
│   │   ├── git-workflow.md
│   │   ├── architecture-decisions.md
│   │   └── MCP_SETUP.md     Configuración de MCP servers
│   ├── old/                  Archivos obsoletos (FastAPI, docs viejos)
│   ├── CLAUDE.md            ⭐ Guía principal (concisa)
│   └── README.md            README de GitHub
│
├── 🎨 DJANGO APPS
│   ├── core/                 App principal - modelos de BD
│   │   ├── models.py        (480 líneas) - 5 modelos Django
│   │   ├── admin.py         (150 líneas) - Admin config
│   │   ├── management/commands/
│   │   │   └── seed_database.py  Comando de seed
│   │   └── migrations/
│   ├── api/                  API REST con DRF
│   │   ├── serializers.py   (380 líneas) - 15+ serializers
│   │   ├── views.py         (300 líneas) - 5 ViewSets
│   │   └── urls.py          Router DRF
│   ├── calculators/          Calculadoras rápidas (sin BD)
│   │   ├── views.py         Pendiente migrar
│   │   └── templates/
│   └── studio/               HidroStudio Professional (con BD)
│       ├── views.py         Pendiente implementar
│       └── templates/
│
├── 🖼️ FRONTEND
│   ├── templates/            Templates Django globales
│   │   └── base.html
│   └── static/
│       ├── css/
│       ├── js/
│       └── img/
│
├── ⚙️ CONFIGURACIÓN
│   ├── hidrocal_project/    Proyecto Django principal
│   │   ├── settings.py      Configuración
│   │   ├── urls.py          URLs principales
│   │   └── wsgi.py/asgi.py
│   ├── .env.django           Variables de entorno Django
│   ├── .env.mcp              Instrucciones para API keys
│   └── manage.py             CLI de Django
│
├── 📊 DATOS Y TESTS
│   ├── data/                 Datos de configuración
│   ├── tests/                Tests (pendiente)
│   └── hidrocal_django.db    Base de datos SQLite (450 KB)
│
└── 📦 OTROS
    ├── src_fastapi_backup/   Backup código FastAPI original
    ├── requirements_django.txt  Dependencias Python
    └── .gitignore
```

---

## 🗄️ Modelos de Base de Datos

### **Diagrama de Relaciones:**

```
User (Django Auth)
  │
  └─1:N─→ Project
            │
            ├─ name: str
            ├─ description: text
            ├─ location: str
            ├─ is_active: bool
            └─ timestamps
            │
            └─1:N─→ Watershed
                      │
                      ├─ name: str
                      ├─ area_hectareas: float
                      ├─ tc_horas: float
                      ├─ nc_scs: int
                      ├─ c_racional: float
                      └─ coordinates
                      │
                      ├─1:N─→ DesignStorm
                      │         │
                      │         ├─ name: str
                      │         ├─ return_period_years: int
                      │         ├─ duration_hours: float
                      │         ├─ total_rainfall_mm: float
                      │         └─ distribution_type
                      │         │
                      │         └─1:N─→ Hydrograph
                      │                   │
                      │                   ├─ method: str
                      │                   ├─ peak_discharge_m3s: float
                      │                   ├─ hydrograph_data: JSON
                      │                   └─ metadata
                      │
                      └─1:N─→ RainfallData
                                │
                                ├─ event_date: date
                                ├─ total_rainfall_mm: float
                                └─ rainfall_series: JSON
```

### **Campos Clave por Modelo:**

#### **Project** (Proyecto hidrológico)
- ID, name, description, location, country, region
- owner (ForeignKey → User)
- is_active, timestamps

#### **Watershed** (Cuenca)
- ID, project (FK), name, description
- area_hectareas, tc_horas, nc_scs, c_racional
- latitude, longitude, elevation_m
- extra_metadata (JSON)

#### **DesignStorm** (Tormenta de diseño)
- ID, watershed (FK), name
- return_period_years, duration_hours
- total_rainfall_mm, distribution_type
- SCS parameters (Ia, S)

#### **Hydrograph** (Hidrograma)
- ID, design_storm (FK), name, method
- peak_discharge_m3s, time_to_peak_minutes
- total_runoff_mm, volume_hm3
- hydrograph_data (JSON) ← Serie temporal

#### **RainfallData** (Datos de lluvia)
- ID, watershed (FK), event_date
- total_rainfall_mm, duration_hours
- rainfall_series (JSON) ← Serie temporal
- source (DNM, IMFIA, etc.)

---

## 🔌 API REST - Endpoints Disponibles

### **Base URL:** `/api/`

#### **Projects:**
```
GET    /api/projects/                    Lista de proyectos
POST   /api/projects/                    Crear proyecto
GET    /api/projects/{id}/               Detalle de proyecto
PUT    /api/projects/{id}/               Actualizar proyecto
DELETE /api/projects/{id}/               Eliminar proyecto
GET    /api/projects/{id}/watersheds/   Cuencas del proyecto
GET    /api/projects/{id}/stats/        Estadísticas del proyecto
```

#### **Watersheds:**
```
GET    /api/watersheds/                  Lista de cuencas
POST   /api/watersheds/                  Crear cuenca
GET    /api/watersheds/{id}/             Detalle de cuenca
PUT    /api/watersheds/{id}/             Actualizar cuenca
DELETE /api/watersheds/{id}/             Eliminar cuenca
GET    /api/watersheds/{id}/design_storms/     Tormentas de la cuenca
GET    /api/watersheds/{id}/rainfall_data/     Datos de lluvia
```

#### **Design Storms:**
```
GET    /api/design-storms/               Lista de tormentas
POST   /api/design-storms/               Crear tormenta
GET    /api/design-storms/{id}/          Detalle de tormenta
PUT    /api/design-storms/{id}/          Actualizar tormenta
DELETE /api/design-storms/{id}/          Eliminar tormenta
GET    /api/design-storms/{id}/hydrographs/    Hidrogramas
```

#### **Hydrographs:**
```
GET    /api/hydrographs/                 Lista de hidrogramas
POST   /api/hydrographs/                 Crear hidrograma
GET    /api/hydrographs/{id}/            Detalle de hidrograma
PUT    /api/hydrographs/{id}/            Actualizar hidrograma
DELETE /api/hydrographs/{id}/            Eliminar hidrograma
GET    /api/hydrographs/by_watershed/   Hidrogramas por cuenca
GET    /api/hydrographs/compare/        Comparar hidrogramas
```

#### **Rainfall Data:**
```
GET    /api/rainfall-data/               Lista de datos de lluvia
POST   /api/rainfall-data/               Crear registro
GET    /api/rainfall-data/{id}/          Detalle
PUT    /api/rainfall-data/{id}/          Actualizar
DELETE /api/rainfall-data/{id}/          Eliminar
```

**Total:** 30+ endpoints

---

## 🎨 Arquitectura Dual Propuesta

### **Modo 1: Calculadoras Rápidas** (`/calculators/*`)
- Sin login requerido
- Calculadoras independientes
- No persiste en BD
- Exportar a PDF/Excel
- Público: profesionales que necesitan cálculos rápidos

**Calculadoras:**
- Método Racional
- Curvas IDF Uruguay
- Tiempo de Concentración
- Coeficiente de Escorrentía Ponderado

### **Modo 2: HidroStudio Professional** (`/studio/*`)
- Login requerido
- Gestión de proyectos completos
- Base de datos persistente
- Flujo hidrológico integrado
- Reportes profesionales

**Flujo:**
1. Dashboard de proyectos
2. Gestión de cuencas
3. Análisis hidrológico completo
4. Generación de hidrogramas
5. Comparación y reportes

---

## 🔒 Autenticación y Permisos

### **Sistema de Autenticación:**
- Django Allauth (web)
- JWT tokens (API)
- Session-based (calculadoras)

### **Niveles de Acceso:**
- **Anónimo:** Calculadoras rápidas
- **Autenticado:** HidroStudio + API
- **Staff:** Admin panel
- **Superuser:** Control total

---

## 🚀 Flujo de Desarrollo

### **Comandos Frecuentes:**

```bash
# Servidor de desarrollo
python manage.py runserver

# Migraciones
python manage.py makemigrations
python manage.py migrate

# Seed de datos
python manage.py seed_database --clear

# Django shell
python manage.py shell

# Admin panel
http://localhost:8000/admin (admin/admin123)

# API
http://localhost:8000/api/
```

---

## 📊 Métricas del Proyecto

- **Total líneas de código:** ~5,000
- **Modelos Django:** 5
- **Serializers DRF:** 15+
- **ViewSets:** 5
- **Endpoints API:** 30+
- **Management Commands:** 1
- **Templates:** Pendiente migrar
- **Tests:** 0 (pendiente)

---

## 🔧 Tecnologías MCP Disponibles

1. **Playwright** - Testing automatizado
2. **Filesystem** - Gestión avanzada de archivos
3. **GitHub** - Integración con repositorio
4. **PostgreSQL** - Gestión de BD
5. **Context7** - Documentación de librerías

---

## 🎯 Estado Actual

- ✅ Backend Django completo
- ✅ API REST funcional
- ✅ Admin panel configurado
- ✅ Base de datos migrada
- ⏳ Frontend pendiente migrar
- ⏳ Autenticación pendiente
- ⏳ HidroStudio pendiente
- ⏳ Testing pendiente

---

**Última actualización:** 2025-11-08
**Versión:** 3.0-django
