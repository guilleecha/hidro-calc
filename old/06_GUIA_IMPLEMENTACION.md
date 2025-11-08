# Guía de Implementación: Base de Datos en HidroCalc

## 📋 Tabla de Contenidos
1. [Resumen Arquitectónico](#resumen)
2. [Estructura de Directorios](#estructura)
3. [Pasos de Implementación](#pasos)
4. [Ejemplo de Flujo Completo](#ejemplo)
5. [Consultas Útiles](#consultas)
6. [Mantenimiento](#mantenimiento)

---

## Resumen Arquitectónico {#resumen}

Tu HidroCalc tendrá una estructura **jerárquica** que permite organizar y guardar hidrogramas:

```
┌─────────────────────────────────────┐
│ 1. PROYECTO (Project)               │
│ └─ "Sistema Drenaje Montevideo"     │
│                                      │
│   ┌─────────────────────────────┐   │
│   │ 2. CUENCA (Watershed)       │   │
│   │ └─ "Arroyo Miguelete Alto"  │   │
│   │    • Área: 250 ha           │   │
│   │    • Tc: 1.8 h              │   │
│   │    • NC: 72                 │   │
│   │                             │   │
│   │    ┌────────────────────┐   │   │
│   │    │ 3. TORMENTA       │   │   │
│   │    │ "Tr=10 Años 2h"   │   │   │
│   │    │ "Tr=10 Años 6h"   │   │   │
│   │    │ "Tr=10 Años 12h"  │   │   │
│   │    │ "Tr=10 Años 24h"  │   │   │
│   │    │                    │   │   │
│   │    │ ┌────────────────┐ │   │   │
│   │    │ │ 4. HIDROGRAMA │ │   │   │
│   │    │ │                │ │   │   │
│   │    │ │ - Qmax: 125 m³/s
│   │    │ │ - Tiempo pico: 45 min
│   │    │ │ - Volumen: 2,150 m³
│   │    │ │ - Serie tiempo   │ │   │   │
│   │    │ │ [t,Q,V,...]     │ │   │   │
│   │    │ └────────────────┘ │   │   │
│   │    └────────────────────┘   │   │
│   └─────────────────────────────┘   │
│                                      │
│   (Puedes tener múltiples cuencas)   │
└─────────────────────────────────────┘
```

---

## Estructura de Directorios {#estructura}

```
C:\myprojects\hidro-calc\
│
├── src\
│   ├── main.py                      # FastAPI app + rutas principales
│   ├── database.py                  # ✅ NUEVO: Configuración BD
│   │
│   ├── core\
│   │   ├── __init__.py
│   │   ├── models.py                # ✅ NUEVO: Modelos SQLAlchemy
│   │   ├── schemas.py               # ✅ NUEVO: Esquemas Pydantic
│   │   ├── rational_method.py       # Método Racional (existente)
│   │   └── scs_method.py            # ✅ NUEVO: Método SCS (para futuro)
│   │
│   ├── api\
│   │   ├── __init__.py
│   │   └── routes.py                # ✅ NUEVO: Rutas CRUD completas
│   │
│   └── services\
│       ├── __init__.py
│       └── hydrograph_service.py    # ✅ NUEVO: Lógica de negocio
│
├── templates\
│   └── index.html                   # Frontend (necesita actualizar)
│
├── static\
│   ├── css\
│   │   └── style.css
│   └── js\
│       └── app.js                   # Frontend (necesita actualizar)
│
├── tests\
│   └── test_database.py             # ✅ NUEVO: Tests de BD
│
├── .env                             # ✅ NUEVO: Variables de entorno
│
├── requirements.txt                 # Actualizar dependencias
│
└── hidrocal.db                      # Base de datos SQLite (auto-creada)
```

---

## Pasos de Implementación {#pasos}

### FASE 1: Actualizar Dependencias

**1.1 Abrir `requirements.txt` y agregar:**

```txt
# Existentes
fastapi==0.104.0
uvicorn==0.24.0
pydantic==2.5.0

# ✅ NUEVOS - Base de Datos
sqlalchemy==2.0.23
psycopg2-binary==2.9.9  # Para PostgreSQL (opcional)
pymysql==1.1.0          # Para MySQL (opcional)
alembic==1.12.1         # Para migraciones (futuro)

# Desarrollo
python-dotenv==1.0.0
pytest==7.4.3
pytest-asyncio==0.21.1
```

**1.2 Instalar dependencias:**

```bash
cd C:\myprojects\hidro-calc
.\venv\Scripts\activate

pip install -r requirements.txt
```

---

### FASE 2: Crear Archivo `.env`

**2.1 Crear archivo `C:\myprojects\hidro-calc\.env`:**

```env
# ============================================================
# Base de Datos
# ============================================================

# Opción A: SQLite (Desarrollo - por defecto)
DATABASE_URL=sqlite:///./hidrocal.db

# Opción B: PostgreSQL (Producción recomendado)
# DATABASE_URL=postgresql://user:password@localhost:5432/hidrocal_db

# Opción C: MySQL
# DATABASE_URL=mysql+pymysql://user:password@localhost:3306/hidrocal_db

# ============================================================
# Logging
# ============================================================
SQL_ECHO=false  # true para ver queries SQL

# ============================================================
# FastAPI
# ============================================================
ENVIRONMENT=development  # o production
DEBUG=true
```

---

### FASE 3: Copiar Archivos

**3.1 Copiar los 5 archivos generados:**

```bash
# DESDE: /mnt/user-data/outputs/
# A: C:\myprojects\hidro-calc\src\

copy 02_models.py          src\core\models.py
copy 03_schemas.py         src\core\schemas.py
copy 04_routes.py          src\api\routes.py
copy 05_database.py        src\database.py
```

---

### FASE 4: Actualizar `main.py`

**4.1 Reemplazar el contenido de `src/main.py`:**

```python
# src/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from database import init_db, get_db_stats, SessionLocal
from api.routes import router as api_router

# ============================================================
# Inicialización
# ============================================================

app = FastAPI(
    title="HidroCalc",
    description="Herramienta de análisis hidrológico e hidráulico",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Rutas API
app.include_router(api_router)

# ============================================================
# EVENTOS DE STARTUP
# ============================================================

@app.on_event("startup")
async def startup_event():
    """Ejecutar al iniciar la aplicación"""
    print("\n" + "="*60)
    print("🌊 HidroCalc - Herramienta de Hidrología e Hidráulica")
    print("="*60)
    
    # Inicializar base de datos
    init_db()
    
    # Mostrar estadísticas
    db = SessionLocal()
    try:
        stats = get_db_stats(db)
        print(f"\n📊 Estadísticas de Base de Datos:")
        print(f"   • Proyectos: {stats['num_projects']}")
        print(f"   • Cuencas: {stats['num_watersheds']}")
        print(f"   • Tormentas: {stats['num_design_storms']}")
        print(f"   • Hidrogramas: {stats['num_hydrographs']}")
    finally:
        db.close()
    
    print("\n🚀 Servidor iniciado en: http://localhost:8000")
    print("📚 Documentación API: http://localhost:8000/docs")
    print("="*60 + "\n")


# ============================================================
# RUTAS PRINCIPALES
# ============================================================

@app.get("/")
async def root():
    """Página principal"""
    return FileResponse("templates/index.html")


@app.get("/api/v1/health")
async def health():
    """Health check"""
    db = SessionLocal()
    try:
        stats = get_db_stats(db)
        return {"status": "ok", "database": stats}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    finally:
        db.close()


@app.get("/api/v1/docs")
async def api_docs():
    """Redirigir a documentación"""
    return FileResponse("static/api-docs.html")
```

---

### FASE 5: Inicializar Base de Datos

**5.1 Ejecutar script de inicialización:**

```bash
# OPCIÓN 1: Solo crear tablas (BD vacía)
python src/database.py init

# OPCIÓN 2: Crear tablas + datos de prueba
python src/database.py seed

# OPCIÓN 3: Reset completo (limpiar + crear + seed)
python src/database.py reset
```

**Output esperado:**

```
============================================================
HidroCalc - Database Manager
============================================================
🔧 Inicializando base de datos...
✅ Base de datos lista
🌱 Sembrando datos de prueba...
✅ Seed completado: 1 proyecto, 3 cuencas, 4 tormentas
```

---

## Ejemplo de Flujo Completo {#ejemplo}

### Scenario: Crear un nuevo análisis de tormenta

**1. Crear un Proyecto:**

```bash
POST /api/v1/projects

{
    "name": "Ampliación Drenaje Zona Norte",
    "description": "Análisis de tormentas para ampliación de drenaje",
    "location": "Zona Norte, Montevideo",
    "country": "Uruguay",
    "region": "Montevideo"
}

Response:
{
    "id": 2,
    "name": "Ampliación Drenaje Zona Norte",
    ...
}
```

**2. Crear una Cuenca dentro del Proyecto:**

```bash
POST /api/v1/projects/2/watersheds

{
    "name": "Arroyo Pando",
    "area_hectareas": 450,
    "tc_horas": 2.2,
    "nc_scs": 70,
    "latitude": -34.82,
    "longitude": -56.16
}

Response:
{
    "id": 4,
    "project_id": 2,
    "name": "Arroyo Pando",
    ...
}
```

**3. Crear Tormentas de Diseño (múltiples duraciones):**

```bash
# Tormenta de 2 horas
POST /api/v1/watersheds/4/design-storms

{
    "name": "Tr=10 Años 2h",
    "return_period_years": 10,
    "duration_hours": 2.0,
    "total_rainfall_mm": 87.5,
    "distribution_type": "alternating_block"
}

Response: {"id": 15, ...}

# Tormenta de 6 horas
POST /api/v1/watersheds/4/design-storms
{
    "name": "Tr=10 Años 6h",
    "return_period_years": 10,
    "duration_hours": 6.0,
    "total_rainfall_mm": 105.2,
    ...
}

Response: {"id": 16, ...}

# Tormenta de 12 horas
POST /api/v1/watersheds/4/design-storms
{
    "name": "Tr=10 Años 12h",
    "return_period_years": 10,
    "duration_hours": 12.0,
    "total_rainfall_mm": 128.9,
    ...
}

Response: {"id": 17, ...}

# Tormenta de 24 horas
POST /api/v1/watersheds/4/design-storms
{
    "name": "Tr=10 Años 24h",
    "return_period_years": 10,
    "duration_hours": 24.0,
    "total_rainfall_mm": 155.3,
    ...
}

Response: {"id": 18, ...}
```

**4. Calcular y Guardar Hidrogramas:**

```bash
# Para Tr=10 años 2h
POST /api/v1/design-storms/15/hydrographs

{
    "name": "Hidrograma SCS - Alternating Block",
    "method": "scs_alternating_block",
    "peak_discharge_m3s": 125.45,
    "peak_discharge_lps": 125450,
    "time_to_peak_minutes": 42,
    "total_runoff_mm": 65.3,
    "total_runoff_m3": 294350,
    "volume_hm3": 0.2944,
    "rainfall_excess_mm": 65.3,
    "infiltration_total_mm": 22.2,
    "hydrograph_data": [
        {"time_min": 0, "discharge_m3s": 0, "cumulative_volume_m3": 0},
        {"time_min": 5, "discharge_m3s": 2.5, "cumulative_volume_m3": 625},
        {"time_min": 10, "discharge_m3s": 8.3, "cumulative_volume_m3": 2250},
        ...
        {"time_min": 120, "discharge_m3s": 0.1, "cumulative_volume_m3": 294350}
    ]
}

Response: {"id": 101, ...}
```

**5. Comparar Hidrogramas de diferentes duraciones:**

```bash
POST /api/v1/compare-hydrographs

{
    "watershed_id": 4,
    "return_period_years": 10,
    "durations_hours": [2.0, 6.0, 12.0, 24.0]
}

Response:
{
    "hydrographs": [
        {
            "id": 101,
            "method": "scs_alternating_block",
            "peak_discharge_m3s": 125.45,
            "total_runoff_m3": 294350,
            "created_at": "2025-11-08T15:30:00"
        },
        {
            "id": 102,
            "method": "scs_alternating_block",
            "peak_discharge_m3s": 98.23,
            "total_runoff_m3": 472680,
            "created_at": "2025-11-08T15:35:00"
        },
        ...
    ],
    "statistics": {
        "num_hydrographs": 4,
        "max_peak_flow": 125.45,
        "min_peak_flow": 62.15,
        "avg_peak_flow": 95.67,
        "max_volume": 598430,
        "min_volume": 294350,
        "avg_volume": 425123
    }
}
```

---

## Consultas Útiles {#consultas}

### Desde Python (usando SQLAlchemy):

```python
from database import SessionLocal
from core.models import Project, Watershed, DesignStorm, Hydrograph

db = SessionLocal()

# 1. Obtener todos los proyectos
projects = db.query(Project).all()

# 2. Obtener todas las cuencas de un proyecto
project_id = 1
watersheds = db.query(Watershed).filter(
    Watershed.project_id == project_id
).all()

# 3. Obtener todas las tormentas de una cuenca
watershed_id = 4
storms = db.query(DesignStorm).filter(
    DesignStorm.watershed_id == watershed_id
).all()

# 4. Obtener todos los hidrogramas de una tormenta
design_storm_id = 15
hydrographs = db.query(Hydrograph).filter(
    Hydrograph.design_storm_id == design_storm_id
).all()

# 5. Comparar caudales para diferentes duraciones
from sqlalchemy import func
results = db.query(
    DesignStorm.duration_hours,
    func.max(Hydrograph.peak_discharge_m3s)
).join(Hydrograph).filter(
    DesignStorm.watershed_id == 4,
    DesignStorm.return_period_years == 10
).group_by(
    DesignStorm.duration_hours
).order_by(
    DesignStorm.duration_hours
).all()

# 6. Obtener hidrograma específico con todos sus datos
hydrograph = db.query(Hydrograph).filter(
    Hydrograph.id == 101
).first()

# Acceder a los datos de serie temporal
hydrograph_data = hydrograph.hydrograph_data  # Es un array JSON
for point in hydrograph_data:
    print(f"Tiempo: {point['time_min']} min, Q: {point['discharge_m3s']} m³/s")

db.close()
```

---

## Mantenimiento {#mantenimiento}

### Copias de Seguridad

```bash
# SQLite
copy hidrocal.db hidrocal_backup_$(date +%Y%m%d).db

# PostgreSQL
pg_dump -U postgres -d hidrocal_db > backup_$(date +%Y%m%d).sql

# Restaurar
psql -U postgres -d hidrocal_db < backup_20251108.sql
```

### Limpiar Datos Antiguos

```python
from database import SessionLocal
from core.models import Hydrograph
from datetime import datetime, timedelta

db = SessionLocal()

# Eliminar hidrogramas más antiguos de 30 días
old_date = datetime.utcnow() - timedelta(days=30)
db.query(Hydrograph).filter(
    Hydrograph.created_at < old_date
).delete()

db.commit()
db.close()
```

---

## 🚀 Próximos Pasos

1. **Actualizar Frontend** con interfaz para seleccionar/guardar hidrogramas
2. **Implementar Método SCS** en `core/scs_method.py`
3. **Gráficos Interactivos** con Plotly/Chart.js
4. **Migraciones de BD** con Alembic
5. **Autenticación de usuarios** con JWT
6. **Deployment** en servidor (Heroku, Railway, etc)

---

¿Preguntas sobre la implementación?
