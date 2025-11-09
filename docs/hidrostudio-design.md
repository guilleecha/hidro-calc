# 🏢 HidroStudio Professional - Diseño y Arquitectura

**Fecha:** 2025-11-09
**Estado:** 📝 Planificación
**Inspiración:** Planilla Excel avanzada + Software hidrológico profesional

---

## 🎯 Visión General

HidroStudio es un **workspace profesional integrado** para análisis hidrológico completo, similar a una planilla Excel avanzada pero con:
- ✅ Persistencia de datos en BD
- ✅ Visualizaciones interactivas
- ✅ Comparación de metodologías
- ✅ Generación de reportes
- ✅ Gestión de proyectos multi-cuenca

---

## 📊 Dashboard Principal

### **Layout del Dashboard**

```
┌─────────────────────────────────────────────────────────────┐
│  HidroStudio Professional - Proyecto: "Cuenca Río Santa Ana"│
├─────────────────────────────────────────────────────────────┤
│  [🏠 Proyectos] [💧 Cuencas] [🌧️ Tormentas] [📈 Hidrogramas]│
├──────────────────┬──────────────────────────────────────────┤
│                  │                                          │
│  Sidebar         │  Main Workspace                         │
│  (Navegación)    │  (Visualizaciones y Datos)              │
│                  │                                          │
│  📁 Proyectos    │  ┌────────────────────────────────┐    │
│    → Proyecto 1  │  │   Gráfico: Hietograma          │    │
│    → Proyecto 2  │  │   (Tormenta de diseño)         │    │
│                  │  └────────────────────────────────┘    │
│  💧 Cuencas      │                                          │
│    → Cuenca A    │  ┌────────────────────────────────┐    │
│    → Cuenca B    │  │   Gráfico: Hidrograma          │    │
│                  │  │   (Comparación de métodos)     │    │
│  📊 Análisis     │  └────────────────────────────────┘    │
│    → Tormentas   │                                          │
│    → Hidrogramas │  ┌────────────────────────────────┐    │
│    → Comparar    │  │   Tabla: Parámetros de cuenca  │    │
│                  │  │   Area, Tc, NC, C, etc.        │    │
│                  │  └────────────────────────────────┘    │
└──────────────────┴──────────────────────────────────────────┘
```

---

## 🗂️ Estructura de Vistas

### **1. Vista: Dashboard Principal**
**URL:** `/studio/dashboard/<project_id>/`

**Componentes:**
- **Panel izquierdo:** Árbol de navegación (Proyectos → Cuencas → Análisis)
- **Panel central:** Visualizaciones principales
  - Hietograma de tormenta de diseño
  - Hidrograma(s) superpuestos
  - Tabla resumen de parámetros
- **Panel derecho:** Info rápida de la cuenca seleccionada

**Datos mostrados:**
```python
{
    "project": Project,
    "watershed": Watershed,
    "design_storm": DesignStorm,
    "hydrographs": [Hydrograph, ...],  # Lista para comparar
    "summary_stats": {
        "peak_discharge_max": 15.2,  # m³/s
        "total_volume": 1250,         # m³
        "time_to_peak_avg": 45,       # min
    }
}
```

---

### **2. Vista: Hietogramas (Rainfall Distribution)**
**URL:** `/studio/hyetograph/<storm_id>/`

**Objetivo:** Visualizar distribución temporal de lluvia

**Gráfico:**
```
Intensidad (mm/h)
    │
120 │              ███
100 │            ██   ██
 80 │          ██       ██
 60 │        ██           ██
 40 │      ██               ██
 20 │    ██                   ██
  0 │────┴─────┴─────┴─────┴─────┴─── Tiempo (min)
       0    30    60    90   120  150
```

**Tipos de distribución:**
- Alternating Block Method
- Chicago Method
- Sidle Method
- Custom (usuario define)

**Datos necesarios:**
```python
{
    "time_steps": [0, 5, 10, 15, ...],      # minutos
    "intensity": [20, 45, 80, 120, ...],    # mm/h
    "cumulative": [0, 1.67, 5.0, 12.5, ...] # mm
}
```

---

### **3. Vista: Hidrogramas (Hydrograph Comparison)**
**URL:** `/studio/hydrographs/compare/`

**Objetivo:** Comparar múltiples hidrogramas calculados con diferentes métodos

**Gráfico:**
```
Caudal (m³/s)
    │
 15 │        Método Racional ─────
    │           ╱╲
 12 │          ╱  ╲
    │         ╱    ╲      SCS ·····
  9 │        ╱      ╲    ╱╲
    │       ╱        ╲  ╱  ╲
  6 │      ╱          ╲╱    ╲
    │     ╱                  ╲
  3 │    ╱                    ╲
    │   ╱                      ╲
  0 │──┴────────────────────────┴─── Tiempo (min)
      0   30   60   90  120  150  180
```

**Tabla de comparación:**
```
┌────────────────┬─────────────┬─────────────┬─────────────┐
│ Método         │ Q pico (m³/s)│ T pico (min)│ Vol (m³)    │
├────────────────┼─────────────┼─────────────┼─────────────┤
│ Racional       │ 15.2        │ 45          │ 1,250       │
│ SCS Unit       │ 12.8        │ 60          │ 1,320       │
│ Synth Unit     │ 13.5        │ 52          │ 1,285       │
└────────────────┴─────────────┴─────────────┴─────────────┘
```

**Parámetros de comparación:**
- ✅ Caudal pico (Q max)
- ✅ Tiempo al pico (Tp)
- ✅ Volumen total de escorrentía
- ✅ Duración de escorrentía significativa
- ✅ Forma del hidrograma (asimetría)

---

### **4. Vista: Parámetros de Cuenca**
**URL:** `/studio/watershed/<watershed_id>/parameters/`

**Layout tipo Excel:**
```
┌──────────────────────────────────────────────────┐
│  Parámetros Hidrológicos - Cuenca: "Santa Ana"  │
├──────────────────────────────────────────────────┤
│                                                   │
│  📏 CARACTERÍSTICAS FÍSICAS                       │
│  ├─ Área (A)                : 125.5 ha           │
│  ├─ Área (m²)               : 1,255,000 m²       │
│  ├─ Longitud cauce          : 2,450 m            │
│  ├─ Pendiente promedio      : 2.5 %              │
│  └─ Elevación               : 145 msnm           │
│                                                   │
│  ⏱️ TIEMPO DE CONCENTRACIÓN                       │
│  ├─ Tc (Kirpich)            : 45 min             │
│  ├─ Tc (SCS)                : 52 min             │
│  └─ Tc adoptado             : 48 min [Editable]  │
│                                                   │
│  💧 PARÁMETROS DE ESCORRENTÍA                     │
│  ├─ Coef. Racional (C)      : 0.65               │
│  ├─ Número de Curva (NC)    : 78                 │
│  ├─ Abstracción inicial (Ia): 14.2 mm            │
│  └─ Almacenamiento (S)      : 71.1 mm            │
│                                                   │
│  🌧️ TORMENTA DE DISEÑO ACTIVA                     │
│  ├─ Nombre                  : "Tr=25 años"       │
│  ├─ Período de retorno      : 25 años            │
│  ├─ Duración                : 2 horas            │
│  ├─ Lluvia total            : 85 mm              │
│  └─ Intensidad promedio     : 42.5 mm/h          │
│                                                   │
└──────────────────────────────────────────────────┘
```

---

## 🔄 Flujo de Trabajo en HidroStudio

### **Workflow típico:**

```
1. Crear Proyecto
   ↓
2. Definir Cuenca(s)
   ├─ Parámetros físicos (A, Tc, elevación)
   ├─ Parámetros hidrológicos (C, NC)
   └─ Ubicación geográfica
   ↓
3. Crear Tormenta de Diseño
   ├─ Seleccionar Tr y duración
   ├─ Definir P3,10 o usar IDF
   ├─ Elegir distribución temporal
   └─ Ver hietograma
   ↓
4. Calcular Hidrogramas
   ├─ Método Racional
   ├─ SCS Unit Hydrograph
   └─ Synthetic Unit Hydrograph
   ↓
5. Comparar Resultados
   ├─ Gráfico superpuesto
   ├─ Tabla comparativa
   └─ Análisis de sensibilidad
   ↓
6. Exportar Reporte
   ├─ PDF con gráficos
   ├─ Excel con datos
   └─ CSV para otros software
```

---

## 📊 Visualizaciones con Plotly

### **Gráfico 1: Hietograma**
```python
# static/js/plotly-charts.js

function renderHyetograph(timeSteps, intensity, containerId) {
    const data = [{
        x: timeSteps,
        y: intensity,
        type: 'bar',
        name: 'Intensidad',
        marker: {
            color: '#2563eb',
            line: {
                color: '#1e40af',
                width: 1
            }
        }
    }];

    const layout = {
        title: 'Hietograma - Distribución Temporal de Lluvia',
        xaxis: {
            title: 'Tiempo (minutos)',
            gridcolor: '#e5e7eb'
        },
        yaxis: {
            title: 'Intensidad (mm/h)',
            gridcolor: '#e5e7eb'
        },
        plot_bgcolor: '#f9fafb',
        paper_bgcolor: 'white'
    };

    Plotly.newPlot(containerId, data, layout, {responsive: true});
}
```

### **Gráfico 2: Hidrograma Comparativo**
```python
function renderHydrographComparison(hydrographs, containerId) {
    const data = hydrographs.map((hydro, index) => ({
        x: hydro.time_steps,
        y: hydro.discharge,
        type: 'scatter',
        mode: 'lines',
        name: hydro.method,
        line: {
            width: 2,
            color: COLORS[index]
        }
    }));

    const layout = {
        title: 'Comparación de Hidrogramas',
        xaxis: {
            title: 'Tiempo (minutos)',
            gridcolor: '#e5e7eb'
        },
        yaxis: {
            title: 'Caudal (m³/s)',
            gridcolor: '#e5e7eb'
        },
        hovermode: 'x unified',
        plot_bgcolor: '#f9fafb',
        paper_bgcolor: 'white',
        legend: {
            x: 1,
            y: 1,
            bgcolor: 'rgba(255,255,255,0.8)'
        }
    };

    Plotly.newPlot(containerId, data, layout, {responsive: true});
}
```

---

## 🗄️ Estructura de Base de Datos (Ya existe)

### **Modelos actuales:**
```
projects/models.py
  └─ Project (name, location, owner, is_active)

watersheds/models.py
  └─ Watershed (project, area, tc, nc_scs, c_racional)

hydrology/models.py
  ├─ DesignStorm (watershed, Tr, duration, total_rainfall, distribution_type)
  ├─ Hydrograph (design_storm, method, peak_discharge, hydrograph_data)
  └─ RainfallData (watershed, event_date, rainfall_series)
```

### **Relaciones:**
```
Project (1) ──→ (N) Watershed
Watershed (1) ──→ (N) DesignStorm
DesignStorm (1) ──→ (N) Hydrograph
Watershed (1) ──→ (N) RainfallData
```

**Perfecto!** Los modelos ya están listos. Solo falta crear las vistas.

---

## 🎨 UI Components Necesarios

### **1. Sidebar de Navegación**
```html
<nav class="studio-sidebar">
    <div class="sidebar-section">
        <h3>📁 Proyectos</h3>
        <ul class="tree-view">
            <li class="active">
                <span class="project-name">Cuenca Santa Ana</span>
                <ul class="sub-tree">
                    <li>💧 Cuenca Principal</li>
                    <li>💧 Sub-cuenca Norte</li>
                </ul>
            </li>
        </ul>
    </div>
    <div class="sidebar-section">
        <h3>📊 Análisis</h3>
        <ul class="menu-list">
            <li><a href="#">🌧️ Tormentas de Diseño</a></li>
            <li><a href="#">📈 Hidrogramas</a></li>
            <li><a href="#">📊 Comparar Métodos</a></li>
        </ul>
    </div>
</nav>
```

### **2. Cards de Resumen**
```html
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-icon">💧</div>
        <div class="stat-value">15.2</div>
        <div class="stat-label">Caudal Pico (m³/s)</div>
    </div>
    <div class="stat-card">
        <div class="stat-icon">⏱️</div>
        <div class="stat-value">45</div>
        <div class="stat-label">Tiempo al Pico (min)</div>
    </div>
    <div class="stat-card">
        <div class="stat-icon">📊</div>
        <div class="stat-value">1,250</div>
        <div class="stat-label">Volumen (m³)</div>
    </div>
</div>
```

### **3. Tabla Comparativa**
```html
<table class="comparison-table">
    <thead>
        <tr>
            <th>Método</th>
            <th>Q pico</th>
            <th>T pico</th>
            <th>Volumen</th>
            <th>Acciones</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><span class="badge badge-primary">Racional</span></td>
            <td>15.2 m³/s</td>
            <td>45 min</td>
            <td>1,250 m³</td>
            <td>
                <button class="btn-icon">📊 Ver</button>
                <button class="btn-icon">📄 Exportar</button>
            </td>
        </tr>
    </tbody>
</table>
```

---

## 🚀 Implementación por Fases

### **Fase 1: Dashboard Básico** (2-3 horas)
- [x] Modelos ya creados ✅
- [ ] Vista `studio/views.py` con dashboard
- [ ] Template `studio/dashboard.html`
- [ ] Sidebar con árbol de navegación
- [ ] Panel central con info de cuenca
- [ ] URL `/studio/dashboard/<project_id>/`

### **Fase 2: Visualizaciones** (3-4 horas)
- [ ] Integrar Plotly.js
- [ ] Hietograma interactivo
- [ ] Hidrograma simple
- [ ] Tabla de parámetros
- [ ] Cards de estadísticas

### **Fase 3: Comparación** (2-3 horas)
- [ ] Vista de comparación de hidrogramas
- [ ] Gráfico superpuesto con Plotly
- [ ] Tabla comparativa
- [ ] Análisis de diferencias

### **Fase 4: CRUD Completo** (3-4 horas)
- [ ] Crear/Editar proyectos
- [ ] Crear/Editar cuencas
- [ ] Crear/Editar tormentas
- [ ] Calcular hidrogramas con diferentes métodos
- [ ] Guardar análisis

### **Fase 5: Exportación** (2-3 horas)
- [ ] PDF con reportlab
- [ ] Excel con openpyxl
- [ ] CSV para otros software

---

## 🎯 Próximos Pasos Inmediatos

1. **Crear vista dashboard básica** en `studio/views.py`
2. **Template dashboard.html** con layout sidebar + main
3. **Integrar Plotly.js** para gráficos
4. **Vista de hietograma** con datos de DesignStorm
5. **Vista de hidrograma** con datos de Hydrograph

---

**¿Te parece bien esta estructura?** Podemos empezar por Fase 1 creando el dashboard básico con la navegación lateral y mostrar la info de una cuenca.
