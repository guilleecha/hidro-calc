# Instrucciones para Claude CLI - FASE 1: MVP Método Racional

## 🎯 OBJETIVO PRINCIPAL

Crear una **aplicación web completa** que funcione en el navegador, donde el usuario pueda:
1. Abrir http://localhost:8000 en su navegador
2. Ver una interfaz gráfica profesional
3. Ingresar datos en un formulario (C, I, A)
4. Hacer clic en "Calcular"
5. Ver los resultados en pantalla sin recargar la página

---

## 📋 CONTEXTO DEL PROYECTO

**Proyecto**: HidroCalc - Herramienta de Hidrología e Hidráulica
**Usuario**: Ingeniero Civil especializado en diseño de pluviales
**Ubicación**: C:\myprojects\hidro-calc
**Stack**: 
- Backend: Python 3.14 + FastAPI
- Frontend: HTML5 + CSS3 + JavaScript (Vanilla)
- Cálculos: NumPy, SciPy

**Estructura ya creada**:
- Carpetas: src/, templates/, static/css, static/js, data/, tests/
- Entorno virtual: venv/ (activado)
- Dependencias instaladas: fastapi, uvicorn, numpy, scipy, pandas, matplotlib, jinja2, pydantic

---

## 🎨 REQUERIMIENTO CRÍTICO: INTERFAZ WEB GRÁFICA

**La aplicación DEBE tener una interfaz web completa que se visualiza en el navegador.**

### Características de la Interfaz:

#### Diseño Visual:
- **Tema**: Profesional, colores azules (tema agua/hidrología)
- **Layout**: Centrado, max-width 800px, responsive
- **Tipografía**: Sans-serif moderna (system fonts)
- **Espaciado**: Generoso, no apretado

#### Elementos de la Interfaz:
1. **Header**:
   - Logo o ícono de agua 💧
   - Título: "HidroCalc - Método Racional"
   - Subtítulo: "Cálculo de Caudales de Diseño"

2. **Card/Panel de Entrada**:
   - Título: "Datos de Entrada"
   - 3 campos de formulario con labels claros:
     * **Coeficiente de Escorrentía (C)**: Input numérico (0-1)
     * **Intensidad de Lluvia (I)**: Input numérico (mm/h)
     * **Área de la Cuenca (A)**: Input numérico (hectáreas)
   - Cada campo con:
     - Label descriptivo
     - Placeholder con ejemplo
     - Unidades visibles
     - Validación en tiempo real

3. **Botón de Acción**:
   - Texto: "Calcular Caudal"
   - Estilo destacado (color primario)
   - Efecto hover
   - Estado disabled durante cálculo

4. **Card/Panel de Resultados**:
   - Inicialmente oculto
   - Se muestra después de calcular
   - Título: "Resultados"
   - Mostrar:
     * Caudal en L/s (destacado, grande)
     * Caudal en m³/s (secundario)
     * Resumen de datos ingresados
   - Diseño tipo "card" con sombra

5. **Footer**:
   - Fórmula utilizada: Q = C × I × A / 360
   - Referencia bibliográfica

---

## 🔧 TAREAS ESPECÍFICAS

### 1. Backend - src/main.py
```python
# Servidor FastAPI que:
- Sirve archivos estáticos desde /static
- Renderiza templates con Jinja2
- Endpoint GET / → retorna templates/index.html
- Incluye router de API
- Configuración CORS
- Puerto 8000
```

### 2. Lógica de Cálculo - src/core/rational_method.py
```python
# Módulo de cálculo puro (sin dependencia de FastAPI)

def calculate_rational_flow(C: float, I_mmh: float, A_ha: float) -> dict:
    """
    Calcula caudal usando Método Racional
    
    Fórmula: Q = C × I × A / 360
    
    Args:
        C: Coeficiente de escorrentía (0-1)
        I_mmh: Intensidad en mm/h
        A_ha: Área en hectáreas
    
    Returns:
        {
            'Q_ls': float,      # Caudal en L/s
            'Q_m3s': float,     # Caudal en m³/s
            'C': float,
            'I_mmh': float,
            'A_ha': float
        }
    
    Raises:
        ValueError: Si parámetros fuera de rango
    """
    
    # Validaciones:
    # - C entre 0 y 1
    # - I > 0 (advertir si > 500)
    # - A > 0
    
    # Cálculo
    # Q_ls = C × I × A / 360
    # Q_m3s = Q_ls / 1000
    
    # Retornar diccionario con resultados
```

### 3. API Endpoints - src/api/routes.py
```python
# Router FastAPI

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, validator

class RationalInput(BaseModel):
    C: float = Field(..., ge=0, le=1)
    I: float = Field(..., gt=0)
    A: float = Field(..., gt=0)
    
    # Validadores aquí

class RationalOutput(BaseModel):
    Q_ls: float
    Q_m3s: float
    C: float
    I_mmh: float
    A_ha: float
    formula: str = "Q = C × I × A / 360"

router = APIRouter()

@router.post("/api/calculate-rational", response_model=RationalOutput)
async def calculate_rational(data: RationalInput):
    """
    Endpoint para cálculo de método racional
    
    Recibe JSON: {"C": 0.65, "I": 80, "A": 5}
    Retorna JSON con resultados
    """
    try:
        # Llamar a función de cálculo
        # Retornar resultado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

### 4. Interfaz HTML - templates/index.html
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HidroCalc - Método Racional</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>🌊 HidroCalc</h1>
            <h2>Método Racional - Cálculo de Caudales</h2>
        </header>
        
        <main>
            <!-- Card de entrada -->
            <div class="card">
                <h3>Datos de Entrada</h3>
                <form id="rational-form">
                    <div class="form-group">
                        <label for="C">Coeficiente de Escorrentía (C)</label>
                        <input 
                            type="number" 
                            id="C" 
                            name="C" 
                            step="0.01" 
                            min="0" 
                            max="1"
                            placeholder="Ej: 0.65"
                            required>
                        <span class="unit">Adimensional (0-1)</span>
                    </div>
                    
                    <div class="form-group">
                        <label for="I">Intensidad de Lluvia (I)</label>
                        <input 
                            type="number" 
                            id="I" 
                            name="I" 
                            step="0.1" 
                            min="0.1"
                            placeholder="Ej: 80"
                            required>
                        <span class="unit">mm/h</span>
                    </div>
                    
                    <div class="form-group">
                        <label for="A">Área de la Cuenca (A)</label>
                        <input 
                            type="number" 
                            id="A" 
                            name="A" 
                            step="0.1" 
                            min="0.1"
                            placeholder="Ej: 5"
                            required>
                        <span class="unit">hectáreas</span>
                    </div>
                    
                    <button type="submit" class="btn-primary">
                        Calcular Caudal
                    </button>
                </form>
            </div>
            
            <!-- Card de resultados (inicialmente oculto) -->
            <div id="results" class="card results-card" style="display: none;">
                <h3>Resultados</h3>
                <div class="result-main">
                    <span class="result-label">Caudal de Diseño:</span>
                    <span id="Q-ls" class="result-value">--</span>
                    <span class="result-unit">L/s</span>
                </div>
                <div class="result-secondary">
                    <span id="Q-m3s" class="result-value-small">--</span>
                    <span class="result-unit-small">m³/s</span>
                </div>
                <div class="result-summary">
                    <p><strong>Datos utilizados:</strong></p>
                    <ul>
                        <li>C = <span id="result-C">--</span></li>
                        <li>I = <span id="result-I">--</span> mm/h</li>
                        <li>A = <span id="result-A">--</span> ha</li>
                    </ul>
                </div>
            </div>
        </main>
        
        <footer>
            <p><strong>Fórmula:</strong> Q = C × I × A / 360</p>
            <p><small>Referencia: Ven Te Chow, "Applied Hydrology" (1988)</small></p>
        </footer>
    </div>
    
    <script src="/static/js/app.js"></script>
</body>
</html>
```

### 5. Estilos CSS - static/css/style.css
```css
/* Diseño profesional con tema azul agua */

:root {
    --primary-color: #2563eb;      /* Azul principal */
    --primary-hover: #1d4ed8;      /* Azul hover */
    --bg-color: #f8fafc;           /* Fondo gris claro */
    --card-bg: #ffffff;            /* Fondo cards */
    --text-color: #1e293b;         /* Texto principal */
    --text-secondary: #64748b;     /* Texto secundario */
    --border-color: #e2e8f0;       /* Bordes */
    --success-color: #10b981;      /* Verde éxito */
    --shadow: 0 1px 3px rgba(0,0,0,0.1);
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: var(--bg-color);
    color: var(--text-color);
    line-height: 1.6;
    padding: 20px;
}

.container {
    max-width: 800px;
    margin: 0 auto;
}

header {
    text-align: center;
    margin-bottom: 40px;
}

header h1 {
    font-size: 2.5rem;
    color: var(--primary-color);
    margin-bottom: 10px;
}

header h2 {
    font-size: 1.2rem;
    color: var(--text-secondary);
    font-weight: normal;
}

.card {
    background: var(--card-bg);
    border-radius: 12px;
    padding: 30px;
    margin-bottom: 20px;
    box-shadow: var(--shadow);
}

.card h3 {
    font-size: 1.5rem;
    margin-bottom: 20px;
    color: var(--primary-color);
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    font-weight: 600;
    margin-bottom: 8px;
    color: var(--text-color);
}

.form-group input {
    width: 100%;
    padding: 12px 16px;
    font-size: 1rem;
    border: 2px solid var(--border-color);
    border-radius: 8px;
    transition: border-color 0.3s;
}

.form-group input:focus {
    outline: none;
    border-color: var(--primary-color);
}

.unit {
    display: block;
    font-size: 0.875rem;
    color: var(--text-secondary);
    margin-top: 4px;
}

.btn-primary {
    width: 100%;
    padding: 14px 24px;
    font-size: 1.1rem;
    font-weight: 600;
    color: white;
    background: var(--primary-color);
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.3s;
    margin-top: 10px;
}

.btn-primary:hover {
    background: var(--primary-hover);
}

.btn-primary:disabled {
    background: var(--border-color);
    cursor: not-allowed;
}

.results-card {
    border-left: 4px solid var(--success-color);
}

.result-main {
    text-align: center;
    padding: 20px;
    background: var(--bg-color);
    border-radius: 8px;
    margin-bottom: 15px;
}

.result-label {
    display: block;
    font-size: 0.9rem;
    color: var(--text-secondary);
    margin-bottom: 5px;
}

.result-value {
    font-size: 3rem;
    font-weight: bold;
    color: var(--primary-color);
}

.result-unit {
    font-size: 1.5rem;
    color: var(--text-secondary);
    margin-left: 10px;
}

.result-secondary {
    text-align: center;
    margin-bottom: 20px;
}

.result-value-small {
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--text-color);
}

.result-unit-small {
    font-size: 1rem;
    color: var(--text-secondary);
}

.result-summary {
    padding-top: 20px;
    border-top: 1px solid var(--border-color);
}

.result-summary ul {
    list-style: none;
    padding: 0;
}

.result-summary li {
    padding: 8px 0;
    font-size: 1rem;
}

footer {
    text-align: center;
    padding: 20px;
    color: var(--text-secondary);
}

footer p {
    margin: 5px 0;
}

/* Responsive */
@media (max-width: 600px) {
    header h1 {
        font-size: 2rem;
    }
    
    .card {
        padding: 20px;
    }
    
    .result-value {
        font-size: 2.5rem;
    }
}
```

### 6. JavaScript Frontend - static/js/app.js
```javascript
// App principal - Manejo del formulario y comunicación con API

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('rational-form');
    const resultsCard = document.getElementById('results');
    const submitBtn = form.querySelector('button[type="submit"]');
    
    // Event listener del formulario
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Obtener valores del formulario
        const C = parseFloat(document.getElementById('C').value);
        const I = parseFloat(document.getElementById('I').value);
        const A = parseFloat(document.getElementById('A').value);
        
        // Validación básica frontend
        if (!validateInputs(C, I, A)) {
            return;
        }
        
        // Deshabilitar botón durante cálculo
        submitBtn.disabled = true;
        submitBtn.textContent = 'Calculando...';
        
        try {
            // Llamada a la API
            const response = await fetch('/api/calculate-rational', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ C, I, A })
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
            // Rehabilitar botón
            submitBtn.disabled = false;
            submitBtn.textContent = 'Calcular Caudal';
        }
    });
    
    // Función de validación
    function validateInputs(C, I, A) {
        if (isNaN(C) || C < 0 || C > 1) {
            alert('El coeficiente C debe estar entre 0 y 1');
            return false;
        }
        
        if (isNaN(I) || I <= 0) {
            alert('La intensidad debe ser mayor a 0');
            return false;
        }
        
        if (I > 500) {
            if (!confirm('La intensidad parece muy alta (>500 mm/h). ¿Continuar?')) {
                return false;
            }
        }
        
        if (isNaN(A) || A <= 0) {
            alert('El área debe ser mayor a 0');
            return false;
        }
        
        return true;
    }
    
    // Función para mostrar resultados
    function displayResults(result) {
        // Actualizar valores
        document.getElementById('Q-ls').textContent = result.Q_ls.toFixed(2);
        document.getElementById('Q-m3s').textContent = result.Q_m3s.toFixed(4);
        document.getElementById('result-C').textContent = result.C;
        document.getElementById('result-I').textContent = result.I_mmh;
        document.getElementById('result-A').textContent = result.A_ha;
        
        // Mostrar card de resultados con animación
        resultsCard.style.display = 'block';
        resultsCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
});
```

---

## ✅ CRITERIOS DE ÉXITO

La tarea estará completa cuando:

1. ✅ El servidor FastAPI corre sin errores en http://localhost:8000
2. ✅ Al abrir http://localhost:8000 en el navegador se ve una interfaz gráfica completa
3. ✅ La interfaz tiene diseño profesional con colores azules
4. ✅ El usuario puede ingresar C, I, A en campos de formulario
5. ✅ Al hacer clic en "Calcular", se envía petición a la API
6. ✅ Los resultados se muestran en pantalla sin recargar la página
7. ✅ Las validaciones funcionan (frontend y backend)
8. ✅ Se manejan errores con mensajes claros
9. ✅ La interfaz es responsive (funciona en diferentes tamaños de pantalla)
10. ✅ El código está limpio, comentado y sigue las convenciones

---

## 🚀 COMANDO PARA EJECUTAR

Después de crear los archivos:

```bash
# Desde C:\myprojects\hidro-calc con entorno virtual activado
python src/main.py
```

Luego abrir en navegador: **http://localhost:8000**

---

## 📝 NOTAS FINALES

- Priorizar funcionalidad sobre optimización prematura
- Código simple y legible
- Comentarios en español
- Docstrings con fórmulas y referencias
- Usar el sistema de archivos MCP para crear todos los archivos directamente