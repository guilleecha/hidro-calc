# Diseño de Base de Datos para HidroCalc
## Arquitectura Jerárquica Completa

---

## 📊 ESTRUCTURA RELACIONAL

```
PROYECTOS (Project)
    ↓
CUENCAS (Watershed)
    ↓
TORMENTAS DE DISEÑO (DesignStorm)
    ↓
HIDROGRAMAS (Hydrograph)
```

---

## 🗂️ TABLAS Y RELACIONES

### 1. **TABLA: `projects`**
Nivel superior - Agrupa toda la información de un proyecto

```sql
CREATE TABLE projects (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    location VARCHAR(255),
    country VARCHAR(100),
    region VARCHAR(100),
    timezone VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Metadata
    owner_id INT,  -- Para multi-usuario futuro
    is_active BOOLEAN DEFAULT TRUE,
    
    INDEX idx_owner (owner_id),
    INDEX idx_active (is_active)
);
```

**Registros de ejemplo:**
- "Sistema de Drenaje Montevideo"
- "Presa Tacuarembó"
- "Canalización Río Negro"

---

### 2. **TABLA: `watersheds`**
Información de las cuencas dentro de cada proyecto

```sql
CREATE TABLE watersheds (
    id INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    
    -- Características hidráulicas
    area_hectareas DECIMAL(12,2) NOT NULL,
    tc_horas DECIMAL(8,4) NOT NULL,  -- Tiempo de concentración
    nc_scs INT,  -- Número de curva SCS (0-100)
    
    -- Ubicación
    latitude DECIMAL(10,6),
    longitude DECIMAL(10,6),
    elevation_m DECIMAL(10,2),
    
    -- Coeficiente de escorrentía
    c_racional DECIMAL(4,3),  -- Coeficiente C para Método Racional
    
    metadata JSON,  -- Para datos adicionales (permeabilidad, etc)
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    UNIQUE KEY unique_watershed (project_id, name),
    INDEX idx_project (project_id),
    INDEX idx_area (area_hectareas)
);
```

**Registros de ejemplo:**
```
Proyecto: "Sistema de Drenaje Montevideo"
├─ Cuenca 1: "Arroyo Miguelete Alto"
│  └─ area: 250 ha, tc: 1.8h, nc: 72
├─ Cuenca 2: "Arroyo Carrasco Medio"
│  └─ area: 180 ha, tc: 1.5h, nc: 75
└─ Cuenca 3: "Arroyo Pantanoso"
   └─ area: 320 ha, tc: 2.1h, nc: 68
```

---

### 3. **TABLA: `design_storms`**
Tormentas de diseño parametrizadas

```sql
CREATE TABLE design_storms (
    id INT PRIMARY KEY AUTO_INCREMENT,
    watershed_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    
    -- Parámetros básicos
    return_period_years INT NOT NULL,  -- Período de retorno (10, 25, 100, etc)
    duration_hours DECIMAL(8,2) NOT NULL,  -- 2, 6, 12, 24, etc
    
    -- Lluvia total
    total_rainfall_mm DECIMAL(8,2) NOT NULL,  -- Profundidad de lluvia total
    
    -- Método de distribución
    distribution_type VARCHAR(50),  -- 'alternating_block', 'chicago', 'sidle', 'custom'
    
    -- Parámetros SCS
    initial_abstraction_mm DECIMAL(8,3),  -- Ia = 0.2*S
    storage_parameter_mm DECIMAL(8,3),    -- S = (25400/NC - 254)
    
    -- Parámetro de tiempo
    time_step_minutes INT DEFAULT 5,  -- Intervalo de cálculo
    
    metadata JSON,  -- Información adicional (fuente de datos, notas, etc)
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (watershed_id) REFERENCES watersheds(id) ON DELETE CASCADE,
    UNIQUE KEY unique_storm (watershed_id, name),
    INDEX idx_watershed (watershed_id),
    INDEX idx_return_period (return_period_years),
    INDEX idx_duration (duration_hours)
);
```

**Registros de ejemplo:**
```
Cuenca: "Arroyo Miguelete Alto"
├─ Tormenta: "Tr=10 Años 2h"
│  └─ return_period: 10, duration: 2.0h, rainfall: 85.3 mm
├─ Tormenta: "Tr=10 Años 6h"
│  └─ return_period: 10, duration: 6.0h, rainfall: 102.5 mm
├─ Tormenta: "Tr=10 Años 12h"
│  └─ return_period: 10, duration: 12.0h, rainfall: 125.8 mm
└─ Tormenta: "Tr=10 Años 24h"
   └─ return_period: 10, duration: 24.0h, rainfall: 152.2 mm
```

---

### 4. **TABLA: `hydrographs`** ⭐ LA MÁS IMPORTANTE
Almacena los hidrogramas calculados con TODOS sus puntos

```sql
CREATE TABLE hydrographs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    design_storm_id INT NOT NULL,
    
    -- Identificación
    name VARCHAR(255),  -- Nombre descriptivo
    
    -- Parámetros del cálculo
    method VARCHAR(50),  -- 'rational', 'scs_unit_hydrograph', 'synth_unit_hydro'
    
    -- Resultados resumen
    peak_discharge_m3s DECIMAL(10,3) NOT NULL,  -- Q máximo (m³/s)
    peak_discharge_lps DECIMAL(12,2),           -- Q máximo (L/s)
    time_to_peak_minutes DECIMAL(8,2),          -- Tiempo al pico
    total_runoff_mm DECIMAL(8,3),               -- Escorrentía total (mm)
    total_runoff_m3 DECIMAL(14,2),              -- Escorrentía total (m³)
    volume_hm3 DECIMAL(10,3),                   -- Volumen en hm³
    
    -- Datos del hidrograma (JSON con serie temporal)
    hydrograph_data JSON NOT NULL,  -- Array de {time_min, discharge_m3s, cumulative_volume_m3}
    
    -- Metadata
    rainfall_excess_mm DECIMAL(8,3),  -- Lluvia neta después de abstracciones
    infiltration_total_mm DECIMAL(8,3),
    
    notes TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (design_storm_id) REFERENCES design_storms(id) ON DELETE CASCADE,
    INDEX idx_design_storm (design_storm_id),
    INDEX idx_method (method),
    INDEX idx_peak (peak_discharge_m3s)
);
```

**Ejemplo de `hydrograph_data` (JSON):**
```json
[
  {"time_min": 0, "discharge_m3s": 0.0, "cum_volume_m3": 0},
  {"time_min": 5, "discharge_m3s": 2.45, "cum_volume_m3": 612.5},
  {"time_min": 10, "discharge_m3s": 5.82, "cum_volume_m3": 2150.3},
  {"time_min": 15, "discharge_m3s": 9.34, "cum_volume_m3": 4285.2},
  {"time_min": 20, "discharge_m3s": 12.87, "cum_volume_m3": 6952.1},
  {"time_min": 25, "discharge_m3s": 15.23, "cum_volume_m3": 9125.4},
  {"time_min": 30, "discharge_m3s": 14.56, "cum_volume_m3": 11203.8},
  ...
  {"time_min": 120, "discharge_m3s": 0.15, "cum_volume_m3": 28547.6}
]
```

---

### 5. **TABLA: `rainfall_data` (Opcional pero recomendada)**
Datos de lluvia medidos para calibración

```sql
CREATE TABLE rainfall_data (
    id INT PRIMARY KEY AUTO_INCREMENT,
    watershed_id INT NOT NULL,
    
    event_date DATE NOT NULL,
    return_period_years INT,  -- Tr estimado
    duration_hours DECIMAL(8,2),
    total_rainfall_mm DECIMAL(8,2),
    
    -- Serie de intensidades
    rainfall_series JSON,  -- {time_min, intensity_mm_h, cumulative_mm}
    
    source VARCHAR(100),  -- DNM, IMFIA, sensor local, etc
    notes TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (watershed_id) REFERENCES watersheds(id) ON DELETE CASCADE,
    INDEX idx_watershed (watershed_id),
    INDEX idx_event_date (event_date)
);
```

---

## 🔑 RELACIONES Y CARDINALIDAD

```
1 Project ——— N Watersheds
1 Watershed ——— N Design_Storms
1 Design_Storm ——— N Hydrographs
1 Watershed ——— N Rainfall_Data (opcional)
```

**Cardinalidad detallada:**
- Un Proyecto contiene múltiples Cuencas
- Una Cuenca puede tener múltiples Tormentas (Tr=10,25,100 y duraciones 2,6,12,24h)
- Una Tormenta genera UN hidrograma principal, pero puedes guardar variantes (diferentes métodos)
- Los Datos de lluvia se relacionan directamente con la Cuenca

---

## 📈 CONSULTAS TÍPICAS

### 1. Obtener todos los hidrogramas de una cuenca
```sql
SELECT h.* 
FROM hydrographs h
JOIN design_storms ds ON h.design_storm_id = ds.id
JOIN watersheds w ON ds.watershed_id = w.id
WHERE w.id = 1;
```

### 2. Comparar caudales máximos para diferentes duraciones
```sql
SELECT 
    ds.duration_hours,
    ds.return_period_years,
    h.peak_discharge_m3s,
    h.total_runoff_m3,
    h.created_at
FROM hydrographs h
JOIN design_storms ds ON h.design_storm_id = ds.id
WHERE ds.watershed_id = 1
ORDER BY ds.return_period_years, ds.duration_hours;
```

### 3. Obtener todos los proyectos de un usuario
```sql
SELECT * FROM projects WHERE owner_id = 123;
```

### 4. Buscar cuencas por área
```sql
SELECT * FROM watersheds 
WHERE area_hectareas BETWEEN 100 AND 500
ORDER BY area_hectareas DESC;
```

---

## 🛠️ ÍNDICES PARA OPTIMIZACIÓN

```sql
-- Ya definidos en las tablas, pero aquí el resumen:

-- Proyectos
CREATE INDEX idx_project_owner ON projects(owner_id);
CREATE INDEX idx_project_active ON projects(is_active);

-- Cuencas
CREATE INDEX idx_watershed_project ON watersheds(project_id);
CREATE INDEX idx_watershed_area ON watersheds(area_hectareas);

-- Tormentas
CREATE INDEX idx_storm_watershed ON design_storms(watershed_id);
CREATE INDEX idx_storm_tr ON design_storms(return_period_years);
CREATE INDEX idx_storm_duration ON design_storms(duration_hours);

-- Hidrogramas
CREATE INDEX idx_hydro_storm ON hydrographs(design_storm_id);
CREATE INDEX idx_hydro_method ON hydrographs(method);
CREATE INDEX idx_hydro_peak ON hydrographs(peak_discharge_m3s);

-- Datos de lluvia
CREATE INDEX idx_rainfall_watershed ON rainfall_data(watershed_id);
CREATE INDEX idx_rainfall_date ON rainfall_data(event_date);
```

---

## 📝 MODELO ENTIDAD-RELACIÓN (MER)

```
┌──────────────────┐
│   PROJECTS       │
├──────────────────┤
│ PK: id           │
│ name             │
│ description      │
│ location         │
│ owner_id         │
│ created_at       │
└────────┬─────────┘
         │ 1:N
         │
┌────────▼──────────────┐
│   WATERSHEDS         │
├──────────────────────┤
│ PK: id               │
│ FK: project_id       │
│ name                 │
│ area_hectareas       │
│ tc_horas             │
│ nc_scs               │
│ c_racional           │
│ latitude, longitude  │
└────────┬─────────────┘
         │ 1:N
         │
┌────────▼──────────────────┐
│   DESIGN_STORMS          │
├──────────────────────────┤
│ PK: id                   │
│ FK: watershed_id         │
│ name                     │
│ return_period_years      │
│ duration_hours           │
│ total_rainfall_mm        │
│ distribution_type       │
│ time_step_minutes       │
└────────┬─────────────────┘
         │ 1:N
         │
┌────────▼──────────────────┐
│   HYDROGRAPHS ⭐         │
├──────────────────────────┤
│ PK: id                   │
│ FK: design_storm_id      │
│ name                     │
│ method                   │
│ peak_discharge_m3s       │
│ time_to_peak_minutes     │
│ total_runoff_m3          │
│ hydrograph_data (JSON)   │
│ created_at               │
└──────────────────────────┘
```

---

## 🚀 VENTAJAS DE ESTA ARQUITECTURA

✅ **Escalabilidad**: Crece con múltiples proyectos y cuencas  
✅ **Reutilización**: Guardar hidrogramas para comparación posterior  
✅ **Flexibilidad**: JSON permite datos heterogéneos  
✅ **Rastreabilidad**: Timestamps y auditoría integrada  
✅ **Integridad referencial**: Relaciones bien definidas  
✅ **Consultas eficientes**: Índices estratégicos  
✅ **Multi-método**: Soporta Racional, SCS, UH sintéticos, etc  

---

## 📱 SIGUIENTE PASO: IMPLEMENTACIÓN

Esta estructura se implementará en:
1. **SQLAlchemy ORM** (Python)
2. **FastAPI** (Backend)
3. **PostgreSQL o MySQL** (Base de datos)
4. **React o Vue** (Frontend)

¿Preguntas sobre la estructura? ¿Necesitas ajustes?
