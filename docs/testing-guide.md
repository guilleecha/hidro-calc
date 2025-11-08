# 🧪 Testing Guide - HidroCalc

Guía completa de testing para garantizar calidad del código.

---

## 🎯 Testing Philosophy

### **Reglas de Testing**

1. **NO usar mocks para servicios reales**
   - Probar contra base de datos real (SQLite en tests)
   - Probar contra Redis real si está disponible
   - Usar `pytest-django` con fixtures

2. **Tests completos antes de avanzar**
   - No pasar al siguiente test hasta completar el actual
   - Si falla, revisar estructura del test primero
   - No asumir que el código necesita refactoring sin validar el test

3. **Tests verbosos para debugging**
   - Mensajes de error claros y descriptivos
   - Imprimir valores intermedios cuando sea útil
   - Usar `pytest -v` para output detallado

4. **Test por cada función**
   - Toda función pública debe tener al menos un test
   - Tests deben cubrir casos normales y edge cases
   - Tests deben revelar fallos, no ocultarlos

---

## 🚨 ABSOLUTE RULE: IMPLEMENT TEST FOR EVERY FUNCTION

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

## 🚫 NO CHEATER TESTS

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

## 📝 Ejemplo de Test Correcto

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

## 🛠️ Testing Setup

### **Ejecutar tests**

```bash
# Ejecutar todos los tests
python -m pytest

# Con coverage
python -m pytest --cov=core --cov=api

# Tests específicos
python -m pytest tests/test_models.py

# Verbose mode
python -m pytest -v

# Con output de print statements
python -m pytest -s
```

---

## 📊 Estructura de Tests

```
tests/
├── __init__.py
├── conftest.py              # Fixtures compartidas
├── test_models.py           # Tests de modelos (5 tests)
├── test_serializers.py      # Tests de serializers (15+ tests)
├── test_api/
│   ├── test_projects.py     # API de proyectos
│   ├── test_watersheds.py   # API de cuencas
│   ├── test_storms.py       # API de tormentas
│   └── test_hydrographs.py  # API de hidrogramas
├── test_calculators/
│   ├── test_rational.py     # Método Racional
│   ├── test_idf.py          # Curvas IDF
│   └── test_tc.py           # Tiempo de Concentración
└── test_e2e/                # Tests E2E con Playwright
    └── test_calculators.py
```

---

## 🔧 Fixtures de pytest-django

```python
# tests/conftest.py
import pytest
from django.contrib.auth.models import User
from core.models import Project, Watershed

@pytest.fixture
def user(db):
    """Create test user"""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )

@pytest.fixture
def project(db, user):
    """Create test project"""
    return Project.objects.create(
        name="Test Project",
        description="Test description",
        location="Test Location",
        created_by=user
    )

@pytest.fixture
def watershed(db, project):
    """Create test watershed"""
    return Watershed.objects.create(
        project=project,
        name="Test Watershed",
        area_hectareas=100.0,
        tc_horas=2.5
    )
```

---

## 🧪 Test de Modelos

```python
# tests/test_models.py
import pytest
from core.models import Watershed

@pytest.mark.django_db
def test_watershed_area_conversion(watershed):
    """Test that area_m2 property correctly converts hectares"""
    assert watershed.area_hectareas == 100.0
    assert watershed.area_m2 == 1_000_000.0

@pytest.mark.django_db
def test_watershed_str_representation(watershed):
    """Test string representation"""
    expected = "Test Watershed (100.0 ha)"
    assert str(watershed) == expected
```

---

## 🌐 Test de API

```python
# tests/test_api/test_projects.py
import pytest
from rest_framework.test import APIClient
from django.urls import reverse

@pytest.mark.django_db
def test_list_projects_authenticated(user, project):
    """Test listing projects when authenticated"""
    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse('project-list')
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['name'] == "Test Project"

@pytest.mark.django_db
def test_create_project(user):
    """Test creating a new project"""
    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse('project-list')
    data = {
        'name': 'New Project',
        'description': 'New description',
        'location': 'New Location'
    }
    response = client.post(url, data)

    assert response.status_code == 201
    assert response.data['name'] == 'New Project'
```

---

## 🧮 Test de Cálculos

```python
# tests/test_calculators/test_rational.py
import pytest
from calculators.services import calculate_rational_method

def test_rational_method_zero_area():
    """Test rational method with zero area"""
    with pytest.raises(ValueError, match="Area must be greater than 0"):
        calculate_rational_method(C=0.65, I=80.0, A=0)

def test_rational_method_invalid_c():
    """Test rational method with invalid C coefficient"""
    with pytest.raises(ValueError, match="C must be between 0 and 1"):
        calculate_rational_method(C=1.5, I=80.0, A=100.0)

def test_rational_method_benchmark():
    """Test against Chow's Applied Hydrology benchmark"""
    # Chow Example 4.3.1
    result = calculate_rational_method(
        C=0.65,
        I=80.0,  # mm/h
        A=5.0    # ha
    )

    # Expected: Q = 0.278 * C * I * A = 72.17 L/s
    assert result['Q_lps'] == pytest.approx(72.17, rel=0.01)
    assert result['Q_m3s'] == pytest.approx(0.0722, rel=0.01)
```

---

## 🎭 Tests E2E con Playwright

```python
# tests/test_e2e/test_calculators.py
import pytest
from playwright.sync_api import Page, expect

def test_rational_method_calculator(page: Page):
    """Test rational method calculator E2E"""
    # Navigate to calculator
    page.goto("http://localhost:8000/calculators/rational/")

    # Fill inputs
    page.fill("#id_c", "0.65")
    page.fill("#id_i", "80")
    page.fill("#id_area", "5")

    # Submit
    page.click("#calculate-btn")

    # Wait for results
    page.wait_for_selector("#results")

    # Verify output
    q_lps = page.locator("#q_lps").inner_text()
    assert "72.17" in q_lps
```

---

## 📈 Coverage Goals

**Objetivos mínimos:**
- Models: 90%+ coverage
- Serializers: 85%+ coverage
- Services: 80%+ coverage
- Views/API: 75%+ coverage
- Overall: 80%+ coverage

```bash
# Generar reporte de coverage
python -m pytest --cov=core --cov=api --cov-report=html

# Ver reporte en navegador
# htmlcov/index.html
```

---

## ⚡ CI/CD con GitHub Actions

```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        pip install -r requirements_django.txt
        pip install pytest pytest-django pytest-cov

    - name: Run tests
      run: |
        python -m pytest --cov=core --cov=api
```

---

## 🔍 Test-Driven Development (TDD)

**Workflow recomendado:**

1. **Escribir test primero** (rojo)
```python
def test_calculate_tc_kirpich():
    result = calculate_tc_kirpich(length_m=1000, slope=0.05)
    assert result == pytest.approx(0.38, rel=0.01)  # FALLA
```

2. **Implementar función** (verde)
```python
def calculate_tc_kirpich(length_m, slope):
    """Kirpich formula for time of concentration"""
    return 0.0195 * (length_m ** 0.77) * (slope ** -0.385) / 60
```

3. **Refactorizar** (mantener verde)
```python
def calculate_tc_kirpich(length_m, slope):
    """
    Calculate time of concentration using Kirpich formula

    Args:
        length_m: Main channel length in meters
        slope: Channel slope (dimensionless)

    Returns:
        Time of concentration in hours
    """
    if length_m <= 0:
        raise ValueError("Length must be positive")
    if slope <= 0:
        raise ValueError("Slope must be positive")

    tc_minutes = 0.0195 * (length_m ** 0.77) * (slope ** -0.385)
    return tc_minutes / 60
```

---

**Última actualización:** 2025-11-08
