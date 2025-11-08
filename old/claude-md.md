# Instrucciones para Claude CLI - HidroCalc

## 🎯 Contexto del Proyecto

**HidroCalc** es una aplicación web para cálculos de hidrología e hidráulica, desarrollada para ingenieros civiles especializados en diseño de sistemas pluviales.

### Información del Desarrollador
- **Especialidad**: Ingeniero Civil - Cálculo de Pluviales
- **Ubicación del proyecto**: `C:\myprojects\hidro-calc`
- **Conocimientos**: Hidrología, hidráulica, diseño de alcantarillado

---

## 🛠️ Stack Tecnológico

### Backend
- **Python 3.14**
- **FastAPI** - Framework web (simple, rápido, documentación automática)
- **Uvicorn** - Servidor ASGI
- **Pydantic** - Validación de datos

### Cálculos Científicos
- **NumPy** - Operaciones numéricas
- **SciPy** - Algoritmos científicos (interpolación, integración, optimización)
- **Pandas** - Manejo de datos tabulares
- **Matplotlib** - Generación de gráficos

### Frontend
- **HTML5 + CSS3** - Interfaz web
- **JavaScript (Vanilla)** - Interactividad
- **Jinja2** - Templates server-side

### Base de Datos (Futuro)
- **SQLite** para desarrollo
- **PostgreSQL** para producción (opcional)

---

## 📁 Estructura del Proyecto

```
hidro-calc/
├── src/
│   ├── __init__.py
│   ├── main.py                    # Servidor FastAPI principal
│   ├── models/                    # Modelos Pydantic
│   │   ├── __init__.py
│   │   ├── hydrology.py          # Modelos hidrológicos
│   │   └── hydraulics.py         # Modelos hidráulicos
│   ├── core/                      # Lógica de cálculo (puro Python)
│   │   ├── __init__.py
│   │   ├── rational_method.py    # Método racional Q=CIA
│   │   ├── storms.py             # Tormentas de diseño
│   │   ├── idf_curves.py         # Curvas IDF
│   │   ├── unit_hydrograph.py    # Hidrograma unitario
│   │   ├── gvf.py                # Flujo gradualmente variado
│   │   ├── channels.py           # Diseño de canales
│   │   └── structures.py         # Obras hidráulicas
│   ├── api/                       # Endpoints FastAPI
│   │   ├── __init__.py
│   │   ├── routes.py             # Rutas principales
│   │   └── dependencies.py       # Dependencias comunes
│   └── utils/                     # Utilidades
│       ├── __init__.py
│       ├── conversions.py        # Conversión de unidades
│       ├── validators.py         # Validaciones custom
│       └── constants.py          # Constantes (gravedad, etc)
├── templates/                     # HTML templates
│   ├── base.html                 # Template base
│   ├── index.html                # Página principal
│   ├── rational.html             # Método racional
│   └── storms.html               # Tormentas de diseño
├── static/                        # Archivos estáticos
│   ├── css/
│   │   ├── style.css            # Estilos principales
│   │   └── forms.css            # Estilos de formularios
│   ├── js/
│   │   ├── app.js               # JavaScript principal
│   │   ├── charts.js            # Gráficos
│   │   └── validators.js        # Validaciones frontend
│   └── img/                      # Imágenes
├── data/                          # Datos de referencia
│   ├── idf_curves.json           # Curvas IDF por región
│   ├── roughness.json            # Coeficientes de rugosidad
│   └── cn_values.json            # Números de curva SCS
├── tests/                         # Tests unitarios
│   ├── test_rational.py
│   ├── test_storms.py
│   └── test_gvf.py
├── docs/                          # Documentación
│   ├── API.md
│   ├── FORMULAS.md
│   └── EJEMPLOS.md
├── venv/                          # Entorno virtual (no subir a Git)
├── .gitignore
├── requirements.txt
├── CLAUDE.md                      # Este archivo
├── README.md
└── DESARROLLO.md
```

---

## 🎨 Principios de Diseño

### Para el Código
1. **Separación de responsabilidades**: Core (cálculos puros) separado de API
2. **Validación estricta**: Usar Pydantic en todos los inputs
3. **Documentación**: Docstrings en español con fórmulas y referencias
4. **Testing**: Cada función de cálculo debe tener tests
5. **Unidades claras**: Siempre especificar unidades en nombres de variables

### Para la Interfaz
1. **Simplicidad**: Formularios claros, sin decoraciones excesivas
2. **Profesional**: Colores sobrios (azul tema agua: #2563eb)
3. **Feedback inmediato**: Validación en tiempo real
4. **Responsivo**: Funcionar en escritorio y tablet
5. **Accesibilidad**: Labels claros, errores descriptivos

---

## 📐 Convenciones de Código

### Nombres de Variables
```python
# Siempre incluir unidades en el nombre
Q_ls = 150.5           # Caudal en litros por segundo
I_mmh = 80.0           # Intensidad en mm/h
A_ha = 5.2             # Área en hectáreas
L_m = 250.0            # Longitud en metros
n_manning = 0.013      # Adimensional

# Para funciones
def calculate_flow_ls(C: float, I_mmh: float, A_ha: float) -> float:
    """Calcula caudal en L/s usando método racional"""
    pass
```

### Documentación
```python
def calculate_rational_flow(C: float, I_mmh: float, A_ha: float) -> float:
    """
    Calcula el caudal de diseño usando el Método Racional.
    
    Fórmula: Q = C × I × A / 360
    
    Args:
        C: Coeficiente de escorrentía (adimensional, 0-1)
        I_mmh: Intensidad de lluvia en mm/h
        A_ha: Área de la cuenca en hectáreas
    
    Returns:
        float: Caudal de diseño en L/s
    
    Raises:
        ValueError: Si los parámetros están fuera de rango válido
    
    Referencias:
        - Ven Te Chow, "Applied Hydrology" (1988)
        - ASCE Manual of Practice No. 77
    
    Ejemplo:
        >>> calculate_rational_flow(C=0.65, I_mmh=80, A_ha=5)
        722.22
    """
    pass
```

---

## 🧮 Módulos a Desarrollar (Prioridad)

### FASE 1: MVP - Método Racional ✅
- [x] Servidor FastAPI básico
- [x] Cálculo Q = C × I × A
- [x] Interfaz con formulario
- [x] Validaciones

### FASE 2: Tormentas de Diseño 🔄
- [ ] Curvas IDF interactivas
- [ ] Método de bloques alternos
- [ ] Hietogramas de diseño
- [ ] Distribución temporal SCS

### FASE 3: Hidrología Avanzada
- [ ] Hidrograma Unitario SCS
- [ ] Método del Número de Curva
- [ ] Tiempos de concentración (múltiples métodos)
- [ ] Routing de hidrogramas

### FASE 4: Flujo Gradualmente Variado
- [ ] Perfiles de flujo (M1, M2, S1, etc)
- [ ] Método de paso estándar
- [ ] Profundidad normal y crítica
- [ ] Visualización de perfiles

### FASE 5: Diseño de Canales
- [ ] Flujo uniforme (Manning)
- [ ] Secciones óptimas
- [ ] Energía específica
- [ ] Resalto hidráulico

### FASE 6: Obras de Drenaje
- [ ] Diseño de alcantarillas
- [ ] Vertederos (múltiples geometrías)
- [ ] Orificios
- [ ] Transiciones

---

## 🎯 Instrucciones para Tareas Comunes

### Crear un Nuevo Módulo de Cálculo

```
Necesito crear un módulo para [NOMBRE DEL CÁLCULO]

Contexto:
- Fórmulas: [FÓRMULAS PRINCIPALES]
- Referencias: [LIBRO O NORMA]
- Inputs: [PARÁMETROS DE ENTRADA]
- Outputs: [RESULTADOS ESPERADOS]

Crear:
1. src/core/[nombre].py con funciones de cálculo
2. src/models/[nombre].py con modelos Pydantic
3. src/api/routes.py agregar endpoint POST /api/[nombre]
4. templates/[nombre].html con formulario
5. static/js/[nombre].js para frontend
6. tests/test_[nombre].py con casos de prueba

Incluir:
- Validaciones estrictas
- Conversiones de unidades
- Manejo de errores descriptivos
- Documentación con fórmulas
```

### Agregar Visualización con Gráficos

```
Necesito agregar un gráfico para [TIPO DE DATO]

Requisitos:
- Tipo de gráfico: [línea/barras/área/etc]
- Datos del eje X: [descripción]
- Datos del eje Y: [descripción]
- Formato: [preferencias]

Usar:
- Matplotlib en backend para generar PNG
- O Chart.js en frontend para interactividad

Crear endpoint /api/plot/[nombre] que retorne imagen o datos JSON
```

### Agregar Curvas de Referencia

```
Necesito agregar datos de [CURVAS IDF / RUGOSIDAD / CN / ETC]

Formato:
- Archivo: data/[nombre].json
- Estructura: [describir estructura JSON]
- Fuente: [referencia bibliográfica]

Crear función en src/utils/ para leer e interpolar datos
```

---

## ⚠️ Validaciones Importantes

### Siempre Validar:
1. **Rangos físicos**: No hay caudales negativos, áreas negativas, etc
2. **Unidades**: Verificar conversiones correctas
3. **Valores extremos**: Alertar si valores parecen anormalmente altos/bajos
4. **Inputs requeridos**: Todos los campos necesarios deben estar presentes

### Ejemplo de Validación:
```python
if C < 0 or C > 1:
    raise ValueError("El coeficiente C debe estar entre 0 y 1")

if I_mmh > 500:
    warnings.warn("Intensidad muy alta (>500 mm/h). Verifica el valor.")

if A_ha > 10000:
    warnings.warn("Área muy grande (>10,000 ha). Considera subcuencas.")
```

---

## 🔧 Comandos Útiles

### Desarrollo
```bash
# Activar entorno virtual
.\venv\Scripts\activate

# Ejecutar servidor
python src/main.py

# Ejecutar con reload automático
uvicorn src.main:app --reload --port 8000

# Ejecutar tests
pytest tests/ -v

# Ver documentación API
# Abrir: http://localhost:8000/docs
```

### Manejo de Dependencias
```bash
# Instalar nueva dependencia
pip install nombre-paquete
pip freeze > requirements.txt

# Instalar desde requirements
pip install -r requirements.txt
```

---

## 📚 Referencias Técnicas

### Libros de Referencia
1. **Ven Te Chow** - "Applied Hydrology" (1988)
2. **Ven Te Chow** - "Open Channel Hydraulics" (1959)
3. **USDA** - "Urban Hydrology for Small Watersheds" (TR-55)
4. **HEC-HMS** - Reference Manual (US Army Corps)

### Normas y Estándares
- ASCE Manual of Practice No. 77
- Manual de Carreteras (volumen de drenaje)
- Normas locales de Uruguay (si aplica)

### Datos de Referencia Necesarios
- Curvas IDF de Montevideo y otras ciudades
- Coeficientes de rugosidad de Manning
- Valores de CN para diferentes tipos de suelo
- Coeficientes de escorrentía por tipo de superficie

---

## 🚀 Estilo de Trabajo con Claude

### Al Solicitar Código
1. **Contexto claro**: Siempre mencionar el módulo y su propósito
2. **Fórmulas explícitas**: Incluir las ecuaciones que se deben implementar
3. **Casos de prueba**: Dar ejemplos de inputs y outputs esperados
4. **Referencias**: Citar fuente de las fórmulas (libro, norma, página)

### Al Reportar Bugs
1. **Reproducir**: Pasos exactos para reproducir el error
2. **Inputs**: Valores que causaron el problema
3. **Output esperado**: Qué debería haber pasado
4. **Output actual**: Qué pasó realmente

### Al Pedir Mejoras
1. **Objetivo**: Qué se quiere lograr
2. **Restricciones**: Limitaciones o consideraciones
3. **Prioridad**: Crítico / Importante / Nice-to-have

---

## ✅ Checklist de Calidad

Antes de considerar un módulo completo:

- [ ] Código funciona sin errores
- [ ] Validaciones implementadas
- [ ] Documentación con docstrings
- [ ] Tests unitarios creados
- [ ] Interfaz funcional y responsiva
- [ ] Manejo de errores con mensajes claros
- [ ] Conversiones de unidades verificadas
- [ ] Resultados validados con cálculos manuales

---

## 🎓 Notas para Claude

- El usuario es ingeniero civil, no programador profesional
- Priorizar claridad sobre optimización prematura
- Incluir comentarios explicativos en cálculos complejos
- Sugerir mejores prácticas pero mantener código accesible
- Cuando haya dudas técnicas de hidrología, preguntar al usuario

---

**Última actualización**: Noviembre 2025