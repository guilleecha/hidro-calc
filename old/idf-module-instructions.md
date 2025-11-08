# Instrucciones: Módulo Curvas IDF Uruguay

## 🎯 Objetivo

Agregar al proyecto HidroCalc un módulo para calcular intensidades de lluvia usando las **Curvas IDF específicas de Uruguay**, permitiendo al usuario ingresar el valor de P₃,₁₀ y obtener intensidades corregidas por período de retorno, duración y área de cuenca.

---

## 📂 Archivos a Crear/Modificar

### 1. Backend - Lógica de Cálculo

**Archivo:** `src/core/idf_uruguay.py`

Crear funciones para:

#### Función: `calculate_CT(Tr)`
Calcula el factor de corrección por período de retorno.

**Fórmula:**
```python
CT(Tr) = 0.5786 - 0.4312 × log[ln(Tr / (Tr - 1))]
```

**Args:**
- `Tr` (float): Período de retorno en años (>= 2)

**Returns:**
- `float`: Factor CT

**Validaciones:**
- Tr debe ser >= 2 años
- Advertir si Tr > 100 años

---

#### Función: `calculate_CD(d)`
Calcula el factor de corrección por duración.

**Fórmulas:**

Para d < 3 horas:
```python
CD(d) = (0.6208 × d) / (d + 0.0137)^0.5639
```

Para d >= 3 horas:
```python
CD(d) = (1.0287 × d) / (d + 1.0293)^0.8083
```

**Args:**
- `d` (float): Duración en horas (> 0)

**Returns:**
- `float`: Factor CD

**Validaciones:**
- d debe ser > 0
- Advertir si d > 24 horas

---

#### Función: `calculate_CA(Ac, d)`
Calcula el factor de corrección por área de cuenca.

**Fórmula:**
```python
CA(Ac,d) = 1.0 - (0.3549 × d^(-0.4272)) × (1.0 - e^(-0.005792 × Ac))
```

**Args:**
- `Ac` (float): Área de cuenca en km² (>= 0)
- `d` (float): Duración en horas

**Returns:**
- `float`: Factor CA (retorna 1.0 si Ac = 0)

**Validaciones:**
- Si Ac = 0 o None, retornar 1.0 (sin corrección)
- Advertir si Ac > 300 km²

---

#### Función: `calculate_intensity_idf(P3_10, Tr, d, Ac=None)`
Función principal que calcula la intensidad corregida.

**Fórmula:**
```python
I(Tr,d) = P₃,₁₀ × CT(Tr) × CD(d) × CA(Ac,d) / d
```

**Args:**
- `P3_10` (float): Precipitación de 3h y 10 años en mm
- `Tr` (float): Período de retorno en años
- `d` (float): Duración en horas
- `Ac` (float, optional): Área de cuenca en km²

**Returns:**
- Dictionary con:
  ```python
  {
      'I_mmh': float,        # Intensidad en mm/h
      'P_mm': float,         # Precipitación total en mm
      'CT': float,           # Factor por Tr
      'CD': float,           # Factor por duración
      'CA': float,           # Factor por área
      'P3_10': float,        # Valor ingresado
      'Tr': float,           # Período de retorno
      'd_hours': float,      # Duración en horas
      'Ac_km2': float|None   # Área de cuenca
  }
  ```

**Validaciones:**
- P3_10 debe estar entre 50 y 100 mm (rango típico de Uruguay)
- Todas las validaciones de las funciones auxiliares

---

### 2. Backend - Modelos Pydantic

**Archivo:** `src/models/idf.py`

```python
from pydantic import BaseModel, Field, validator

class IDFInput(BaseModel):
    P3_10: float = Field(..., ge=50, le=100, description="P3,10 en mm")
    Tr: float = Field(..., ge=2, le=500, description="Período de retorno en años")
    d: float = Field(..., gt=0, le=48, description="Duración en horas")
    Ac: float = Field(None, ge=0, description="Área de cuenca en km²")
    
    @validator('Tr')
    def validate_Tr(cls, v):
        if v < 2:
            raise ValueError('El período de retorno debe ser >= 2 años')
        if v > 100:
            # Solo advertencia, no error
            pass
        return v
    
    @validator('d')
    def validate_duration(cls, v):
        if v <= 0:
            raise ValueError('La duración debe ser mayor a 0')
        return v

class IDFOutput(BaseModel):
    I_mmh: float = Field(..., description="Intensidad en mm/h")
    P_mm: float = Field(..., description="Precipitación total en mm")
    CT: float = Field(..., description="Factor de corrección por Tr")
    CD: float = Field(..., description="Factor de corrección por duración")
    CA: float = Field(..., description="Factor de corrección por área")
    P3_10: float
    Tr: float
    d_hours: float
    Ac_km2: float = None
    formula: str = Field(default="I = P₃,₁₀ × CT × CD × CA / d")
```

---

### 3. Backend - API Endpoint

**Archivo:** `src/api/routes.py` (agregar al router existente)

```python
@router.post("/api/calculate-idf", response_model=IDFOutput)
async def calculate_idf(data: IDFInput):
    """
    Calcula intensidad de lluvia usando curvas IDF de Uruguay
    
    Recibe:
    - P3_10: Precipitación de 3h y 10 años (mm)
    - Tr: Período de retorno (años)
    - d: Duración de la tormenta (horas)
    - Ac: Área de cuenca (km²) - opcional
    
    Retorna:
    - Intensidad corregida (mm/h)
    - Precipitación total (mm)
    - Factores de corrección (CT, CD, CA)
    """
    try:
        from src.core.idf_uruguay import calculate_intensity_idf
        
        result = calculate_intensity_idf(
            P3_10=data.P3_10,
            Tr=data.Tr,
            d=data.d,
            Ac=data.Ac
        )
        
        return IDFOutput(**result)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en cálculo: {str(e)}")
```

---

### 4. Frontend - HTML

**Archivo:** `templates/idf.html`

Crear una nueva página HTML con:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HidroCalc - Curvas IDF Uruguay</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>🌧️ Curvas IDF - Uruguay</h1>
            <p class="subtitle">Cálculo de Intensidades de Lluvia según Rodríguez Fontal (1980)</p>
        </header>

        <nav class="breadcrumb">
            <a href="/">← Inicio</a> / Curvas IDF
        </nav>

        <main>
            <!-- Card de Entrada -->
            <div class="card">
                <h3>📍 Datos de Entrada</h3>
                <form id="idf-form">
                    <div class="form-group">
                        <label for="P3_10">
                            P₃,₁₀ - Precipitación base (mm)
                            <span class="tooltip" title="Precipitación de 3 horas y 10 años. Consultar mapa de isoyetas.">ℹ️</span>
                        </label>
                        <input 
                            type="number" 
                            id="P3_10" 
                            name="P3_10" 
                            step="0.1" 
                            min="50" 
                            max="100"
                            placeholder="Ej: 75"
                            required>
                        <span class="unit">mm (rango típico: 60-90 mm)</span>
                        <small class="help-text">
                            <a href="#" id="show-map">📍 Ver mapa de isoyetas de Uruguay</a>
                        </small>
                    </div>

                    <div class="form-group">
                        <label for="Tr">Período de Retorno (años)</label>
                        <div class="radio-group">
                            <label class="radio-label">
                                <input type="radio" name="Tr" value="2"> 2
                            </label>
                            <label class="radio-label">
                                <input type="radio" name="Tr" value="5"> 5
                            </label>
                            <label class="radio-label">
                                <input type="radio" name="Tr" value="10" checked> 10
                            </label>
                            <label class="radio-label">
                                <input type="radio" name="Tr" value="25"> 25
                            </label>
                            <label class="radio-label">
                                <input type="radio" name="Tr" value="50"> 50
                            </label>
                            <label class="radio-label">
                                <input type="radio" name="Tr" value="100"> 100
                            </label>
                            <label class="radio-label">
                                <input type="radio" name="Tr" value="custom"> Otro
                            </label>
                        </div>
                        <input 
                            type="number" 
                            id="Tr-custom" 
                            name="Tr-custom"
                            step="1"
                            min="2"
                            placeholder="Período personalizado"
                            style="display: none; margin-top: 10px;">
                    </div>

                    <div class="form-group">
                        <label for="d">Duración de la Tormenta (horas)</label>
                        <select id="d" name="d" required>
                            <option value="">Seleccionar...</option>
                            <option value="0.25">15 minutos (0.25 h)</option>
                            <option value="0.5">30 minutos (0.5 h)</option>
                            <option value="1" selected>1 hora</option>
                            <option value="2">2 horas</option>
                            <option value="3">3 horas</option>
                            <option value="6">6 horas</option>
                            <option value="12">12 horas</option>
                            <option value="24">24 horas</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="Ac">
                            Área de la Cuenca (km²)
                            <span class="optional">(opcional)</span>
                        </label>
                        <input 
                            type="number" 
                            id="Ac" 
                            name="Ac" 
                            step="0.1" 
                            min="0"
                            placeholder="Ej: 30">
                        <span class="unit">km²</span>
                        <small class="help-text">Dejar vacío para calcular intensidad puntual (sin corrección por área)</small>
                    </div>

                    <button type="submit" class="btn-primary">
                        Calcular Intensidad
                    </button>
                </form>
            </div>

            <!-- Card de Resultados -->
            <div id="results" class="card results-card" style="display: none;">
                <h3>📊 Resultados</h3>
                
                <div class="result-main">
                    <span class="result-label">Intensidad de Lluvia:</span>
                    <span id="I-mmh" class="result-value">--</span>
                    <span class="result-unit">mm/h</span>
                </div>

                <div class="result-secondary">
                    <span class="result-label">Precipitación Total:</span>
                    <span id="P-mm" class="result-value-small">--</span>
                    <span class="result-unit-small">mm</span>
                </div>

                <div class="result-factors">
                    <h4>Factores de Corrección:</h4>
                    <table class="factors-table">
                        <tr>
                            <td><strong>CT</strong> (Período de retorno):</td>
                            <td id="CT">--</td>
                        </tr>
                        <tr>
                            <td><strong>CD</strong> (Duración):</td>
                            <td id="CD">--</td>
                        </tr>
                        <tr>
                            <td><strong>CA</strong> (Área de cuenca):</td>
                            <td id="CA">--</td>
                        </tr>
                    </table>
                </div>

                <div class="result-summary">
                    <p><strong>Datos utilizados:</strong></p>
                    <ul>
                        <li>P₃,₁₀ = <span id="result-P3_10">--</span> mm</li>
                        <li>Tr = <span id="result-Tr">--</span> años</li>
                        <li>d = <span id="result-d">--</span> horas</li>
                        <li>Ac = <span id="result-Ac">--</span></li>
                    </ul>
                </div>

                <div class="formula-box">
                    <strong>Fórmula:</strong> I = P₃,₁₀ × CT × CD × CA / d
                </div>
            </div>

            <!-- Card de Referencia -->
            <div class="card info-card">
                <h3>💡 Información de Referencia</h3>
                <p><strong>Fuente:</strong> Rodríguez Fontal (1980) - Curvas IDF de Uruguay</p>
                <p><strong>Período de datos:</strong> 1906-1980</p>
                <p><strong>Valores típicos de P₃,₁₀ en Uruguay:</strong></p>
                <ul>
                    <li>Montevideo: ~75 mm</li>
                    <li>La Paloma: ~74 mm</li>
                    <li>Minas: ~79 mm</li>
                    <li>Rango general: 60-90 mm</li>
                </ul>
                <button id="btn-show-recommendations" class="btn-secondary">
                    Ver recomendaciones de Tr según tipo de obra
                </button>
            </div>
        </main>

        <footer>
            <p><small>Referencia: Rodríguez Fontal (1980), Genta et al. (1998)</small></p>
        </footer>
    </div>

    <script src="/static/js/idf.js"></script>
</body>
</html>
```

---

### 5. Frontend - JavaScript

**Archivo:** `static/js/idf.js`

```javascript
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('idf-form');
    const resultsCard = document.getElementById('results');
    const submitBtn = form.querySelector('button[type="submit"]');
    
    // Manejo de Tr personalizado
    const trRadios = document.querySelectorAll('input[name="Tr"]');
    const trCustomInput = document.getElementById('Tr-custom');
    
    trRadios.forEach(radio => {
        radio.addEventListener('change', (e) => {
            if (e.target.value === 'custom') {
                trCustomInput.style.display = 'block';
                trCustomInput.required = true;
            } else {
                trCustomInput.style.display = 'none';
                trCustomInput.required = false;
                trCustomInput.value = '';
            }
        });
    });
    
    // Submit del formulario
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Obtener valores
        const P3_10 = parseFloat(document.getElementById('P3_10').value);
        
        // Determinar Tr
        let Tr;
        const selectedTr = document.querySelector('input[name="Tr"]:checked');
        if (selectedTr.value === 'custom') {
            Tr = parseFloat(trCustomInput.value);
        } else {
            Tr = parseFloat(selectedTr.value);
        }
        
        const d = parseFloat(document.getElementById('d').value);
        const AcInput = document.getElementById('Ac').value;
        const Ac = AcInput ? parseFloat(AcInput) : null;
        
        // Validaciones básicas
        if (!validateInputs(P3_10, Tr, d)) {
            return;
        }
        
        // Deshabilitar botón
        submitBtn.disabled = true;
        submitBtn.textContent = 'Calculando...';
        
        try {
            // Preparar datos
            const requestData = {
                P3_10: P3_10,
                Tr: Tr,
                d: d
            };
            
            if (Ac !== null) {
                requestData.Ac = Ac;
            }
            
            // Llamada a la API
            const response = await fetch('/api/calculate-idf', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Error en el cálculo');
            }
            
            const result = await response.json();
            
            // Mostrar resultados
            displayResults(result);
            
        } catch (error) {
            alert(`Error: ${error.message}`);
            console.error('Error:', error);
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Calcular Intensidad';
        }
    });
    
    // Validaciones
    function validateInputs(P3_10, Tr, d) {
        if (isNaN(P3_10) || P3_10 < 50 || P3_10 > 100) {
            alert('P₃,₁₀ debe estar entre 50 y 100 mm');
            return false;
        }
        
        if (isNaN(Tr) || Tr < 2) {
            alert('El período de retorno debe ser mayor o igual a 2 años');
            return false;
        }
        
        if (Tr > 100) {
            if (!confirm('Período de retorno muy alto (>100 años). ¿Continuar?')) {
                return false;
            }
        }
        
        if (isNaN(d) || d <= 0) {
            alert('La duración debe ser mayor a 0');
            return false;
        }
        
        return true;
    }
    
    // Mostrar resultados
    function displayResults(result) {
        // Valores principales
        document.getElementById('I-mmh').textContent = result.I_mmh.toFixed(2);
        document.getElementById('P-mm').textContent = result.P_mm.toFixed(2);
        
        // Factores
        document.getElementById('CT').textContent = result.CT.toFixed(4);
        document.getElementById('CD').textContent = result.CD.toFixed(4);
        document.getElementById('CA').textContent = result.CA.toFixed(4);
        
        // Datos de entrada
        document.getElementById('result-P3_10').textContent = result.P3_10;
        document.getElementById('result-Tr').textContent = result.Tr;
        document.getElementById('result-d').textContent = result.d_hours;
        document.getElementById('result-Ac').textContent = 
            result.Ac_km2 !== null ? `${result.Ac_km2} km²` : 'Sin corrección (puntual)';
        
        // Mostrar card
        resultsCard.style.display = 'block';
        resultsCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
});
```

---

### 6. Estilos CSS Adicionales

**Archivo:** `static/css/style.css` (agregar al final)

```css
/* Estilos para módulo IDF */

.subtitle {
    font-size: 1rem;
    color: var(--text-secondary);
    margin-top: -10px;
}

.breadcrumb {
    margin-bottom: 20px;
    font-size: 0.9rem;
}

.breadcrumb a {
    color: var(--primary-color);
    text-decoration: none;
}

.breadcrumb a:hover {
    text-decoration: underline;
}

.radio-group {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    margin: 10px 0;
}

.radio-label {
    display: flex;
    align-items: center;
    gap: 5px;
    cursor: pointer;
}

.radio-label input[type="radio"] {
    cursor: pointer;
}

.help-text {
    display: block;
    margin-top: 5px;
    font-size: 0.85rem;
    color: var(--text-secondary);
}

.help-text a {
    color: var(--primary-color);
    text-decoration: none;
}

.help-text a:hover {
    text-decoration: underline;
}

.optional {
    font-size: 0.85rem;
    color: var(--text-secondary);
    font-weight: normal;
}

.tooltip {
    cursor: help;
    color: var(--primary-color);
}

.result-factors {
    margin-top: 20px;
    padding-top: 20px;
    border-top: 1px solid var(--border-color);
}

.result-factors h4 {
    margin-bottom: 10px;
    color: var(--primary-color);
}

.factors-table {
    width: 100%;
    border-collapse: collapse;
}

.factors-table td {
    padding: 8px 0;
}

.factors-table td:last-child {
    text-align: right;
    font-family: monospace;
}

.formula-box {
    margin-top: 20px;
    padding: 15px;
    background: var(--bg-color);
    border-left: 4px solid var(--primary-color);
    border-radius: 4px;
    font-family: monospace;
}

.info-card {
    background: #f0f9ff;
    border-left: 4px solid var(--primary-color);
}

.info-card ul {
    margin: 10px 0;
    padding-left: 20px;
}

.info-card li {
    margin: 5px 0;
}

.btn-secondary {
    width: 100%;
    padding: 12px 20px;
    margin-top: 15px;
    font-size: 1rem;
    color: var(--primary-color);
    background: white;
    border: 2px solid var(--primary-color);
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s;
}

.btn-secondary:hover {
    background: var(--primary-color);
    color: white;
}
```

---

### 7. Actualizar Navegación

**Archivo:** `templates/index.html` (agregar link)

Agregar en la página principal un botón/card para acceder al módulo IDF:

```html
<div class="card">
    <h3>🌧️ Curvas IDF - Uruguay</h3>
    <p>Cálculo de intensidades de lluvia según período de retorno y duración</p>
    <a href="/idf" class="btn-secondary">Abrir módulo</a>
</div>
```

**Archivo:** `src/main.py` (agregar ruta)

```python
@app.get("/idf")
async def idf_page(request: Request):
    """Página de Curvas IDF"""
    return templates.TemplateResponse(
        "idf.html",
        {"request": request, "title": "Curvas IDF - Uruguay"}
    )
```

---

## ✅ Checklist de Implementación

- [ ] Crear `src/core/idf_uruguay.py` con todas las funciones
- [ ] Crear `src/models/idf.py` con modelos Pydantic
- [ ] Agregar endpoint en `src/api/routes.py`
- [ ] Crear `templates/idf.html`
- [ ] Crear `static/js/idf.js`
- [ ] Agregar estilos en `static/css/style.css`
- [ ] Agregar ruta `/idf` en `src/main.py`
- [ ] Agregar link en `templates/index.html`
- [ ] Crear tests en `tests/test_idf.py`

---

## 🧪 Casos de Prueba

### Caso 1: Ejemplo del PDF (La Paloma)
- P₃,₁₀ = 74 mm
- Tr = 5 años
- d = 1 hora
- Ac = 30 km²
- **Resultado esperado**: I ≈ 36.3 mm/h

### Caso 2: Sin corrección por área
- P₃,₁₀ = 75 mm
- Tr = 10 años
- d = 1 hora
- Ac = None
- **Resultado esperado**: I ≈ 38.6 mm/h (aproximado)

### Caso 3: Duración corta
- P₃,₁₀ = 79 mm
- Tr = 10 años
- d = 0.5 horas
- **Resultado esperado**: Mayor intensidad que caso 2

---

## 📚 Referencias

- Rodríguez Fontal (1980) - Curvas IDF de Uruguay
- Genta et al. (1998) - Actualización de curvas IDF
- Manual de Hidrología e Hidráulica Aplicadas - UdelaR

---

## 🎯 Criterios de Éxito

La implementación estará completa cuando:

1. ✅ El usuario puede ingresar P₃,₁₀ manualmente
2. ✅ El usuario puede seleccionar Tr de opciones predefinidas o ingresar valor personalizado
3. ✅ El usuario puede seleccionar duración de un dropdown
4. ✅ El usuario puede opcionalmente ingresar área de cuenca
5. ✅ El sistema calcula correctamente I, P, CT, CD, CA
6. ✅ Los resultados se muestran de forma clara y profesional
7. ✅ Las validaciones funcionan en frontend y backend
8. ✅ El módulo es accesible desde la página principal
9. ✅ Los casos de prueba del PDF se replican correctamente

---

## 💡 Mejoras Futuras (Opcional)

### Fase 2.1 - Visualización
- Gráfico de curva IDF con múltiples períodos de retorno
- Tabla comparativa de intensidades para diferentes duraciones
- Exportación de resultados a PDF

### Fase 2.2 - Datos de Referencia
- Base de datos JSON con valores de P₃,₁₀ por ciudad
- Mapa interactivo de Uruguay con isoyetas
- Selector de ubicación por coordenadas o ciudad

### Fase 2.3 - Herramientas Adicionales
- Calculadora inversa: dado I y d, encontrar Tr
- Comparador de múltiples escenarios
- Generación de hietograma de diseño a partir de IDF

---

## 🚀 Comando para Ejecutar después de Implementar

```powershell
# Activar entorno virtual
.\venv\Scripts\activate

# Ejecutar servidor
python src/main.py
```

Luego abrir:
- Página principal: http://localhost:8000
- Módulo IDF: http://localhost:8000/idf
- API Docs: http://localhost:8000/docs

---

## 📋 Notas Importantes para la Implementación

1. **Precisión de Cálculos**: Usar como mínimo 4 decimales en los factores CT, CD, CA
2. **Manejo de Errores**: Todos los errores deben tener mensajes descriptivos en español
3. **Validaciones**: Implementar validaciones tanto en frontend (UX) como backend (seguridad)
4. **Documentación**: Incluir docstrings completos en todas las funciones
5. **Testing**: Crear tests unitarios con los ejemplos del PDF
6. **Accesibilidad**: Labels descriptivos, tooltips informativos
7. **Performance**: Los cálculos son ligeros, no requieren optimización especial

---

## 🔧 Troubleshooting Común

### Error: "P3_10 fuera de rango"
- Verificar que el valor está entre 50-100 mm
- Consultar mapa de isoyetas del PDF

### Error: "División por cero"
- Verificar que duración d > 0
- Verificar que Tr >= 2

### Resultados no coinciden con ejemplos
- Verificar precisión de cálculo (usar float, no int)
- Revisar implementación de fórmulas (paréntesis, exponentes)
- Comparar factores intermedios (CT, CD, CA)

---

## ✨ Código de Ejemplo para Testing

**Archivo:** `tests/test_idf.py`

```python
import pytest
from src.core.idf_uruguay import (
    calculate_CT,
    calculate_CD,
    calculate_CA,
    calculate_intensity_idf
)

def test_example_la_paloma():
    """Ejemplo del PDF - La Paloma"""
    result = calculate_intensity_idf(
        P3_10=74,
        Tr=5,
        d=1,
        Ac=30
    )
    
    # Verificar resultado aproximado
    assert 35.5 <= result['I_mmh'] <= 37.0
    assert result['CT'] > 0
    assert result['CD'] > 0
    assert result['CA'] > 0

def test_CT_calculation():
    """Test del factor CT"""
    CT_5 = calculate_CT(5)
    CT_10 = calculate_CT(10)
    CT_100 = calculate_CT(100)
    
    # CT debe ser creciente con Tr
    assert CT_5 < CT_10 < CT_100
    
    # Valores aproximados conocidos
    assert 0.8 <= CT_5 <= 0.9
    assert 0.9 <= CT_10 <= 1.0

def test_CD_short_duration():
    """Test de CD para duraciones < 3h"""
    CD_1 = calculate_CD(1)
    CD_2 = calculate_CD(2)
    
    # CD debe decrecer con duración
    assert CD_1 > CD_2

def test_CD_long_duration():
    """Test de CD para duraciones >= 3h"""
    CD_3 = calculate_CD(3)
    CD_6 = calculate_CD(6)
    CD_24 = calculate_CD(24)
    
    # CD debe decrecer con duración
    assert CD_3 > CD_6 > CD_24

def test_CA_no_area():
    """Test de CA sin área de cuenca"""
    CA = calculate_CA(None, 1)
    assert CA == 1.0
    
    CA = calculate_CA(0, 1)
    assert CA == 1.0

def test_CA_with_area():
    """Test de CA con área de cuenca"""
    CA_30 = calculate_CA(30, 1)
    
    # CA debe ser < 1 cuando hay área
    assert 0 < CA_30 < 1

def test_invalid_inputs():
    """Test de validaciones"""
    with pytest.raises(ValueError):
        calculate_intensity_idf(P3_10=40, Tr=5, d=1)  # P3_10 muy bajo
    
    with pytest.raises(ValueError):
        calculate_intensity_idf(P3_10=75, Tr=1, d=1)  # Tr < 2
    
    with pytest.raises(ValueError):
        calculate_intensity_idf(P3_10=75, Tr=5, d=0)  # d = 0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

---

## 📞 Soporte

Si encuentras problemas durante la implementación:

1. Verificar que todas las dependencias están instaladas
2. Revisar logs del servidor para errores detallados
3. Comparar resultados con ejemplos del PDF
4. Verificar que las fórmulas están correctamente implementadas

---

**Fin de las instrucciones. Implementar siguiendo el orden del checklist.**