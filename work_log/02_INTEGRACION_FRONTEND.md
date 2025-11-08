# 🎨 Sesión 2: Integración Frontend-Backend

**Fecha:** 2025-11-08
**Duración:** En progreso...
**Estado:** 🔄 En Progreso

---

## 🎯 Objetivos de la Sesión

Conectar la interfaz web existente con la API de base de datos para:
- Cargar proyectos y cuencas desde BD en lugar de memoria
- Guardar hidrogramas calculados automáticamente
- Visualizar historial de cálculos
- Comparar múltiples hidrogramas

---

## 📋 Plan de Trabajo

### Fase 1: Análisis del Frontend Existente ✅
- [x] Revisar templates HTML (index.html, rational.html, idf.html)
- [x] Revisar JavaScript actual (app.js, rational.js, idf.js)
- [x] Identificar puntos de integración

### Fase 2: Implementación de Carga desde BD
- [ ] Agregar selector de proyectos en la UI
- [ ] Agregar selector de cuencas vinculado al proyecto
- [ ] Cargar datos de cuenca seleccionada en formulario

### Fase 3: Guardar Hidrogramas Automáticamente
- [ ] Modificar función de cálculo para enviar a API
- [ ] Implementar POST a /api/v1/design-storms/{id}/hydrographs
- [ ] Mostrar confirmación de guardado

### Fase 4: Historial y Comparación
- [ ] Crear vista de historial de cálculos
- [ ] Implementar comparación visual de hidrogramas
- [ ] Agregar filtros por fecha, duración, período de retorno

### Fase 5: Testing
- [ ] Probar flujo completo
- [ ] Verificar persistencia
- [ ] Validar visualizaciones

---

## ✅ Tareas Completadas

### 1. Análisis del Frontend Existente

**Estructura de Archivos:**
```
templates/
├── base.html              - Template base con navegación
├── index.html             - Página principal
├── index_simple.html      - Versión simplificada
├── rational.html          - Método Racional ⭐
└── idf.html              - Curvas IDF Uruguay

static/js/
├── app.js                - Utilidades generales (fetchAPI, validators)
├── app_simple.js         - Versión simplificada
├── rational.js           - Lógica del Método Racional ⭐
└── idf.js               - Lógica de curvas IDF
```

**Flujo Actual del Método Racional:**

1. **Formulario de Entrada** (`rational.html`):
   - C (Coeficiente de escorrentía): 0-1
   - I_mmh (Intensidad de lluvia): mm/h
   - A_ha (Área de cuenca): hectáreas
   - description (opcional)

2. **Validación** (`rational.js`):
   - validateForm() verifica rangos
   - Muestra errores en la UI

3. **Cálculo** (`rational.js`):
   - Envía POST a `/api/rational`
   - Payload: { C, I_mmh, A_ha, description }

4. **Respuesta** (de backend):
   ```json
   {
     "Q_ls": 150.5,
     "Q_m3s": 0.1505,
     "Q_m3h": 541.8,
     "inputs": { C, I_mmh, A_ha, A_m2 },
     "warnings": []
   }
   ```

5. **Visualización** (`rational.js`):
   - displayResults() muestra caudales
   - Formatea números con formatNumber()
   - Muestra advertencias si existen

**Problema Actual:**
- No hay persistencia de cálculos
- No se pueden cargar datos de cuencas existentes
- No hay historial de hidrogramas
- Los cálculos se pierden al refrescar la página

---

## 🎯 Plan de Integración Propuesto

### PASO 1: Agregar Sección de Proyecto/Cuenca
**Ubicación:** Antes del formulario de entrada en `rational.html`

**Elementos a agregar:**
```html
<div class="card">
    <h2>Seleccionar Proyecto y Cuenca</h2>

    <!-- Selector de Proyecto -->
    <select id="projectSelect">
        <option value="">-- Nuevo Proyecto --</option>
        <!-- Cargado dinámicamente desde API -->
    </select>

    <!-- Selector de Cuenca -->
    <select id="watershedSelect">
        <option value="">-- Nueva Cuenca --</option>
        <!-- Cargado dinámicamente desde API -->
    </select>

    <!-- Botón para crear nuevo -->
    <button id="createNewProject">Crear Nuevo Proyecto</button>
</div>
```

### PASO 2: JavaScript para Cargar Datos
**Archivo nuevo:** `static/js/database-integration.js`

**Funciones:**
- `loadProjects()` - GET /api/v1/projects
- `loadWatersheds(projectId)` - GET /api/v1/projects/{id}/watersheds
- `populateFormFromWatershed(watershed)` - Llenar formulario con datos de cuenca
- `saveHydrographToDB(data)` - POST /api/v1/design-storms/{id}/hydrographs

### PASO 3: Modificar rational.js
**Cambios:**
1. Al seleccionar cuenca → cargar área automáticamente
2. Al calcular → guardar en BD además de mostrar
3. Agregar botón "Ver Historial"

### PASO 4: Vista de Historial
**Nueva página:** `templates/hydrographs.html`

**Contenido:**
- Lista de hidrogramas guardados
- Filtros por proyecto/cuenca/fecha
- Botón para comparar seleccionados
- Gráficos con Chart.js

---

## 🔧 Detalles Técnicos

### API Endpoints a Usar

**Cargar Proyectos:**
```javascript
GET /api/v1/projects
Response: [
  { id: 1, name: "Sistema Montevideo", ... }
]
```

**Cargar Cuencas:**
```javascript
GET /api/v1/projects/1/watersheds
Response: [
  { id: 1, name: "Arroyo Miguelete", area_hectareas: 250, tc_horas: 1.8, ... }
]
```

**Crear Tormenta de Diseño:**
```javascript
POST /api/v1/watersheds/{watershed_id}/design-storms
Body: {
  name: "Tr=10 Años 2h",
  return_period_years: 10,
  duration_hours: 2.0,
  total_rainfall_mm: 85.3,
  distribution_type: "alternating_block"
}
```

**Guardar Hidrograma:**
```javascript
POST /api/v1/design-storms/{storm_id}/hydrographs
Body: {
  method: "rational",
  peak_discharge_m3s: 0.1505,
  peak_discharge_lps: 150.5,
  time_to_peak_minutes: 45,
  hydrograph_data: [
    { time_min: 0, discharge_m3s: 0, cumulative_volume_m3: 0 },
    { time_min: 5, discharge_m3s: 0.05, cumulative_volume_m3: 15 },
    ...
  ]
}
```

---

## 📦 Archivos a Crear/Modificar

### Nuevos Archivos
- [ ] `static/js/database-integration.js` - Funciones de BD
- [ ] `templates/hydrographs.html` - Vista de historial
- [ ] `static/css/hydrographs.css` - Estilos específicos

### Archivos a Modificar
- [ ] `templates/rational.html` - Agregar selectores
- [ ] `static/js/rational.js` - Integrar guardado automático
- [ ] `static/js/app.js` - Funciones auxiliares
- [ ] `src/main.py` - Agregar ruta para /hydrographs

---

## 📊 Progreso

```
[██████░░░░] 60% - Análisis completado, comenzando implementación...
```

---

## 🔄 Próximos Pasos Inmediatos

1. Crear `database-integration.js` con funciones base
2. Modificar `rational.html` para agregar selectores
3. Modificar `rational.js` para integrar con BD
4. Probar flujo completo

---

**Sesión en progreso** 🚀

_(Este documento se actualiza continuamente)_
