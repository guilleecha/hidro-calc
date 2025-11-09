# 📊 Plan de Reorganización de Models - HidroCalc

**Fecha:** 2025-11-09
**Estado:** 📝 Documentado - Pendiente implementación
**Inspirado en:** [HydroML](https://github.com/guilleecha/HydroML) estructura modular

---

## 🎯 Objetivo

Reorganizar los modelos de Django de `core/models.py` (monolítico, 478 líneas) a una **estructura modular** con un archivo por modelo, siguiendo las mejores prácticas de HydroML y proyectos Django profesionales.

---

## 📊 Análisis de Situación Actual

### **Estructura Actual (Monolítica)**

```
core/
└── models.py            # ❌ 478 líneas con 5 modelos
    ├── Project          # Líneas 11-88   (78 líneas)
    ├── Watershed        # Líneas 89-185  (97 líneas)
    ├── DesignStorm      # Líneas 186-292 (107 líneas)
    ├── Hydrograph       # Líneas 293-416 (124 líneas)
    └── RainfallData     # Líneas 417-478 (62 líneas)
```

### **Problemas Identificados**

1. ❌ **Difícil navegación** - 478 líneas en un solo archivo
2. ❌ **Conflictos en Git** - múltiples devs editando el mismo archivo
3. ❌ **Code review complicado** - cambios mezclados en un archivo grande
4. ❌ **Violación de SRP** - un archivo con múltiples responsabilidades
5. ❌ **Escalabilidad limitada** - agregar models hace crecer el archivo indefinidamente
6. ❌ **Mantenibilidad baja** - difícil localizar y modificar models específicos

---

## 🎨 Estructura Propuesta (Modular)

### **Nueva Estructura (Estilo HydroML)**

```
core/
├── models/
│   ├── __init__.py          # Importa y exporta todos los models
│   ├── project.py           # Project model (78 líneas)
│   ├── watershed.py         # Watershed model (97 líneas)
│   ├── design_storm.py      # DesignStorm model (107 líneas)
│   ├── hydrograph.py        # Hydrograph model (124 líneas)
│   └── rainfall_data.py     # RainfallData model (62 líneas)
├── admin.py
├── apps.py
└── ...
```

### **Beneficios**

1. ✅ **Un archivo por modelo** - fácil de encontrar y editar
2. ✅ **Responsabilidad única** - cada archivo tiene un propósito claro
3. ✅ **Escalable** - agregar nuevos models sin tocar archivos existentes
4. ✅ **Imports limpios** - `from core.models import Project` sigue funcionando
5. ✅ **Git-friendly** - menos conflictos, PRs más pequeños
6. ✅ **Mantenibilidad alta** - cambios aislados por modelo
7. ✅ **Code review fácil** - cambios enfocados en un solo modelo
8. ✅ **Estándar profesional** - usado en HydroML y proyectos grandes

---

## 📝 Plan de Implementación

### **Fase 1: Preparación (5-10 min)**

#### **1.1. Crear carpeta de models**

```bash
mkdir core/models
```

#### **1.2. Crear `__init__.py` base**

```python
# core/models/__init__.py
"""
Models de HidroCalc - Modelos de hidrología

Estructura modular inspirada en HydroML.
Cada modelo en su propio archivo para mejor mantenibilidad.
"""

from .project import Project
from .watershed import Watershed
from .design_storm import DesignStorm
from .hydrograph import Hydrograph
from .rainfall_data import RainfallData

__all__ = [
    'Project',
    'Watershed',
    'DesignStorm',
    'Hydrograph',
    'RainfallData',
]
```

---

### **Fase 2: Extracción de Modelos (15-20 min)**

#### **2.1. Extraer Project**

**Archivo:** `core/models/project.py`

```python
"""
Model: Project - Proyecto hidrológico

Modelo para gestión de proyectos de hidrología.
Contiene información general del proyecto, ubicación y metadatos.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Project(models.Model):
    """
    Modelo para proyectos de hidrología.

    Un proyecto agrupa cuencas, tormentas de diseño y análisis hidrológicos.
    """

    # [Copiar campos del modelo actual líneas 14-67]
    name = models.CharField(...)
    description = models.TextField(...)
    # ... resto de campos

    class Meta:
        db_table = 'projects'
        ordering = ['-created_at']
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'

    def __str__(self):
        return self.name

    # [Copiar métodos del modelo actual]
```

**Líneas a copiar:** 11-88 de `core/models.py`

---

#### **2.2. Extraer Watershed**

**Archivo:** `core/models/watershed.py`

```python
"""
Model: Watershed - Cuenca hidrográfica

Modelo para cuencas hidrográficas dentro de un proyecto.
Contiene parámetros físicos y características de la cuenca.
"""

from django.db import models
from .project import Project


class Watershed(models.Model):
    """
    Modelo para cuencas hidrográficas.

    Define las características físicas e hidrológicas de una cuenca,
    incluyendo área, tiempo de concentración, curva número SCS, etc.
    """

    # Foreign Key
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='watersheds'
    )

    # [Copiar campos del modelo actual líneas 92-176]
    name = models.CharField(...)
    area_hectareas = models.FloatField(...)
    # ... resto de campos

    class Meta:
        db_table = 'watersheds'
        ordering = ['project', 'name']
        verbose_name = 'Cuenca'
        verbose_name_plural = 'Cuencas'

    def __str__(self):
        return f"{self.project.name} - {self.name}"
```

**Líneas a copiar:** 89-185 de `core/models.py`

---

#### **2.3. Extraer DesignStorm**

**Archivo:** `core/models/design_storm.py`

```python
"""
Model: DesignStorm - Tormenta de diseño

Modelo para tormentas de diseño asociadas a una cuenca.
Define precipitación total, duración y período de retorno.
"""

from django.db import models
from .watershed import Watershed


class DesignStorm(models.Model):
    """
    Modelo para tormentas de diseño.

    Representa una tormenta sintética utilizada para análisis hidrológico,
    con distribución temporal definida (SCS Tipo I, II, III, IA).
    """

    # Choices para distribution_type
    SCS_TYPE_I = 'scs_type_i'
    SCS_TYPE_IA = 'scs_type_ia'
    SCS_TYPE_II = 'scs_type_ii'
    SCS_TYPE_III = 'scs_type_iii'

    DISTRIBUTION_CHOICES = [
        (SCS_TYPE_I, 'SCS Tipo I'),
        (SCS_TYPE_IA, 'SCS Tipo IA'),
        (SCS_TYPE_II, 'SCS Tipo II'),
        (SCS_TYPE_III, 'SCS Tipo III'),
    ]

    # Foreign Key
    watershed = models.ForeignKey(
        Watershed,
        on_delete=models.CASCADE,
        related_name='design_storms'
    )

    # [Copiar campos del modelo actual líneas 199-283]
    name = models.CharField(...)
    return_period_years = models.IntegerField(...)
    # ... resto de campos

    class Meta:
        db_table = 'design_storms'
        ordering = ['watershed', 'return_period_years']
        verbose_name = 'Tormenta de Diseño'
        verbose_name_plural = 'Tormentas de Diseño'

    def __str__(self):
        return f"{self.watershed.name} - Tr={self.return_period_years}años"
```

**Líneas a copiar:** 186-292 de `core/models.py`

---

#### **2.4. Extraer Hydrograph**

**Archivo:** `core/models/hydrograph.py`

```python
"""
Model: Hydrograph - Hidrograma

Modelo para hidrogramas generados a partir de tormentas de diseño.
Almacena series temporales de caudal.
"""

from django.db import models
from .design_storm import DesignStorm


class Hydrograph(models.Model):
    """
    Modelo para hidrogramas.

    Representa la respuesta hidrológica de una cuenca ante una tormenta,
    calculado mediante diferentes métodos (SCS, Racional, Snyder, etc.).
    """

    # Choices para method
    METHOD_SCS = 'scs'
    METHOD_RATIONAL = 'rational'
    METHOD_SNYDER = 'snyder'
    METHOD_CUSTOM = 'custom'

    METHOD_CHOICES = [
        (METHOD_SCS, 'SCS Unit Hydrograph'),
        (METHOD_RATIONAL, 'Método Racional'),
        (METHOD_SNYDER, 'Hidrograma de Snyder'),
        (METHOD_CUSTOM, 'Personalizado'),
    ]

    # Foreign Key
    design_storm = models.ForeignKey(
        DesignStorm,
        on_delete=models.CASCADE,
        related_name='hydrographs'
    )

    # [Copiar campos del modelo actual líneas 303-407]
    name = models.CharField(...)
    method = models.CharField(...)
    hydrograph_data = models.JSONField(...)
    # ... resto de campos

    class Meta:
        db_table = 'hydrographs'
        ordering = ['design_storm', '-created_at']
        verbose_name = 'Hidrograma'
        verbose_name_plural = 'Hidrogramas'

    def __str__(self):
        return f"{self.design_storm.name} - {self.method}"
```

**Líneas a copiar:** 293-416 de `core/models.py`

---

#### **2.5. Extraer RainfallData**

**Archivo:** `core/models/rainfall_data.py`

```python
"""
Model: RainfallData - Datos de lluvia observados

Modelo para datos de lluvia medidos en estaciones meteorológicas.
Almacena series temporales de precipitación.
"""

from django.db import models
from .watershed import Watershed


class RainfallData(models.Model):
    """
    Modelo para datos de lluvia observados.

    Registra eventos de precipitación medidos, con series temporales
    de intensidad o acumulados. Útil para calibración de modelos.
    """

    # Foreign Key
    watershed = models.ForeignKey(
        Watershed,
        on_delete=models.CASCADE,
        related_name='rainfall_data'
    )

    # [Copiar campos del modelo actual líneas 427-469]
    event_date = models.DateField(...)
    total_rainfall_mm = models.FloatField(...)
    rainfall_series = models.JSONField(...)
    # ... resto de campos

    class Meta:
        db_table = 'rainfall_data'
        ordering = ['watershed', '-event_date']
        verbose_name = 'Dato de Lluvia'
        verbose_name_plural = 'Datos de Lluvia'

    def __str__(self):
        return f"{self.watershed.name} - {self.event_date}"
```

**Líneas a copiar:** 417-478 de `core/models.py`

---

### **Fase 3: Limpieza y Verificación (5 min)**

#### **3.1. Renombrar archivo antiguo (backup)**

```bash
mv core/models.py core/models.py.backup
```

**⚠️ NO eliminar todavía** - mantener como backup por seguridad.

#### **3.2. Verificar imports**

Probar que los imports funcionen igual:

```python
# Desde Django shell
from core.models import Project, Watershed, DesignStorm, Hydrograph, RainfallData

# Verificar que funcionan
Project.objects.all()
Watershed.objects.all()
```

---

### **Fase 4: Migraciones (5 min)**

#### **4.1. Verificar que no se requieren nuevas migraciones**

```bash
python manage.py makemigrations
```

**Resultado esperado:**
```
No changes detected
```

Si Django detecta cambios, **DETENER** y revisar qué salió mal.

#### **4.2. Verificar migraciones existentes**

```bash
python manage.py migrate --check
```

---

### **Fase 5: Testing (10 min)**

#### **5.1. Ejecutar tests unitarios**

```bash
python -m pytest tests/
```

**Todos los tests deben pasar** - 151/151 tests OK.

#### **5.2. Probar Django Admin**

```bash
python manage.py runserver
```

Visitar: http://localhost:8000/admin

Verificar que se pueden:
- Listar Projects
- Crear/Editar Watersheds
- Ver DesignStorms
- Acceder a todos los modelos

#### **5.3. Probar API**

```bash
curl http://localhost:8000/api/projects/
curl http://localhost:8000/api/watersheds/
```

Verificar que las APIs funcionan correctamente.

---

### **Fase 6: Actualizar Documentación (5 min)**

#### **6.1. Actualizar `context/architecture_overview.md`**

Cambiar:
```markdown
├── core/
│   ├── models.py        (480 líneas) - 5 modelos Django
```

Por:
```markdown
├── core/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── project.py
│   │   ├── watershed.py
│   │   ├── design_storm.py
│   │   ├── hydrograph.py
│   │   └── rainfall_data.py
```

#### **6.2. Actualizar `CLAUDE.md`**

Agregar nota sobre estructura modular de models.

---

## 🔒 Checklist de Seguridad

Antes de eliminar `models.py.backup`:

- [ ] Tests pasando (151/151)
- [ ] Django admin funcional
- [ ] API endpoints funcionando
- [ ] Imports funcionando desde otros archivos
- [ ] Migraciones sin cambios detectados
- [ ] Servidor corriendo sin errores
- [ ] Git commit con cambios

---

## 📊 Compatibilidad con Código Existente

### **Imports - Sin cambios necesarios**

**Antes:**
```python
from core.models import Project, Watershed, DesignStorm
```

**Después:**
```python
from core.models import Project, Watershed, DesignStorm  # ✅ Funciona igual
```

### **Admin - Sin cambios necesarios**

```python
# core/admin.py
from .models import Project, Watershed  # ✅ Funciona igual
```

### **Serializers - Sin cambios necesarios**

```python
# api/serializers.py
from core.models import Project  # ✅ Funciona igual
```

### **Views - Sin cambios necesarios**

```python
# api/views.py
from core.models import Watershed  # ✅ Funciona igual
```

**🎉 CERO cambios** en código que importa models.

---

## 🔄 Rollback Plan (Si algo falla)

Si hay problemas:

1. **Eliminar carpeta `core/models/`**
   ```bash
   rm -rf core/models/
   ```

2. **Restaurar archivo antiguo**
   ```bash
   mv core/models.py.backup core/models.py
   ```

3. **Verificar que todo funciona**
   ```bash
   python manage.py runserver
   python -m pytest
   ```

---

## 📋 Comparación: Antes vs Después

| Aspecto | Antes (Monolítico) | Después (Modular) |
|---------|-------------------|-------------------|
| **Archivos** | 1 archivo (478 líneas) | 6 archivos (~80 líneas c/u) |
| **Navegación** | Scroll en archivo grande | 1 clic al archivo correcto |
| **Edición** | Buscar en 478 líneas | Abrir archivo específico |
| **Git conflicts** | Frecuentes (1 archivo) | Raros (archivos separados) |
| **Code review** | Difícil (cambios mezclados) | Fácil (cambios aislados) |
| **Escalabilidad** | Archivo crece sin límite | Agregar archivos nuevos |
| **Mantenibilidad** | Baja | Alta |
| **Imports** | `from core.models import X` | `from core.models import X` |
| **Compatibilidad** | - | 100% compatible |

---

## 🎯 Métricas de Éxito

- ✅ **0 tests fallando** - 151/151 passing
- ✅ **0 migraciones nuevas** - estructura lógica sin cambios en BD
- ✅ **0 imports rotos** - compatibilidad total
- ✅ **5 archivos creados** - 1 por modelo + __init__.py
- ✅ **Servidor corriendo** - sin errores
- ✅ **Admin funcional** - todos los modelos accesibles
- ✅ **API funcional** - todos los endpoints respondiendo

---

## 📚 Referencias

- **HydroML Structure:** https://github.com/guilleecha/HydroML/tree/main/data_tools/models
- **Django Best Practices:** https://docs.djangoproject.com/en/5.2/topics/db/models/#organizing-models-in-a-package
- **Two Scoops of Django:** Capítulo sobre organización de models

---

## 🚀 Siguiente Paso

**Cuando estés listo para implementar:**

1. Leer este documento completo
2. Crear un branch: `git checkout -b feature/modular-models`
3. Seguir Fase 1-6 paso a paso
4. Verificar checklist de seguridad
5. Commit y PR: "refactor: Reorganizar models en estructura modular"

---

**Última actualización:** 2025-11-09
**Estado:** 📝 Documentado - Listo para implementar
**Estimado de tiempo:** 40-50 minutos
**Riesgo:** Bajo (100% compatible con código existente)
