# HidroCalc v2.0 - Arquitectura de Base de Datos

## 🎯 Visión General

Tu aplicación HidroCalc ahora tendrá una **arquitectura completa de base de datos** que permite:

✅ **Guardar múltiples proyectos** de análisis hidrológico  
✅ **Organizar cuencas por proyecto** con parámetros específicos  
✅ **Crear tormentas de diseño** con duraciones variables (2h, 6h, 12h, 24h)  
✅ **Almacenar hidrogramas calculados** con series temporales completas  
✅ **Comparar hidrogramas** de diferentes duraciones  
✅ **Reutilizar datos** sin recalcular  

---

## 📊 Estructura de Datos

### Jerarquía de Datos:

```
PROJECT (1 Nivel)
│
├─ WATERSHED (N por proyecto)
│  │
│  ├─ DESIGN_STORM (N por cuenca, múltiples duraciones)
│  │  │
│  │  └─ HYDROGRAPH (N por tormenta, diferentes métodos)
│  │     └─ [Serie temporal: tiempo, caudal, volumen acumulado]
│  │
│  └─ RAINFALL_DATA (Opcional: datos medidos para calibración)
│
└─ [Más cuencas...]
```

### Ejemplo Concreto:

```
📁 Sistema de Drenaje Montevideo
│
├─ 🌊 Cuenca: Arroyo Miguelete Alto (250 ha, Tc=1.8h, NC=72)
│  │
│  ├─ 🌧️ Tormenta: Tr=10 años, 2 horas (85.3 mm)
│  │  └─ 📈 Hidrograma: Qmax=125 m³/s, V=294,350 m³
│  │
│  ├─ 🌧️ Tormenta: Tr=10 años, 6 horas (102.5 mm)
│  │  └─ 📈 Hidrograma: Qmax=98 m³/s, V=472,680 m³
│  │
│  ├─ 🌧️ Tormenta: Tr=10 años, 12 horas (125.8 mm)
│  │  └─ 📈 Hidrograma: Qmax=72 m³/s, V=635,420 m³
│  │
│  └─ 🌧️ Tormenta: Tr=10 años, 24 horas (152.2 mm)
│     └─ 📈 Hidrograma: Qmax=45 m³/s, V=768,890 m³
│
└─ 🌊 Cuenca: Arroyo Carrasco Medio (180 ha, Tc=1.5h, NC=75)
   ├─ 🌧️ Tormenta: Tr=10 años, 2 horas
   │  └─ 📈 Hidrograma...
   └─ 🌧️ Tormenta: Tr=10 años, 24 horas
      └─ 📈 Hidrograma...
```

---

## 🗄️ Tablas Principales

| Tabla | Descripción | Registros |
|-------|-------------|-----------|
| **projects** | Proyectos de análisis | Múltiples |
| **watersheds** | Cuencas hidrográficas | N por proyecto |
| **design_storms** | Tormentas parametrizadas | N por cuenca |
| **hydrographs** | Hidrogramas calculados | N por tormenta |
| **rainfall_data** | Datos de lluvia medidos | Opcional |

---

## 🔄 Relaciones

```
1 Proyecto ──→ N Cuencas
1 Cuenca ──→ N Tormentas de Diseño
1 Tormenta ──→ N Hidrogramas

Ejemplo:
- 1 proyecto puede tener 3+ cuencas
- 1 cuenca puede tener 12+ tormentas (3 Tr × 4 duraciones)
- 1 tormenta puede tener 2+ hidrogramas (diferentes métodos)
```

---

## 📁 Archivos Entregados

```
/outputs/

1. 01_DISEÑO_BASE_DATOS_HIDROC.md    ← Especificación técnica completa
2. 02_models.py                       ← Modelos SQLAlchemy ORM
3. 03_schemas.py                      ← Esquemas Pydantic de validación
4. 04_routes.py                       ← Rutas FastAPI CRUD
5. 05_database.py                     ← Configuración y utilidades BD
6. 06_GUIA_IMPLEMENTACION.md          ← Instrucciones paso a paso
7. README.md                          ← Este archivo
```

---

## 🚀 Inicio Rápido

### 1. Copiar archivos al proyecto

```bash
copy 02_models.py    C:\myprojects\hidro-calc\src\core\models.py
copy 03_schemas.py   C:\myprojects\hidro-calc\src\core\schemas.py
copy 04_routes.py    C:\myprojects\hidro-calc\src\api\routes.py
copy 05_database.py  C:\myprojects\hidro-calc\src\database.py
```

### 2. Actualizar `requirements.txt`

```txt
sqlalchemy==2.0.23
python-dotenv==1.0.0
```

### 3. Instalar y inicializar

```bash
pip install -r requirements.txt
python src/database.py seed
```

### 4. Ejecutar servidor

```bash
python src/main.py
```

### 5. Acceder a API

- **Web**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **Base de datos**: `hidrocal.db` (SQLite)

---

## 💾 API Endpoints

### Proyectos
```
GET    /api/v1/projects                    → Listar todos
POST   /api/v1/projects                    → Crear nuevo
GET    /api/v1/projects/{id}               → Obtener detalles
PUT    /api/v1/projects/{id}               → Actualizar
DELETE /api/v1/projects/{id}               → Eliminar
```

### Cuencas
```
GET    /api/v1/projects/{id}/watersheds    → Listar por proyecto
POST   /api/v1/projects/{id}/watersheds    → Crear nueva
GET    /api/v1/watersheds/{id}             → Obtener detalles
PUT    /api/v1/watersheds/{id}             → Actualizar
DELETE /api/v1/watersheds/{id}             → Eliminar
GET    /api/v1/watersheds/{id}/summary     → Resumen estadístico
```

### Tormentas
```
GET    /api/v1/watersheds/{id}/design-storms      → Listar por cuenca
POST   /api/v1/watersheds/{id}/design-storms      → Crear nueva
GET    /api/v1/design-storms/{id}                 → Obtener detalles
PUT    /api/v1/design-storms/{id}                 → Actualizar
DELETE /api/v1/design-storms/{id}                 → Eliminar
```

### Hidrogramas ⭐
```
GET    /api/v1/design-storms/{id}/hydrographs    → Listar por tormenta
POST   /api/v1/design-storms/{id}/hydrographs    → Guardar nuevo
GET    /api/v1/hydrographs/{id}                  → Obtener completo
PUT    /api/v1/hydrographs/{id}                  → Actualizar
DELETE /api/v1/hydrographs/{id}                  → Eliminar
POST   /api/v1/compare-hydrographs               → Comparar múltiples
```

---

## 📊 Ejemplo de Respuesta API

### GET `/api/v1/watersheds/4/summary`

```json
{
  "watershed": {
    "id": 4,
    "project_id": 1,
    "name": "Arroyo Miguelete Alto",
    "area_hectareas": 250,
    "tc_horas": 1.8,
    "nc_scs": 72,
    "latitude": -34.85,
    "longitude": -56.15,
    "elevation_m": 50,
    "c_racional": null,
    "created_at": "2025-11-08T10:30:00"
  },
  "num_design_storms": 4,
  "num_hydrographs": 4,
  "peak_flow_statistics": {
    "max_peak_flow_m3s": 125.45,
    "min_peak_flow_m3s": 45.20
  }
}
```

### POST `/api/v1/compare-hydrographs`

```json
{
  "hydrographs": [
    {
      "id": 101,
      "name": null,
      "method": "scs_alternating_block",
      "peak_discharge_m3s": 125.45,
      "peak_discharge_lps": 125450,
      "total_runoff_m3": 294350,
      "created_at": "2025-11-08T15:30:00"
    },
    {
      "id": 102,
      "name": null,
      "method": "scs_alternating_block",
      "peak_discharge_m3s": 98.23,
      "peak_discharge_lps": 98230,
      "total_runoff_m3": 472680,
      "created_at": "2025-11-08T15:35:00"
    }
  ],
  "statistics": {
    "num_hydrographs": 4,
    "max_peak_flow": 125.45,
    "min_peak_flow": 45.20,
    "avg_peak_flow": 87.23,
    "max_volume": 768890,
    "min_volume": 294350,
    "avg_volume": 517855
  }
}
```

---

## 🎨 Características Clave

### 1. **JSON para Series Temporales**
Los hidrogramas almacenan datos completos:
```json
"hydrograph_data": [
  {"time_min": 0, "discharge_m3s": 0, "cumulative_volume_m3": 0},
  {"time_min": 5, "discharge_m3s": 2.45, "cumulative_volume_m3": 612.5},
  {"time_min": 10, "discharge_m3s": 5.82, "cumulative_volume_m3": 2150.3},
  ...
]
```

### 2. **Flexibilidad en Metadata**
Campo JSON para datos adicionales:
```json
"metadata": {
  "calibration_notes": "Revisado con datos 2023",
  "data_source": "DNM",
  "uncertainty_factor": 1.15
}
```

### 3. **Índices para Rendimiento**
- Búsquedas rápidas por cuenca
- Filtrado eficiente por período de retorno
- Consultas de comparación optimizadas

---

## 🔐 Seguridad (Futuro)

Para proteger datos:
- [ ] Añadir autenticación con JWT
- [ ] Validar permisos por usuario
- [ ] Encriptar datos sensibles
- [ ] Auditoría de cambios
- [ ] Backups automáticos

---

## 📈 Casos de Uso Futuros

1. **Análisis Multi-Método**: Guardar hidrogramas con Racional, SCS, Snyder, etc
2. **Calibración**: Comparar hidrogramas sintéticos vs medidos
3. **Diseño de Obras**: Usar hidrogramas máximos para dimensionamiento
4. **Informes**: Generar reportes automáticos con gráficos
5. **Colaboración**: Multi-usuario con permisos

---

## 📝 Documentación

Para más detalles:
- 📖 **Especificación técnica**: Ver `01_DISEÑO_BASE_DATOS_HIDROC.md`
- 🛠️ **Guía de implementación**: Ver `06_GUIA_IMPLEMENTACION.md`
- 📚 **API completa**: http://localhost:8000/docs

---

## 💬 Preguntas Frecuentes

**P: ¿Puedo usar PostgreSQL en lugar de SQLite?**  
R: Sí, solo cambia `DATABASE_URL` en `.env` a `postgresql://...`

**P: ¿Cómo elimino datos antiguos?**  
R: Ver script en `06_GUIA_IMPLEMENTACION.md` - sección "Mantenimiento"

**P: ¿Puedo exportar hidrogramas?**  
R: Sí, el JSON permite exportar fácilmente a CSV, Excel, etc

**P: ¿Cuántos registros puedo guardar?**  
R: Depende de la BD, pero SQLite soporta millones de registros sin problema

---

## 🚀 Próximas Fases

| Fase | Descripción | Estado |
|------|-------------|--------|
| 1 | MVP con Método Racional | ✅ Hecho |
| 2 | Base de datos jerárquica | ✅ Diseño entregado |
| 3 | Hidrogramas y comparación | ⏳ Implementar |
| 4 | Gráficos interactivos | ⏳ Próximo |
| 5 | Multi-método (SCS, Snyder) | ⏳ Futuro |
| 6 | Autenticación y multi-usuario | ⏳ Futuro |

---

**Versión**: 2.0  
**Fecha**: Noviembre 2025  
**Estado**: Listo para implementación  

¿Listo para comenzar? 🚀
