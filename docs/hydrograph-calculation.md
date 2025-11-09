# Hydrograph Calculation System

> Documentación técnica del sistema de cálculo de hidrogramas en HidroCalc

**Última actualización:** 2025-11-09
**Estado:** En desarrollo

---

## 📋 Tabla de Contenidos

1. [Visión General](#visión-general)
2. [Estado Actual](#estado-actual)
3. [Arquitectura Propuesta](#arquitectura-propuesta)
4. [Flujo de Usuario](#flujo-de-usuario)
5. [Implementación Técnica](#implementación-técnica)
6. [Herramienta de Ponderación de Parámetros](#herramienta-de-ponderación-de-parámetros)
7. [Referencias](#referencias)

---

## 🎯 Visión General

El sistema de cálculo de hidrogramas permite a los usuarios convertir tormentas de diseño (DesignStorm) en hidrogramas de escorrentía utilizando diferentes metodologías hidrológicas.

**Objetivo:** Proporcionar una experiencia fluida donde el usuario selecciona una tormenta y método, y el sistema calcula automáticamente el hidrograma resultante.

---

## 📊 Estado Actual

### ✅ Lo que ya existe:

1. **Modelo de datos completo:**
   - `DesignStorm`: Tormentas de diseño con IDF real de Uruguay (Rodríguez Fontal, 1980)
   - `Hydrograph`: Almacenamiento de hidrogramas calculados
   - `Watershed`: Cuencas con parámetros físicos e hidrológicos

2. **API CRUD básico:**
   - `POST /api/hydrographs/` - Crear hidrograma (requiere datos completos ya calculados)
   - `GET /api/hydrographs/` - Listar hidrogramas
   - `GET /api/hydrographs/{id}/` - Detalle de hidrograma
   - `GET /api/hydrographs/compare/?ids=1,2,3` - Comparar múltiples

3. **Servicios de cálculo existentes:**
   - `calculators/services/rational.py` - Método Racional
   - `calculators/services/idf.py` - Curvas IDF de Uruguay
   - `calculators/services/runoff_coefficient.py` - Coeficiente de escorrentía

4. **Dashboard HidroStudio:**
   - Visualización de hidrogramas con Plotly.js
   - Comparación de metodologías
   - Integración con proyectos y cuencas

### ❌ Lo que falta:

1. **Servicio automatizado de cálculo:**
   - No existe un servicio que calcule hidrogramas automáticamente a partir de DesignStorm
   - El endpoint actual requiere enviar TODO el hidrograma ya calculado (no práctico)

2. **Generación de hietogramas:**
   - Falta implementar distribución temporal de lluvia (Alternating Block, Chicago, etc.)
   - DesignStorm tiene `distribution_type` pero no se usa

3. **Métodos de hidrogramas:**
   - Método Racional: Solo calcula caudal pico, falta hidrograma completo
   - SCS Unit Hydrograph: No implementado
   - Synthetic Unit Hydrograph: No implementado

4. **Herramienta de ponderación:**
   - No existe forma de ponderar C (coeficiente escorrentía) y NC (número de curva) por área de subcuencas
   - Usuario debe calcular manualmente parámetros ponderados

---

## 🏗️ Arquitectura Propuesta

```
┌─────────────────┐
│  DesignStorm    │ (Tormenta de diseño con IDF)
└────────┬────────┘
         │
         ↓
┌─────────────────────────────────────────────┐
│  HydrographCalculatorService                │
│  ├─ generate_hyetograph()                   │ → Distribución temporal de lluvia
│  ├─ calculate_rainfall_excess()             │ → Pérdidas por infiltración
│  ├─ calculate_hydrograph_rational()         │ → Hidrograma método racional
│  ├─ calculate_hydrograph_scs()              │ → SCS Unit Hydrograph
│  └─ calculate_hydrograph_synthetic()        │ → Sintético triangular/otros
└─────────────────┬───────────────────────────┘
                  │
                  ↓
         ┌────────────────┐
         │   Hydrograph   │ (Hidrograma calculado + metadata)
         └────────────────┘
```

### Componentes:

1. **HyetographGenerator** (`core/services/hyetograph.py`):
   ```python
   def generate_hyetograph(
       total_rainfall_mm: float,
       duration_hours: float,
       time_step_minutes: float,
       method: str = 'alternating_block'
   ) -> List[Dict]:
       """Genera distribución temporal de lluvia"""
   ```

2. **RainfallExcessCalculator** (`core/services/rainfall_excess.py`):
   ```python
   def calculate_rainfall_excess(
       rainfall_series: List[float],
       C: float = None,
       NC: int = None,
       method: str = 'rational'
   ) -> Dict:
       """Calcula lluvia efectiva (escorrentía) con pérdidas por infiltración"""
   ```

3. **HydrographCalculator** (`core/services/hydrograph_calculator.py`):
   ```python
   def calculate_hydrograph(
       design_storm: DesignStorm,
       method: str = 'rational',
       custom_params: Dict = None
   ) -> Hydrograph:
       """
       Función principal que orquesta:
       1. Generar hietograma
       2. Calcular lluvia efectiva
       3. Calcular hidrograma según método
       4. Crear y guardar objeto Hydrograph
       """
   ```

4. **API Endpoint Mejorado**:
   ```python
   # api/views.py
   @action(detail=False, methods=['post'])
   def calculate(self, request):
       """
       POST /api/hydrographs/calculate/

       Body:
       {
         "design_storm_id": 1,
         "method": "rational",
         "name": "Optional custom name",
         "custom_params": {
           "C": 0.75,  # Override watershed C
           "NC": 80    # Override watershed NC
         }
       }

       Returns: Hydrograph (201 Created)
       """
   ```

---

## 👤 Flujo de Usuario

### Caso de uso: Generar hidrograma para una tormenta

**Escenario:** Ingeniero quiere analizar el caudal de diseño para Tr=25 años, D=1h

```
1. Login → /accounts/login/
   ├─ Email: admin@hidrocal.com
   └─ Password: admin123

2. Dashboard → /studio/
   ├─ Seleccionar proyecto: "Sistema de Drenaje Montevideo"
   ├─ Seleccionar cuenca: "Arroyo Miguelete Alto"
   └─ Ver tormentas de diseño disponibles

3. Seleccionar tormenta:
   └─ Tr=25a, D=1h (lluvia total: ~52mm)

4. Calcular hidrograma:
   ├─ Método: Racional / SCS / Sintético
   ├─ Revisar parámetros:
   │  ├─ C = 0.65 (cuenca)
   │  ├─ A = 250 ha
   │  └─ Tc = 1.8h
   └─ Click "Calcular Hidrograma"

5. API Request (automático):
   POST /api/hydrographs/calculate/
   {
     "design_storm_id": 12,
     "method": "rational",
     "name": "Hidrograma Racional - Tr25-1h"
   }

6. Sistema calcula:
   ├─ Hietograma (Alternating Block, Δt=5min)
   ├─ Lluvia efectiva (C × P)
   ├─ Hidrograma (método seleccionado)
   └─ Guarda en BD

7. Visualización:
   ├─ Gráfico de hidrograma (Plotly.js)
   ├─ Estadísticas: Qpico, Volumen, Tp
   └─ Opción de comparar con otros métodos
```

---

## 🔧 Implementación Técnica

### Fase 1: Generación de Hietogramas

**Archivo:** `core/services/hyetograph.py`

```python
def generate_alternating_block(
    total_rainfall_mm: float,
    duration_hours: float,
    time_step_minutes: float = 5
) -> Dict:
    """
    Método de bloques alternados para distribución temporal.

    Proceso:
    1. Dividir duración en intervalos de Δt
    2. Calcular intensidad para cada duración usando IDF
    3. Calcular incrementos de lluvia
    4. Ordenar en patrón alternado (pico al centro)

    Returns:
    {
      'time_steps': [0, 5, 10, 15, ...],  # minutos
      'rainfall_mm': [2.1, 5.3, 8.7, ...],  # mm en cada Δt
      'intensity_mmh': [25.2, 63.6, 104.4, ...],  # mm/h
      'cumulative_mm': [2.1, 7.4, 16.1, ...]
    }
    """
```

**Referencias:**
- Chow, V.T. (1988). Applied Hydrology. McGraw-Hill.
- SCS (1986). Urban Hydrology for Small Watersheds. TR-55.

### Fase 2: Cálculo de Lluvia Efectiva

**Archivo:** `core/services/rainfall_excess.py`

```python
def calculate_rainfall_excess_rational(
    rainfall_series: List[float],
    C: float,
    area_ha: float
) -> Dict:
    """
    Método Racional: Pe = C × P

    Returns:
    {
      'excess_series': [...],  # mm efectivos por Δt
      'infiltration_series': [...],  # mm infiltrados
      'total_excess_mm': float,
      'total_infiltration_mm': float,
      'runoff_ratio': float  # C efectivo
    }
    """

def calculate_rainfall_excess_scs(
    rainfall_series: List[float],
    CN: int,
    antecedent_condition: str = 'AMC-II'
) -> Dict:
    """
    Método SCS Curve Number:
    Pe = (P - 0.2S)² / (P + 0.8S)
    donde S = (25400 / CN) - 254

    Returns: Similar estructura que rational
    """
```

### Fase 3: Cálculo de Hidrogramas

**Archivo:** `core/services/hydrograph_calculator.py`

#### 3.1 Método Racional Extendido

```python
def calculate_hydrograph_rational(
    rainfall_excess: Dict,
    area_ha: float,
    tc_hours: float,
    time_step_minutes: float = 5
) -> Dict:
    """
    Hidrograma Racional con distribución temporal.

    Asume:
    - Hidrograma triangular
    - Tp = Tc
    - Tiempo de recesión = 1.67 × Tc (regla empírica)
    - Qpico = C × I × A × 2.778

    Returns:
    {
      'time_min': [0, 5, 10, ...],
      'discharge_m3s': [0, 15.2, 45.6, ...],
      'cumulative_volume_m3': [0, 4560, ...],
      'peak_discharge_m3s': float,
      'time_to_peak_min': float,
      'total_volume_m3': float
    }
    """
```

#### 3.2 SCS Unit Hydrograph (Futuro)

```python
def calculate_hydrograph_scs(
    rainfall_excess: Dict,
    area_km2: float,
    tc_hours: float,
    time_step_minutes: float = 5
) -> Dict:
    """
    SCS Dimensionless Unit Hydrograph.

    Basado en:
    - Qp = 2.08 × A / Tp (cfs)
    - Tp = 0.6 × Tc
    - Hidrograma sintético adimensional de SCS
    """
```

#### 3.3 Orquestador Principal

```python
def calculate_hydrograph(
    design_storm: DesignStorm,
    method: str = 'rational',
    custom_params: Dict = None,
    save_to_db: bool = True
) -> Hydrograph:
    """
    Función principal de cálculo.

    Flujo:
    1. Validar inputs
    2. Obtener parámetros de cuenca (o custom_params)
    3. Generar hietograma
    4. Calcular lluvia efectiva
    5. Calcular hidrograma según método
    6. Crear objeto Hydrograph
    7. Guardar en BD (opcional)
    8. Retornar

    Args:
        design_storm: Tormenta de diseño
        method: 'rational' | 'scs_unit_hydrograph' | 'synth_unit_hydro'
        custom_params: Override parámetros de cuenca
        save_to_db: Si False, solo retorna objeto sin guardar

    Returns:
        Hydrograph object (guardado o no)

    Raises:
        ValueError: Parámetros inválidos
        CalculationError: Error en cálculos
    """
```

### Fase 4: API Endpoint

**Archivo:** `api/views.py`

```python
class HydrographViewSet(viewsets.ModelViewSet):
    # ... existing methods ...

    @action(detail=False, methods=['post'])
    def calculate(self, request):
        """
        Calcular hidrograma automáticamente.

        POST /api/hydrographs/calculate/

        Body:
        {
          "design_storm_id": 1,
          "method": "rational",
          "name": "Optional custom name",
          "custom_params": {
            "C": 0.75,
            "NC": 80,
            "time_step_minutes": 5
          }
        }

        Returns:
        201 Created - Hydrograph object completo
        400 Bad Request - Parámetros inválidos
        404 Not Found - DesignStorm no existe
        500 Error - Error en cálculo
        """
        from core.services.hydrograph_calculator import calculate_hydrograph

        # Validar request
        design_storm_id = request.data.get('design_storm_id')
        method = request.data.get('method', 'rational')
        name = request.data.get('name')
        custom_params = request.data.get('custom_params', {})

        # Obtener DesignStorm
        try:
            design_storm = DesignStorm.objects.get(id=design_storm_id)
        except DesignStorm.DoesNotExist:
            return Response(
                {'error': 'DesignStorm not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Calcular hidrograma
        try:
            hydrograph = calculate_hydrograph(
                design_storm=design_storm,
                method=method,
                custom_params=custom_params,
                save_to_db=True
            )

            # Aplicar nombre custom si se proveyó
            if name:
                hydrograph.name = name
                hydrograph.save()

            # Serializar y retornar
            serializer = HydrographSerializer(hydrograph)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Calculation error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
```

---

## 🧮 Herramienta de Ponderación de Parámetros

### Problema:

Una cuenca puede tener múltiples subcuencas con diferentes usos de suelo:
- Subcuenca A: 100 ha, C=0.9 (urbano denso)
- Subcuenca B: 80 ha, C=0.5 (parques)
- Subcuenca C: 70 ha, C=0.7 (residencial)

**¿Qué C usar para la cuenca completa?**

### Solución: Ponderación por área

**Archivo:** `core/services/parameter_weighting.py`

```python
def calculate_weighted_C(subcatchments: List[Dict]) -> Dict:
    """
    Calcula C ponderado por área.

    Formula: C_ponderado = Σ(Ci × Ai) / Σ(Ai)

    Args:
        subcatchments: [
            {'area_ha': 100, 'C': 0.9, 'description': 'Urbano'},
            {'area_ha': 80, 'C': 0.5, 'description': 'Parques'},
            ...
        ]

    Returns:
    {
      'weighted_C': 0.718,
      'total_area_ha': 250,
      'breakdown': [
        {'area_ha': 100, 'C': 0.9, 'weight': 0.40, 'contribution': 0.36},
        ...
      ],
      'dominant_category': 'Urbano (40%)'
    }
    """

def calculate_weighted_CN(subcatchments: List[Dict]) -> Dict:
    """
    Calcula CN ponderado por área.

    Formula: CN_ponderado = Σ(CNi × Ai) / Σ(Ai)

    Similar estructura que calculate_weighted_C
    """
```

### API Endpoint:

```python
# api/views.py
@api_view(['POST'])
def calculate_weighted_parameters(request):
    """
    POST /api/watersheds/calculate-weighted-parameters/

    Body:
    {
      "subcatchments": [
        {"area_ha": 100, "C": 0.9, "CN": 92, "description": "Urbano"},
        {"area_ha": 80, "C": 0.5, "CN": 68, "description": "Parques"},
        {"area_ha": 70, "C": 0.7, "CN": 80, "description": "Residencial"}
      ]
    }

    Returns:
    {
      "weighted_C": 0.718,
      "weighted_CN": 81.2,
      "total_area_ha": 250,
      "breakdown_C": [...],
      "breakdown_CN": [...]
    }
    """
```

### UI Integration:

**Pantalla en HidroStudio:**
```
┌─────────────────────────────────────────┐
│  Calcular Parámetros Ponderados        │
│                                         │
│  Subcuenca 1:                           │
│  ├─ Área: [100] ha                      │
│  ├─ C:    [0.9]                         │
│  ├─ CN:   [92]                          │
│  └─ Desc: [Urbano denso]                │
│                                         │
│  Subcuenca 2:                           │
│  ├─ Área: [80] ha                       │
│  ├─ C:    [0.5]                         │
│  ├─ CN:   [68]                          │
│  └─ Desc: [Parques]                     │
│                                         │
│  [+ Agregar Subcuenca]                  │
│                                         │
│  ────────────────────────────────       │
│  Resultados:                            │
│  ├─ C ponderado:  0.718                 │
│  ├─ CN ponderado: 81.2                  │
│  └─ Área total:   250 ha                │
│                                         │
│  [Aplicar a Cuenca]  [Cancelar]         │
└─────────────────────────────────────────┘
```

---

## 📚 Referencias

### Libros:
- Chow, V.T., Maidment, D.R., Mays, L.W. (1988). **Applied Hydrology**. McGraw-Hill.
- SCS (1986). **Urban Hydrology for Small Watersheds**. TR-55.
- Témez, J.R. (1978). **Cálculo Hidrometeorológico de Caudales Máximos**.

### Papers:
- Rodríguez Fontal (1980). **Curvas IDF de Uruguay**.
- Genta et al. (1998). **Actualización de curvas IDF**.

### Códigos existentes:
- `calculators/services/rational.py` - Método Racional
- `calculators/services/idf.py` - Curvas IDF Uruguay
- `calculators/services/runoff_coefficient.py` - Tablas de C

---

## 🚀 Plan de Implementación

### Sprint 1: Hietogramas y Lluvia Efectiva (2-3 días)
- [ ] Crear `core/services/hyetograph.py`
- [ ] Implementar Alternating Block Method
- [ ] Crear `core/services/rainfall_excess.py`
- [ ] Implementar cálculo con C (Racional)
- [ ] Tests unitarios

### Sprint 2: Hidrograma Racional (2-3 días)
- [ ] Crear `core/services/hydrograph_calculator.py`
- [ ] Implementar hidrograma triangular (Racional extendido)
- [ ] Integrar hietograma + lluvia efectiva + hidrograma
- [ ] Tests de integración

### Sprint 3: API Endpoint (1-2 días)
- [ ] Crear endpoint `POST /api/hydrographs/calculate/`
- [ ] Serializers de request/response
- [ ] Manejo de errores
- [ ] Documentación Swagger

### Sprint 4: Herramienta de Ponderación (2-3 días)
- [ ] Crear `core/services/parameter_weighting.py`
- [ ] Endpoint `POST /api/watersheds/calculate-weighted-parameters/`
- [ ] UI en HidroStudio dashboard
- [ ] Tests

### Sprint 5: Testing End-to-End (1 día)
- [ ] Flujo completo: Login → Seleccionar tormenta → Calcular → Visualizar
- [ ] Comparación de métodos
- [ ] Performance testing
- [ ] Documentación de usuario

---

**Total estimado:** 8-12 días de desarrollo

**Prioridad actual:** Sprint 1 (Hietogramas) → Sprint 2 (Hidrograma Racional)
