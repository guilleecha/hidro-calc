# 🚨 Error Handling Philosophy - HidroCalc

Estrategia de manejo de errores para robustez y resiliencia.

---

## 🎯 Filosofía General

### **Error Handling Approach**

- **Fail Fast:** Fallar rápido para configuraciones críticas
- **Log and Continue:** Registrar errores y continuar para features opcionales
- **Graceful Degradation:** Degradación elegante cuando servicios externos no disponibles
- **User-Friendly Messages:** Mensajes claros al usuario a través de capa de resiliencia

---

## 🔴 Fail Fast (Configuración Crítica)

**Usar cuando:**
- Configuración de base de datos incorrecta
- SECRET_KEY faltante
- Modelos requeridos no disponibles

**Ejemplo:**
```python
# settings.py
if not SECRET_KEY:
    raise ImproperlyConfigured("SECRET_KEY must be set in environment")

# core/models.py
from django.core.exceptions import ImproperlyConfigured

class Project(models.Model):
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False  # REQUERIDO - fail fast si falta
    )
```

---

## 🟡 Log and Continue (Features Opcionales)

**Usar cuando:**
- Redis no disponible
- Celery worker offline
- Servicios de terceros temporalmente caídos

**Ejemplo:**
```python
import logging

logger = logging.getLogger(__name__)

# Cache opcional
try:
    redis_client.ping()
    cache_available = True
except ConnectionError:
    logger.warning("Redis unavailable, using fallback cache")
    cache_available = False
    # Continuar con cache dummy

# En código
if cache_available:
    result = cache.get(key)
else:
    result = None  # Calcular directamente
```

---

## 🟢 Graceful Degradation

**Usar cuando:**
- Servicios externos no críticos fallan
- Features de "nice-to-have" no disponibles

**Ejemplo:**
```python
# Export to PDF
try:
    from reportlab.pdfgen import canvas
    PDF_AVAILABLE = True
except ImportError:
    logger.warning("ReportLab not installed, PDF export disabled")
    PDF_AVAILABLE = False

# En vista
def export_report(request, report_id):
    if not PDF_AVAILABLE:
        messages.warning(request, "PDF export not available")
        return redirect('report-detail', pk=report_id)

    # Generar PDF...
```

---

## 💬 User-Friendly Messages

**Regla:** Nunca mostrar stack traces directamente al usuario.

❌ **MAL:**
```python
@api_view(['POST'])
def create_project(request):
    project = Project.objects.create(**request.data)  # Exception!
    return Response({'id': project.id})
```

✅ **BIEN:**
```python
from rest_framework.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
def create_project(request):
    try:
        serializer = ProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = serializer.save()
        return Response(ProjectSerializer(project).data, status=201)

    except ValidationError as e:
        # DRF maneja automáticamente con mensajes claros
        raise

    except Exception as e:
        # Log detallado para developers
        logger.error(
            f"Error creating project: {str(e)}",
            exc_info=True,
            extra={'user': request.user.id, 'data': request.data}
        )

        # Mensaje genérico para usuarios
        return Response(
            {'error': 'Unable to create project. Please try again.'},
            status=500
        )
```

---

## 📊 Niveles de Error

### **1. Critical (500) - Sistema no funcional**

```python
# Base de datos no disponible
# Archivos core no encontrados
# Configuración crítica faltante

if not DATABASE_AVAILABLE:
    raise SystemError("Database connection failed")
```

### **2. Error (400-499) - Request inválido**

```python
# Validación de datos
# Autenticación/Autorización
# Recursos no encontrados

if area_hectares <= 0:
    raise ValidationError("Area must be greater than 0")

if not user.has_perm('core.add_project'):
    raise PermissionDenied("Insufficient permissions")
```

### **3. Warning - Funcionalidad degradada**

```python
# Cache no disponible
# Feature opcional offline

if not CELERY_AVAILABLE:
    logger.warning("Celery offline, processing synchronously")
    # Procesar de forma sincrónica
```

### **4. Info - Operación normal**

```python
# Operaciones exitosas
# Estado del sistema

logger.info(f"Project {project.id} created by user {user.id}")
```

---

## 🛡️ Validación de Entrada

**Regla:** Validar siempre en serializers/forms, no en vistas.

❌ **MAL - Validación en vista:**
```python
@api_view(['POST'])
def calculate_rational(request):
    C = request.data.get('C')
    if C < 0 or C > 1:
        return Response({'error': 'Invalid C'}, status=400)
    # ...
```

✅ **BIEN - Validación en serializer:**
```python
# api/serializers.py
class RationalMethodSerializer(serializers.Serializer):
    C = serializers.FloatField(min_value=0.0, max_value=1.0)
    I = serializers.FloatField(min_value=0.0)
    A = serializers.FloatField(min_value=0.0)

    def validate_A(self, value):
        if value <= 0:
            raise serializers.ValidationError("Area must be greater than 0")
        return value

# api/views.py
@api_view(['POST'])
def calculate_rational(request):
    serializer = RationalMethodSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    result = calculate_rational_method(**serializer.validated_data)
    return Response(result)
```

---

## 🔄 Manejo de Transacciones

**Usar atomic() para operaciones múltiples:**

```python
from django.db import transaction

@transaction.atomic
def create_project_with_watersheds(project_data, watersheds_data):
    """Create project and watersheds atomically"""
    try:
        project = Project.objects.create(**project_data)

        for watershed_data in watersheds_data:
            Watershed.objects.create(project=project, **watershed_data)

        return project

    except Exception as e:
        # Rollback automático
        logger.error(f"Failed to create project: {e}")
        raise
```

---

## 📝 Logging Best Practices

### **Configuración en settings.py**

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'hidrocal.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'core': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
```

### **Uso en código**

```python
import logging

logger = logging.getLogger(__name__)

# DEBUG - Información detallada para debugging
logger.debug(f"Processing watershed {watershed.id}")

# INFO - Operaciones normales
logger.info(f"Project {project.id} created successfully")

# WARNING - Situación inusual pero no crítica
logger.warning(f"Redis unavailable, using fallback")

# ERROR - Error que afecta funcionalidad
logger.error(f"Failed to calculate hydrograph: {e}", exc_info=True)

# CRITICAL - Error que requiere atención inmediata
logger.critical(f"Database connection lost")
```

---

## 🚫 Anti-Patterns

### **1. Swallowing Exceptions**

❌ **NUNCA HACER:**
```python
try:
    result = complex_calculation()
except:
    pass  # Silenciosamente ignora el error!
```

✅ **HACER:**
```python
try:
    result = complex_calculation()
except CalculationError as e:
    logger.error(f"Calculation failed: {e}")
    result = None  # Valor por defecto explícito
```

### **2. Bare Except**

❌ **NUNCA HACER:**
```python
try:
    something()
except:  # Atrapa TODO, incluso KeyboardInterrupt!
    handle_error()
```

✅ **HACER:**
```python
try:
    something()
except SpecificException as e:
    handle_error(e)
except Exception as e:  # Si necesitas atrapar todo, ser explícito
    logger.error(f"Unexpected error: {e}", exc_info=True)
    raise
```

### **3. Logging and Re-raising**

❌ **DUPLICACIÓN:**
```python
try:
    something()
except Exception as e:
    logger.error(f"Error: {e}")
    raise  # Se loguea dos veces en niveles superiores
```

✅ **ELEGIR UNO:**
```python
# Opción 1: Loguear y manejar
try:
    something()
except Exception as e:
    logger.error(f"Error: {e}")
    return handle_error()

# Opción 2: Re-lanzar sin loguear (dejar que nivel superior lo maneje)
try:
    something()
except Exception as e:
    raise CustomException(f"Failed: {e}") from e
```

---

## 📱 Manejo de Errores en API

### **DRF Exception Handler Personalizado**

```python
# api/exceptions.py
from rest_framework.views import exception_handler
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    # Call DRF's default handler first
    response = exception_handler(exc, context)

    if response is not None:
        # Log API errors
        logger.warning(
            f"API Error: {exc}",
            extra={
                'status_code': response.status_code,
                'view': context['view'].__class__.__name__,
                'request': context['request'].path
            }
        )

        # Customize response format
        response.data = {
            'error': response.data,
            'status': response.status_code
        }

    else:
        # Unhandled exception - log as error
        logger.error(
            f"Unhandled exception: {exc}",
            exc_info=True,
            extra={'view': context['view'].__class__.__name__}
        )

        response = Response(
            {'error': 'Internal server error'},
            status=500
        )

    return response

# settings.py
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'api.exceptions.custom_exception_handler'
}
```

---

## 🧪 Testing Error Handling

```python
# tests/test_error_handling.py
import pytest
from rest_framework.test import APIClient
from django.urls import reverse

@pytest.mark.django_db
def test_create_project_missing_required_field():
    """Test error handling for missing required field"""
    client = APIClient()
    url = reverse('project-list')

    # Missing 'name' field
    data = {'description': 'Test'}
    response = client.post(url, data)

    assert response.status_code == 400
    assert 'name' in response.data

def test_create_watershed_invalid_area():
    """Test validation error for negative area"""
    client = APIClient()
    url = reverse('watershed-list')

    data = {
        'name': 'Test',
        'area_hectareas': -10  # Invalid!
    }
    response = client.post(url, data)

    assert response.status_code == 400
    assert 'area_hectareas' in response.data
```

---

**Última actualización:** 2025-11-08
