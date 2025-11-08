# 🌊 HidroCalc - Guía de Arquitectura para Claude

> Plataforma web profesional para cálculos hidrológicos e hidráulicos con arquitectura dual:
> calculadoras rápidas + HidroStudio Professional

---

## ⚡ INICIO RÁPIDO DE SESIÓN

**🎯 AL COMENZAR UNA NUEVA SESIÓN, LEE PRIMERO:**

```bash
1. Este archivo (CLAUDE.md) - Arquitectura general
2. context/current_session.md - Estado actual del proyecto ⭐ MUY IMPORTANTE
3. context/next_steps.md - Qué hacer a continuación
```

### **Archivos de Contexto Disponibles:**

- **`context/current_session.md`** ⭐ **LEER PRIMERO**
  - Estado actual del proyecto
  - Última tarea completada
  - Problemas conocidos
  - Siguiente tarea sugerida

- **`context/completed_tasks.md`**
  - Todas las tareas completadas por sesión
  - Historial cronológico

- **`context/next_steps.md`**
  - Tareas pendientes priorizadas
  - Estimaciones de tiempo
  - Ruta recomendada

- **`context/architecture_overview.md`**
  - Overview completo de la arquitectura
  - Stack tecnológico
  - Modelos de BD
  - Endpoints API

- **`work_log/`**
  - Documentación detallada de cada sesión
  - Ver `work_log/00_INDICE_TRABAJO.md`

**💡 TIP:** El sistema de contexto te ahorra tiempo al comenzar. Lee `context/current_session.md` para saber exactamente dónde continuar.

---

## 📐 Visión de Arquitectura

### **Arquitectura Dual**

HidroCalc funciona en **DOS MODOS** distintos:

#### **⚡ Modo 1: Calculadoras Rápidas** (`/calculators/*`)
- **Sin login requerido** - acceso inmediato
- Calculadoras independientes (Método Racional, IDF, Tc, etc.)
- No persiste datos en base de datos
- Exportar resultados a PDF/Excel
- **Público:** Profesionales que necesitan cálculos rápidos

#### **🏢 Modo 2: HidroStudio Professional** (`/studio/*`)
- **Login requerido** - sistema de autenticación completo
- Gestión de proyectos y cuencas hidrológicas
- Base de datos persistente
- Flujo hidrológico completo integrado: Cuenca → IDF → Método → Hidrograma
- Reportes profesionales, gráficos, comparaciones
- Historial de análisis
- **Público:** Profesionales trabajando en proyectos formales

---

## 🏗️ Estructura de Apps Django

```
hidro-calc/
├── hidrocal_project/          # Proyecto Django principal
│   ├── settings.py            # Configuración (REST_FRAMEWORK, JWT, Celery)
│   ├── urls.py                # URLs principales
│   └── wsgi.py/asgi.py
├── core/                      # App principal (modelos de BD)
│   ├── models.py              # Project, Watershed, DesignStorm, Hydrograph, etc.
│   ├── admin.py               # Django Admin configuration
│   └── services.py            # Lógica de negocio
├── api/                       # Django Rest Framework API
│   ├── serializers.py         # Serializers DRF (equiv. Pydantic schemas)
│   ├── views.py               # ViewSets para endpoints
│   └── urls.py                # URLs de la API
├── calculators/               # Calculadoras rápidas (sin BD)
│   ├── views.py               # Vistas para calculadoras
│   ├── forms.py               # Formularios Django
│   └── templates/             # Templates específicos
├── studio/                    # HidroStudio Professional (con BD)
│   ├── views.py               # Dashboard, proyectos, análisis
│   ├── templates/             # Templates del Studio
│   └── services.py            # Lógica de análisis hidrológico
└── ml_analysis/               # Machine Learning (futuro)
    ├── models.py              # Modelos ML
    ├── tasks.py               # Tareas Celery para entrenamiento
    └── services.py            # Servicios de predicción
```

---

## 🎯 Patrones Arquitectónicos Clave

### **1. Modelos de Base de Datos**
- **Ubicación:** `core/models.py`
- **Primary Keys:** Django default `BigAutoField` (integers con auto-incremento)
- **Relaciones:**
  - `Project` 1:N `Watershed`
  - `Watershed` 1:N `DesignStorm`
  - `DesignStorm` 1:N `Hydrograph`
  - `DesignStorm` 1:N `RainfallData`

### **2. Vistas y Lógica de Negocio**
- **Calculadoras Rápidas:** Function-based views en `calculators/views.py`
- **Studio Professional:** Class-based views en `studio/views.py`
- **API REST:** ViewSets en `api/views.py`
- **Servicios:** Lógica de negocio separada en `*/services.py`

### **3. Serializers (Django Rest Framework)**
- **Ubicación:** `api/serializers.py`
- **Equivalente a:** Pydantic schemas de FastAPI
- **Uso:** Validación, serialización JSON, documentación automática

### **4. Templates**
- **Motor:** Django Templates (no Jinja2)
- **Estructura:** Todos deben comenzar con `{% extends "base.html" %}`
- **Ubicación:**
  - Globales: `/templates/`
  - Por app: `{app}/templates/{app}/`

---

## 🛠️ Stack Tecnológico

### **Backend**
- **Framework:** Django 5.2.8
- **API:** Django Rest Framework 3.16.1
- **Base de Datos:** SQLite (desarrollo), PostgreSQL (producción)
- **Cache & Queue:** Redis 7.0.1
- **Task Queue:** Celery 5.5.3
- **Autenticación:** Django Allauth + JWT (djangorestframework-simplejwt)

### **Frontend**
- **CSS Framework:** Tailwind-like custom CSS (`static/css/`)
- **JavaScript:** Vanilla JS + módulos personalizados
- **Gráficos:** Plotly.js 6.4.0, Matplotlib 3.10.7
- **Exportación:** ReportLab (PDF), OpenPyXL (Excel)

### **ML/Analytics** (para futuro)
- **Scikit-learn** 1.7.2
- **Pandas** 2.3.3, **NumPy** 2.3.4
- **Scipy** 1.16.3
- **Celery** para entrenamiento asíncrono

### **Desarrollo**
- **Linter:** Flake8, Black
- **Testing:** pytest-django
- **Servidor:** Whitenoise (static files), Gunicorn (producción)

---

## ⚙️ Configuración Clave

### **Settings Importantes** (`hidrocal_project/settings.py`)

```python
# Apps instaladas
INSTALLED_APPS = [
    'admin_interface',  # Admin mejorado
    'rest_framework',
    'corsheaders',
    'django_filters',
    'celery',
    'core',
    'api',
    'calculators',
    'studio',
]

# Django Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}

# Locale
LANGUAGE_CODE = 'es-uy'  # Español Uruguay
TIME_ZONE = 'America/Montevideo'

# Static Files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

### **Variables de Entorno** (`.env.django`)

```bash
SECRET_KEY=...
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///hidrocal_django.db
CELERY_BROKER_URL=redis://localhost:6379/0
```

---

## 📋 Convenciones de Desarrollo

### **1. Workflow de Desarrollo**

```bash
# Activar entorno virtual
# (Windows)
.venv\Scripts\activate

# Instalar dependencias
pip install -r requirements_django.txt

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver
```

### **2. Crear Nuevas Migraciones**

```bash
# Después de modificar models.py
python manage.py makemigrations
python manage.py migrate
```

### **3. Testing**

```bash
# Ejecutar tests
python -m pytest

# Con coverage
python -m pytest --cov=core --cov=api
```

### **4. Celery (Tareas Asíncronas)**

```bash
# Worker
celery -A hidrocal_project worker -l info

# Beat scheduler
celery -A hidrocal_project beat -l info
```

---

## 🔐 Autenticación y Permisos

### **Flujo de Autenticación**

1. **Calculadoras Rápidas:** Sin autenticación requerida
2. **HidroStudio:**
   - Login con Django Allauth
   - JWT tokens para API
   - Session-based para web views

### **Endpoints de Auth**

```
POST /api/auth/register     # Registro de usuario
POST /api/auth/login        # Login (obtener JWT)
POST /api/auth/refresh      # Refrescar token
POST /api/auth/logout       # Logout
GET  /api/auth/user         # Usuario actual
```

---

## 📊 Modelos de Base de Datos

### **Esquema Principal**

```python
# core/models.py

class Project(models.Model):
    """Proyecto hidrológico"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    created_by = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)

class Watershed(models.Model):
    """Cuenca hidrográfica"""
    project = models.ForeignKey(Project, related_name='watersheds')
    name = models.CharField(max_length=200)
    area_hectareas = models.FloatField()
    tc_horas = models.FloatField()  # Tiempo de concentración
    nc_scs = models.IntegerField(null=True)  # Número de curva SCS
    c_racional = models.FloatField(null=True)  # Coef. escorrentía

class DesignStorm(models.Model):
    """Tormenta de diseño (IDF)"""
    watershed = models.ForeignKey(Watershed, related_name='design_storms')
    name = models.CharField(max_length=200)
    return_period_years = models.IntegerField()
    duration_hours = models.FloatField()
    total_rainfall_mm = models.FloatField()
    distribution_type = models.CharField(max_length=50)

class Hydrograph(models.Model):
    """Hidrograma calculado"""
    design_storm = models.ForeignKey(DesignStorm, related_name='hydrographs')
    method = models.CharField(max_length=50)  # 'rational', 'scs', etc.
    peak_discharge_m3s = models.FloatField()
    peak_discharge_lps = models.FloatField()
    time_to_peak_minutes = models.FloatField()
    hydrograph_data = models.JSONField()  # Serie temporal
```

---

## 🚀 Comandos Útiles de Django

### **Gestión de Base de Datos**

```bash
# Ver SQL de migraciones
python manage.py sqlmigrate core 0001

# Resetear base de datos (CUIDADO!)
python manage.py flush

# Cargar datos de prueba
python manage.py loaddata fixtures/initial_data.json
```

### **Django Shell**

```bash
# Abrir shell interactivo
python manage.py shell

# Crear datos de prueba
from core.models import Project
p = Project.objects.create(name="Test", ...)
```

### **Admin Panel**

```bash
# Acceder a: http://localhost:8000/admin
# Usuario: admin
# Password: admin123
```

---

## 📁 Estructura de Archivos Clave

```
hidro-calc/
├── CLAUDE.md                      # Este archivo
├── README.md                      # Documentación general
├── requirements_django.txt        # Dependencias Django
├── manage.py                      # Django CLI
├── .env.django                    # Variables de entorno
├── hidrocal_project/
│   ├── settings.py               # ⭐ Configuración principal
│   └── urls.py                   # URLs principales
├── core/
│   ├── models.py                 # ⭐ Modelos de BD
│   ├── admin.py                  # Configuración Admin
│   └── migrations/
├── api/
│   ├── serializers.py            # ⭐ Serializers DRF
│   ├── views.py                  # ViewSets API
│   └── urls.py
├── static/
│   ├── css/                      # Estilos
│   ├── js/                       # JavaScript
│   └── img/
├── templates/
│   ├── base.html                 # Template base
│   ├── calculators/              # Templates calculadoras
│   └── studio/                   # Templates Studio
└── work_log/
    ├── 00_INDICE_TRABAJO.md
    ├── 01_IMPLEMENTACION_BASE_DATOS.md
    ├── 02_INTEGRACION_FRONTEND.md
    └── 03_ARQUITECTURA_DUAL_PROPUESTA.md
```

---

## 🎓 Decisiones de Diseño Importantes

### **1. ¿Por qué Django sobre FastAPI?**
- **Visión a largo plazo:** ML, análisis de datos, proyectos complejos
- **Admin Panel:** Gestión de datos sin código adicional
- **ORM Maduro:** Más estable para proyectos grandes
- **Ecosistema:** Miles de paquetes probados
- **Celery Integration:** Procesamiento ML asíncrono

### **2. ¿Por qué Arquitectura Dual?**
- **Dos públicos distintos:** usuarios rápidos vs. profesionales
- **Modelo de negocio:** calculadoras gratis, Studio de pago (futuro)
- **Escalabilidad:** permite monetización sin afectar herramientas gratuitas

### **3. ¿Por qué SQLite en desarrollo?**
- **Simplicidad:** no requiere servicios externos
- **Portabilidad:** base de datos en un archivo
- **Migración fácil:** cambiar a PostgreSQL en producción

---

## 🔄 Migración desde FastAPI

### **Estado Actual:**
- ✅ Proyecto Django configurado
- ✅ Apps creadas (core, api, calculators, studio)
- ✅ Settings completo (REST_FRAMEWORK, JWT, Celery)
- ✅ Base de datos inicializada
- ✅ Superusuario creado
- ✅ Servidor corriendo

### **Pendiente:**
- [ ] Migrar modelos SQLAlchemy → Django ORM
- [ ] Crear serializers DRF (equivalente a Pydantic schemas)
- [ ] Crear ViewSets y URLs para API REST
- [ ] Configurar Django Admin panel
- [ ] Migrar templates Jinja2 → Django templates
- [ ] Migrar JavaScript de integración con BD

### **Backup:**
- `src_fastapi_backup/` contiene todo el código FastAPI original

---

## 📚 Recursos y Referencias

### **Documentación Oficial**
- Django: https://docs.djangoproject.com/
- Django Rest Framework: https://www.django-rest-framework.org/
- Celery: https://docs.celeryproject.org/

### **Libros de Referencia**
- Ven Te Chow - "Applied Hydrology" (1988)
- ASCE Manual of Practice No. 77

### **Métodos Implementados**
- Método Racional (caudales pico)
- Curvas IDF Uruguay (Rodríguez Fontal)
- Tiempo de Concentración (Kirpich, California, etc.)

---

## 🐛 Debugging y Troubleshooting

### **Problemas Comunes**

1. **Error de importación de módulos**
   ```bash
   # Verificar que estás en el entorno virtual
   which python  # debe apuntar a .venv
   ```

2. **Migraciones conflictivas**
   ```bash
   python manage.py migrate --fake-initial
   ```

3. **Static files no se cargan**
   ```bash
   python manage.py collectstatic
   ```

4. **Redis no disponible** (para Celery)
   ```bash
   # Instalar Redis o deshabilitar cache temporalmente
   # En settings.py cambiar CACHES backend a 'dummy'
   ```

---

## 📞 Notas para Claude

### **Al trabajar en este proyecto:**

1. **Siempre usar Django CLI:** `python manage.py <comando>`
2. **Migraciones:** Después de cambiar models.py, siempre hacer `makemigrations` + `migrate`
3. **Testing:** Probar en servidor de desarrollo antes de commits
4. **Documentación:** Actualizar `work_log/` con cambios importantes
5. **Backup:** Nunca eliminar `src_fastapi_backup/`

### **Comandos frecuentes:**

```bash
# Iniciar servidor
python manage.py runserver

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Shell interactivo
python manage.py shell

# Crear superusuario
python manage.py createsuperuser
```

---

## 🧠 Filosofía de Desarrollo

### **Error Handling**

- **Fail Fast:** Fallar rápido para configuraciones críticas (ej: modelos faltantes, DB inaccesible)
- **Log and Continue:** Registrar errores y continuar para características opcionales
- **Graceful Degradation:** Degradación elegante cuando servicios externos no están disponibles
- **User-Friendly Messages:** Mensajes claros al usuario a través de capa de resiliencia

**Ejemplo:**
```python
# Fail Fast - Configuración crítica
if not settings.SECRET_KEY:
    raise ImproperlyConfigured("SECRET_KEY must be set")

# Log and Continue - Característica opcional
try:
    redis_client.ping()
except ConnectionError:
    logger.warning("Redis unavailable, using fallback cache")
    # Continuar con cache dummy
```

---

## 🧪 Testing Guidelines

### **Reglas de Testing**

1. **NO usar mocks para servicios reales**
   - Probar contra base de datos real (SQLite en tests)
   - Probar contra Redis real si está disponible
   - Usar `pytest-django` con fixtures

2. **Tests completos antes de avanzar**
   - No pasar al siguiente test hasta completar el actual
   - Si falla, revisar estructura del test primero
   - No asumir que el código necesita refactoring sin antes validar el test

3. **Tests verbosos para debugging**
   - Mensajes de error claros y descriptivos
   - Imprimir valores intermedios cuando sea útil
   - Usar `pytest -v` para output detallado

4. **Test por cada función**
   - Toda función pública debe tener al menos un test
   - Tests deben cubrir casos normales y edge cases
   - Tests deben revelar fallos, no ocultarlos

### **Ejemplo de Test Correcto**

```python
# tests/test_rational_method.py
import pytest
from calculators.services import calculate_rational_method

def test_rational_method_basic_calculation():
    """Test basic rational method calculation with known values"""
    # Given
    C = 0.65  # Runoff coefficient
    I = 80.0  # Intensity (mm/h)
    A = 5.0   # Area (ha)

    # When
    result = calculate_rational_method(C, I, A)

    # Then
    assert result['Q_lps'] == pytest.approx(72.17, rel=0.01), \
        f"Expected Q_lps ~72.17, got {result['Q_lps']}"
    assert result['Q_m3s'] == pytest.approx(0.0722, rel=0.01), \
        f"Expected Q_m3s ~0.0722, got {result['Q_m3s']}"

    # Verbose output for debugging
    print(f"DEBUG: C={C}, I={I}, A={A}")
    print(f"DEBUG: Result: {result}")
```

---

## 💬 Tone and Behavior

### **Comunicación Esperada**

- **Criticism is Welcome:** Señalar errores, enfoques incorrectos o mejores alternativas
- **Be Skeptical:** Cuestionar decisiones que parezcan subóptimas
- **Be Concise:** Respuestas cortas y directas, sin florituras innecesarias
- **No Flattery:** No dar cumplidos ni validación innecesaria
- **Ask Questions:** Ante duda, preguntar en lugar de asumir

### **Lo que NO hacer:**

❌ "¡Excelente idea! Tu enfoque es brillante..."
❌ "Esto se ve muy bien, pero quizás podrías..."
❌ Dar resúmenes extensos cuando no se pidieron

### **Lo que SÍ hacer:**

✅ "Esto no va a funcionar porque [razón técnica]"
✅ "Hay un mejor enfoque: [alternativa]"
✅ "¿Estás seguro de que querés hacer esto? [consecuencia]"
✅ "Preguntas: 1) ¿Por qué este enfoque? 2) ¿Consideraste X?"

---

## 🚨 ABSOLUTE RULES (Non-Negotiable)

### **1. NO PARTIAL IMPLEMENTATION**

❌ **PROHIBIDO:**
```python
def calculate_hydrograph(storm_data):
    # TODO: Implement actual calculation
    return {"Q": 0}  # Placeholder
```

✅ **CORRECTO:**
```python
def calculate_hydrograph(storm_data):
    """Calculate complete hydrograph using rational method"""
    Q_peak = storm_data['C'] * storm_data['I'] * storm_data['A'] * 2.778
    time_series = generate_time_series(Q_peak, storm_data['tc'])
    return {
        'Q_peak': Q_peak,
        'time_series': time_series,
        'volume_m3': calculate_volume(time_series)
    }
```

---

### **2. NO SIMPLIFICATION**

❌ **PROHIBIDO:**
```python
# This is simplified for now, complete implementation would include:
# - Error handling
# - Validation
# - Multiple methods
```

✅ **CORRECTO:**
Implementar la funcionalidad completa desde el principio, o no implementarla.

---

### **3. NO CODE DUPLICATION**

Antes de escribir una función, **siempre buscar** si ya existe:

```bash
# Buscar funciones existentes
grep -r "def calculate_" core/
grep -r "class.*Service" */services.py
```

❌ **PROHIBIDO:**
```python
# En calculators/services.py
def calculate_area_m2(area_ha):
    return area_ha * 10000

# En studio/services.py
def convert_ha_to_m2(hectares):
    return hectares * 10000  # DUPLICADO!
```

✅ **CORRECTO:**
```python
# En core/utils.py
def hectares_to_m2(hectares):
    """Convert hectares to square meters"""
    return hectares * 10000

# Importar en ambos lugares
from core.utils import hectares_to_m2
```

---

### **4. NO DEAD CODE**

Eliminar código no usado **inmediatamente**:

❌ **PROHIBIDO:**
```python
def old_calculation():  # No usado
    pass

# def deprecated_method():  # Comentado
#     return None
```

✅ **CORRECTO:**
Si no se usa, eliminar del codebase completamente.

---

### **5. IMPLEMENT TEST FOR EVERY FUNCTION**

**Cada función pública = 1 test mínimo**

```python
# calculators/services.py
def calculate_rational_method(C, I, A):
    return C * I * A * 2.778

# tests/test_calculators.py
def test_calculate_rational_method():  # OBLIGATORIO
    assert calculate_rational_method(0.65, 80, 5) == pytest.approx(72.17)
```

---

### **6. NO CHEATER TESTS**

❌ **TEST INÚTIL:**
```python
def test_always_passes():
    assert True  # Esto no prueba nada
```

❌ **TEST ENGAÑOSO:**
```python
def test_calculation():
    result = calculate()
    assert result is not None  # Muy débil
```

✅ **TEST REAL:**
```python
def test_calculation_accuracy():
    """Test rational method against known benchmark values"""
    # Benchmark: Chow's Applied Hydrology, Example 4.3.1
    result = calculate_rational_method(C=0.65, I=80.0, A=5.0)

    expected_Q_lps = 72.17
    assert abs(result['Q_lps'] - expected_Q_lps) < 0.01, \
        f"Calculation error: expected {expected_Q_lps}, got {result['Q_lps']}"
```

---

### **7. NO INCONSISTENT NAMING**

Leer el codebase existente **antes** de nombrar variables:

```bash
# Ver patrones de naming
grep -r "class.*Model" core/models.py
grep -r "def.*_view" */views.py
```

❌ **INCONSISTENTE:**
```python
class project(models.Model):  # lowercase
class WaterShed(models.Model)  # CamelCase inconsistente
class design_storm(models.Model)  # snake_case
```

✅ **CONSISTENTE:**
```python
class Project(models.Model):
class Watershed(models.Model):
class DesignStorm(models.Model):
```

---

### **8. NO OVER-ENGINEERING**

❌ **SOBRE-INGENIERÍA:**
```python
class CalculationStrategyFactory:
    def create_strategy(self, method_type):
        if method_type == "rational":
            return RationalMethodStrategy()
        # ... 10 líneas más de factory pattern
```

✅ **SIMPLE Y FUNCIONAL:**
```python
def calculate_by_method(method, data):
    if method == "rational":
        return calculate_rational(data)
    elif method == "scs":
        return calculate_scs(data)
    raise ValueError(f"Unknown method: {method}")
```

**Regla:** Si una función simple funciona, no crear clases abstractas.

---

### **9. NO MIXED CONCERNS**

❌ **MEZCLADO:**
```python
@api_view(['POST'])
def create_project(request):
    # Validación + lógica de negocio + DB en un solo lugar
    if not request.data.get('name'):
        return Response({'error': 'Name required'})

    project = Project.objects.create(
        name=request.data['name'],
        area=request.data['area'] * 10000  # Conversión aquí?
    )
    # Cálculos complejos en la vista?
    project.calculated_value = complex_calculation()
    project.save()
    return Response({'id': project.id})
```

✅ **SEPARADO:**
```python
# api/serializers.py - Validación
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'area_hectares']

# core/services.py - Lógica de negocio
def create_project(name, area_hectares):
    area_m2 = hectares_to_m2(area_hectares)
    project = Project.objects.create(name=name, area_m2=area_m2)
    project.calculated_value = calculate_project_metrics(project)
    project.save()
    return project

# api/views.py - Vista limpia
@api_view(['POST'])
def create_project_view(request):
    serializer = ProjectSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    project = create_project(**serializer.validated_data)
    return Response(ProjectSerializer(project).data)
```

---

### **10. NO RESOURCE LEAKS**

Siempre cerrar recursos:

❌ **LEAK:**
```python
def process_file(filename):
    f = open(filename)
    data = f.read()
    # f nunca se cierra!
    return process(data)
```

✅ **CORRECTO:**
```python
def process_file(filename):
    with open(filename) as f:
        data = f.read()
    return process(data)
```

**Aplicar a:**
- Conexiones de BD (usar context managers)
- Archivos (usar `with`)
- Timeouts de JavaScript (usar `clearTimeout`)
- Event listeners (siempre `removeEventListener`)

---

### **11. TAMAÑO MÁXIMO DE FUNCIONES Y CLASES**

#### **Funciones**

**Regla estricta:** Ninguna función debe exceder **50 líneas de código**.

❌ **PROHIBIDO - Función de 80 líneas:**
```python
def process_watershed_analysis(watershed_id, storm_params):
    # 15 líneas de validación
    if not watershed_id:
        raise ValueError("Watershed ID required")
    # ... más validación ...

    # 20 líneas de cálculos
    area_m2 = watershed.area_hectares * 10000
    # ... más cálculos ...

    # 15 líneas de procesamiento
    for storm in storms:
        # ... procesamiento complejo ...

    # 15 líneas de guardado
    # ... guardado en BD ...

    # 15 líneas de generación de reportes
    # ... reportes ...

    return results  # Línea 80+
```

✅ **CORRECTO - Dividir en funciones más pequeñas:**
```python
def process_watershed_analysis(watershed_id, storm_params):
    """Main orchestration function - max 20 líneas"""
    watershed = _validate_and_get_watershed(watershed_id)
    calculations = _perform_calculations(watershed, storm_params)
    _save_results(watershed, calculations)
    report = _generate_report(calculations)
    return report

def _validate_and_get_watershed(watershed_id):
    """Validation logic - max 15 líneas"""
    if not watershed_id:
        raise ValueError("Watershed ID required")
    return Watershed.objects.get(id=watershed_id)

def _perform_calculations(watershed, storm_params):
    """Calculation logic - max 30 líneas"""
    # Solo cálculos, nada más
    ...

def _save_results(watershed, calculations):
    """Persistence logic - max 20 líneas"""
    # Solo guardado en BD
    ...

def _generate_report(calculations):
    """Report generation - max 25 líneas"""
    # Solo generación de reportes
    ...
```

**Ventajas:**
- Más fácil de testear (1 test por función pequeña)
- Más fácil de entender y mantener
- Reutilización de componentes
- Debugging simplificado

---

#### **Modelos Django**

**Regla:** Cada modelo debe tener **máximo 15 campos** + métodos helper.

Si un modelo crece demasiado, dividir en modelos relacionados.

❌ **PROHIBIDO - Modelo con 25 campos:**
```python
class Watershed(models.Model):
    # Datos básicos (5 campos)
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    project = models.ForeignKey(Project)
    created_at = models.DateTimeField()

    # Datos físicos (8 campos)
    area_hectares = models.FloatField()
    perimeter_m = models.FloatField()
    slope_percent = models.FloatField()
    max_elevation_m = models.FloatField()
    min_elevation_m = models.FloatField()
    main_channel_length_m = models.FloatField()
    soil_type = models.CharField(max_length=100)
    land_use = models.CharField(max_length=100)

    # Parámetros hidrológicos (7 campos)
    tc_horas = models.FloatField()
    nc_scs = models.IntegerField()
    c_racional = models.FloatField()
    infiltration_rate = models.FloatField()
    storage_coef = models.FloatField()
    lag_time_h = models.FloatField()
    peak_factor = models.FloatField()

    # Metadatos (5 campos)
    data_source = models.CharField(max_length=200)
    accuracy_level = models.CharField(max_length=50)
    last_survey_date = models.DateField()
    survey_method = models.CharField(max_length=100)
    notes = models.TextField()
    # TOTAL: 25 campos! Demasiado
```

✅ **CORRECTO - Dividir en modelos relacionados:**
```python
class Watershed(models.Model):
    """Core watershed data - solo 8 campos"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200)
    area_hectares = models.FloatField()
    perimeter_m = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.area_hectares} ha)"


class WatershedTopography(models.Model):
    """Physical characteristics - 7 campos"""
    watershed = models.OneToOneField(Watershed, on_delete=models.CASCADE, related_name='topography')
    slope_percent = models.FloatField()
    max_elevation_m = models.FloatField()
    min_elevation_m = models.FloatField()
    main_channel_length_m = models.FloatField()
    soil_type = models.CharField(max_length=100)
    land_use = models.CharField(max_length=100)

    def elevation_difference(self):
        return self.max_elevation_m - self.min_elevation_m


class WatershedHydrology(models.Model):
    """Hydrological parameters - 7 campos"""
    watershed = models.OneToOneField(Watershed, on_delete=models.CASCADE, related_name='hydrology')
    tc_horas = models.FloatField(help_text="Time of concentration")
    nc_scs = models.IntegerField(help_text="SCS Curve Number")
    c_racional = models.FloatField(help_text="Rational method coefficient")
    infiltration_rate_mmh = models.FloatField()
    storage_coefficient = models.FloatField()
    lag_time_hours = models.FloatField()

    @property
    def tc_minutes(self):
        return self.tc_horas * 60


class WatershedMetadata(models.Model):
    """Survey and data quality metadata - 5 campos"""
    watershed = models.OneToOneField(Watershed, on_delete=models.CASCADE, related_name='metadata')
    data_source = models.CharField(max_length=200)
    accuracy_level = models.CharField(max_length=50, choices=ACCURACY_CHOICES)
    last_survey_date = models.DateField(null=True, blank=True)
    survey_method = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
```

**Ventajas de dividir modelos:**
- Queries más eficientes (solo cargar lo necesario)
- Separación clara de concerns
- Más fácil de extender (agregar campos a subcategorías)
- Migraciones más manejables

---

#### **Clases (Views, Services, etc.)**

**Regla:** Máximo **10 métodos públicos** por clase.

❌ **PROHIBIDO - Clase con 15 métodos:**
```python
class WatershedService:
    def create_watershed(self): ...
    def update_watershed(self): ...
    def delete_watershed(self): ...
    def get_watershed(self): ...
    def list_watersheds(self): ...
    def calculate_tc_kirpich(self): ...
    def calculate_tc_california(self): ...
    def calculate_tc_bransby(self): ...
    def calculate_cn_weighted(self): ...
    def calculate_rational_q(self): ...
    def calculate_scs_q(self): ...
    def generate_hydrograph(self): ...
    def export_to_pdf(self): ...
    def export_to_excel(self): ...
    def validate_data(self): ...
    # 15 métodos! Demasiado
```

✅ **CORRECTO - Dividir responsabilidades:**
```python
# core/services/watershed_crud.py
class WatershedCRUDService:
    """CRUD operations - 5 métodos"""
    def create(self, data): ...
    def update(self, watershed_id, data): ...
    def delete(self, watershed_id): ...
    def get(self, watershed_id): ...
    def list(self, filters=None): ...


# calculators/services/time_concentration.py
class TimeConcentrationService:
    """Tc calculations - 4 métodos"""
    def calculate_kirpich(self, length_m, slope): ...
    def calculate_california(self, length_m, slope): ...
    def calculate_bransby(self, area_ha, length_m): ...
    def calculate_recommended(self, watershed): ...


# calculators/services/hydrograph.py
class HydrographService:
    """Hydrograph generation - 3 métodos"""
    def generate_rational(self, watershed, storm): ...
    def generate_scs(self, watershed, storm): ...
    def generate_synthetic(self, watershed, storm, method): ...


# studio/services/export.py
class ExportService:
    """Export functionality - 3 métodos"""
    def to_pdf(self, hydrograph): ...
    def to_excel(self, hydrograph): ...
    def to_json(self, hydrograph): ...
```

---

#### **Archivos de Código**

**Regla:** Máximo **500 líneas** por archivo (incluyendo docstrings).

Si un archivo crece más:

✅ **Dividir en múltiples archivos:**

```
# Antes - Un solo archivo grande
core/
  models.py  # 800 líneas ❌

# Después - Dividido por dominio
core/
  models/
    __init__.py
    project.py         # 120 líneas ✅
    watershed.py       # 150 líneas ✅
    design_storm.py    # 130 líneas ✅
    hydrograph.py      # 180 líneas ✅
    rainfall.py        # 100 líneas ✅
```

---

#### **Preferir Class-Based Views (CBV) en Django**

**Regla:** Para vistas con más de **30 líneas**, usar Class-Based Views.

❌ **Function-Based View larga:**
```python
def watershed_detail(request, watershed_id):
    # 10 líneas de permisos y validación
    if not request.user.is_authenticated:
        return redirect('login')
    # ...

    # 15 líneas de lógica GET
    if request.method == 'GET':
        watershed = get_object_or_404(Watershed, id=watershed_id)
        # ... procesamiento ...

    # 20 líneas de lógica POST
    elif request.method == 'POST':
        # ... procesamiento POST ...

    # 10 líneas de renderizado
    context = {...}
    return render(request, 'template.html', context)
    # TOTAL: 55 líneas ❌
```

✅ **Class-Based View limpia:**
```python
class WatershedDetailView(LoginRequiredMixin, DetailView):
    """Display watershed details - 15 líneas"""
    model = Watershed
    template_name = 'studio/watershed_detail.html'
    context_object_name = 'watershed'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['design_storms'] = self.object.design_storms.all()
        context['recent_hydrographs'] = self.object.get_recent_hydrographs()
        return context


class WatershedUpdateView(LoginRequiredMixin, UpdateView):
    """Update watershed - 12 líneas"""
    model = Watershed
    form_class = WatershedForm
    template_name = 'studio/watershed_form.html'
    success_url = reverse_lazy('watershed-list')

    def form_valid(self, form):
        messages.success(self.request, "Watershed updated successfully")
        return super().form_valid(form)
```

**Ventajas de CBV:**
- Menos código duplicado (heredan funcionalidad)
- Mixins para funcionalidad compartida
- Más fácil de testear
- Patrones estandarizados de Django

---

#### **Cuándo usar CBV vs FBV**

**Usar Function-Based Views (FBV) cuando:**
- Vista simple < 20 líneas
- Lógica muy específica que no se reutiliza
- API endpoints simples con DRF

**Usar Class-Based Views (CBV) cuando:**
- CRUD operations (CreateView, UpdateView, DeleteView, ListView)
- Necesitas mixins (LoginRequiredMixin, PermissionRequiredMixin)
- Vista > 30 líneas
- Necesitas reutilizar lógica entre vistas

---

## 📊 Checklist Pre-Commit

Antes de cada commit, verificar:

### **Código Limpio**
- [ ] No hay código duplicado
- [ ] No hay dead code (código comentado o no usado)
- [ ] No hay implementaciones parciales o TODOs
- [ ] Naming consistente con codebase existente
- [ ] No hay simplificaciones ("This is simplified for now...")

### **Separación de Concerns**
- [ ] Validación en serializers/forms, NO en vistas
- [ ] Lógica de negocio en services, NO en vistas
- [ ] Queries de BD en services/models, NO en templates
- [ ] No hay mixed concerns (validación + lógica + DB en un lugar)

### **Tamaños Correctos**
- [ ] Funciones ≤ 50 líneas
- [ ] Modelos ≤ 15 campos (dividir si es necesario)
- [ ] Clases ≤ 10 métodos públicos
- [ ] Archivos ≤ 500 líneas
- [ ] Vistas > 30 líneas usan Class-Based Views

### **Testing**
- [ ] Todos los tests pasan (`pytest`)
- [ ] Tests nuevos para funcionalidad nueva
- [ ] No hay mocks de servicios reales
- [ ] Tests son verbosos y revelan fallos
- [ ] Cada función pública tiene al menos 1 test

### **Recursos**
- [ ] Archivos se cierran correctamente (usar `with`)
- [ ] Conexiones BD usan context managers
- [ ] No hay event listeners sin remover
- [ ] No hay timeouts sin clearTimeout

---

---

## 📝 AL FINALIZAR UNA SESIÓN

**IMPORTANTE:** Actualiza los archivos de contexto antes de terminar:

```bash
1. context/current_session.md
   - Actualizar "Última tarea completada"
   - Actualizar "Estado del proyecto"
   - Agregar problemas encontrados
   - Sugerir siguiente tarea

2. context/completed_tasks.md
   - Agregar tareas completadas de esta sesión
   - Incluir número de sesión y fecha

3. context/next_steps.md
   - Remover tareas completadas
   - Agregar nuevas tareas descubiertas
   - Repriorizar si es necesario

4. work_log/
   - Si la sesión fue significativa, crear nuevo archivo
   - Actualizar work_log/00_INDICE_TRABAJO.md
```

**Esto asegura que la próxima sesión comience con contexto completo.**

---

**Última actualización:** 2025-11-08
**Versión:** 3.0-django
**Estado:** Migración completa a Django, sistema de contexto implementado
