# 📏 Coding Standards - HidroCalc

Reglas detalladas de código para mantener calidad y consistencia.

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

## 📐 Tamaños Máximos

### **Funciones**

**Regla estricta:** Ninguna función debe exceder **50 líneas de código**.

❌ **Función de 80 líneas - PROHIBIDO**

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
```

**Ventajas:**
- Más fácil de testear
- Más fácil de entender
- Reutilización
- Debugging simplificado

---

### **Modelos Django**

**Regla:** Cada modelo debe tener **máximo 15 campos** + métodos helper.

Si un modelo crece demasiado, dividir en modelos relacionados.

✅ **CORRECTO - Dividir en modelos relacionados:**
```python
class Watershed(models.Model):
    """Core watershed data - solo 8 campos"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200)
    area_hectares = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)


class WatershedTopography(models.Model):
    """Physical characteristics - 7 campos"""
    watershed = models.OneToOneField(Watershed, on_delete=models.CASCADE)
    slope_percent = models.FloatField()
    max_elevation_m = models.FloatField()
    min_elevation_m = models.FloatField()
    # ...


class WatershedHydrology(models.Model):
    """Hydrological parameters - 7 campos"""
    watershed = models.OneToOneField(Watershed, on_delete=models.CASCADE)
    tc_horas = models.FloatField()
    nc_scs = models.IntegerField()
    # ...
```

---

### **Clases (Views, Services)**

**Regla:** Máximo **10 métodos públicos** por clase.

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
```

---

### **Archivos de Código**

**Regla:** Máximo **500 líneas** por archivo (incluyendo docstrings).

Si un archivo crece más, dividir:

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
```

---

## 🎨 Class-Based Views vs Function-Based Views

**Regla:** Para vistas con más de **30 líneas**, usar Class-Based Views.

❌ **Function-Based View larga (55 líneas)**

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
        return context
```

**Cuándo usar CBV vs FBV:**

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

## 🔍 Naming Conventions

**Regla:** Leer el codebase existente **antes** de nombrar variables.

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

## 🚫 NO OVER-ENGINEERING

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

## 🔄 Separation of Concerns

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
    project.calculated_value = complex_calculation()  # Cálculos en vista?
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

## 🔒 Resource Management

**Regla:** Siempre cerrar recursos.

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

## ✅ Pre-Commit Checklist

- [ ] Funciones ≤ 50 líneas
- [ ] Modelos ≤ 15 campos
- [ ] Clases ≤ 10 métodos públicos
- [ ] Archivos ≤ 500 líneas
- [ ] Vistas > 30 líneas usan CBV
- [ ] No hay código duplicado
- [ ] No hay dead code
- [ ] Naming consistente
- [ ] Separación de concerns
- [ ] Recursos cerrados correctamente

---

**Última actualización:** 2025-11-08
