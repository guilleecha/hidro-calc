# ⏱️ Metodología de Timestep (Δt) en Hietogramas

**Fecha:** 2025-11-09
**Autor:** HidroCalc Team

---

## 📚 Fundamento Teórico

El **timestep (Δt)** o intervalo de discretización temporal es crítico para:
1. Representar correctamente la distribución temporal de lluvia
2. Capturar el pico de intensidad
3. Obtener hidrogramas precisos
4. Evitar errores numéricos

---

## 🎯 Criterios Implementados

### **1. Basado en Tiempo de Concentración (Tc)** ⭐ PRIORITARIO

**Regla:** Δt ≤ Tc/5

**Referencias:**
- HEC-HMS Technical Reference Manual (2000)
- NRCS National Engineering Handbook, Part 630 (2007)

**Implementación:**
```python
timestep = tc_minutes / 5

# Límites prácticos:
if timestep < 1:
    timestep = 1    # Mínimo 1 minuto
elif timestep > 30:
    timestep = 30   # Máximo 30 minutos
else:
    # Redondear a múltiplo de 5 para practicidad
    timestep = round(timestep / 5) * 5
```

**Ejemplo:**
- Cuenca con Tc = 45 min → Δt = 45/5 = 9 min → **Δt = 10 min** (redondeado)
- Cuenca con Tc = 120 min → Δt = 120/5 = 24 min → **Δt = 25 min** (redondeado)

---

### **2. Basado en Duración de Tormenta** (Fallback)

Cuando **no se conoce Tc**, se usan reglas empíricas:

| Duración (D) | Timestep Recomendado | Justificación |
|-------------|---------------------|---------------|
| D ≤ 1 hora  | 5 minutos          | Cuencas urbanas, respuesta rápida |
| 1h < D ≤ 6h | 10 minutos         | Cuencas intermedias |
| 6h < D ≤ 24h | 15 minutos        | Tormentas diarias |
| D > 24h     | 30 minutos         | Tormentas multi-día |

**Referencias:**
- Chow, Maidment & Mays - Applied Hydrology (1988)
- Témez - Cálculo Hidrometeorológico de Caudales Máximos (1987)

---

### **3. Override Manual del Usuario**

El usuario puede especificar un timestep custom por razones como:
- Datos observados con intervalo fijo
- Compatibilidad con otros modelos
- Requisitos específicos del proyecto

**Prioridad:** Este valor sobreescribe cualquier cálculo automático.

---

## 🔄 Orden de Prioridad en el Sistema

```
1. custom_timestep (parámetro de función)
   ↓
2. storm.time_step_minutes (campo de modelo, si ≠ 5)
   ↓
3. Auto-calculado desde Tc (Δt = Tc/5)
   ↓
4. Auto-calculado desde duración (reglas empíricas)
```

---

## 💻 Implementación en Código

### **Función Principal:**

```python
def calculate_optimal_timestep(storm, custom_timestep=None):
    """
    Calculate optimal timestep for hyetograph discretization

    Based on:
    - HEC-HMS: Δt ≤ Tc/5
    - NRCS: Δt = 0.2 × Tc
    - Duration-based rules for large storms
    """
    if custom_timestep:
        return float(custom_timestep)

    watershed = storm.watershed
    duration_hours = float(storm.duration_hours)

    # Tc-based calculation (preferred)
    if watershed and watershed.tc_minutes:
        tc_minutes = float(watershed.tc_minutes)
        timestep = tc_minutes / 5

        # Practical limits
        timestep = max(1, min(30, timestep))

        # Round to nearest 5 minutes
        timestep = round(timestep / 5) * 5
        if timestep == 0:
            timestep = 5

        return timestep

    # Duration-based fallback
    if duration_hours <= 1:
        return 5
    elif duration_hours <= 6:
        return 10
    elif duration_hours <= 24:
        return 15
    else:
        return 30
```

---

## 📊 Ejemplos Prácticos

### **Caso 1: Cuenca Urbana Pequeña**
```
Tc = 30 minutos
Duración = 1 hora
Δt = 30/5 = 6 min → 5 min (redondeado)
```

### **Caso 2: Cuenca Rural Media**
```
Tc = 90 minutos
Duración = 6 horas
Δt = 90/5 = 18 min → 20 min (redondeado)
```

### **Caso 3: Sin Tc disponible**
```
Tc = desconocido
Duración = 24 horas
Δt = 15 min (por regla de duración)
```

### **Caso 4: Override Manual**
```
Usuario especifica: 10 minutos
Δt = 10 min (sin importar Tc o duración)
```

---

## ⚠️ Consideraciones Especiales

### **Método Racional:**
- **NO requiere hietograma discretizado**
- Intensidad = P_total / Tc
- El timestep es irrelevante para este método

### **Método SCS Unit Hydrograph:**
- Recomienda: Δt = 0.133 × Tc (NRCS)
- Implementado más conservador: Δt = 0.2 × Tc (Tc/5)

### **Métodos Numéricos (Onda Cinemática):**
- Requieren Δt muy pequeño para estabilidad (Courant condition)
- No aplica para métodos conceptuales

---

## 🔬 Validación

El timestep debe cumplir:

1. **Resolución temporal adecuada:**
   - Δt << Tc (al menos 5 veces menor)

2. **Número mínimo de intervalos:**
   - Mínimo 10 intervalos en la tormenta
   - num_intervals = duration / Δt ≥ 10

3. **Captura del pico de intensidad:**
   - Suficientes puntos para definir la curva IDF

---

## 📚 Referencias Bibliográficas

1. **HEC-HMS Technical Reference Manual** (2000)
   - U.S. Army Corps of Engineers
   - Recomienda: Δt ≤ Tc/5

2. **NRCS National Engineering Handbook, Part 630** (2007)
   - Natural Resources Conservation Service
   - Recomienda: Δt = 0.133 × Tc

3. **Chow, Maidment & Mays - Applied Hydrology** (1988)
   - McGraw-Hill
   - Capítulo 14: Design Storms

4. **Témez, J.R. - Cálculo Hidrometeorológico de Caudales Máximos** (1987)
   - MOPU, España
   - Método Racional Modificado

5. **Viessman & Lewis - Introduction to Hydrology** (2003)
   - Pearson
   - Capítulo 10: Hydrologic Design

---

## 🔄 Actualizaciones Futuras

### **Fase 3 (Planned):**
- [ ] Agregar método Chicago para distribución temporal
- [ ] Implementar método Sidle
- [ ] Permitir curvas IDF personalizadas

### **Fase 4 (Planned):**
- [ ] UI para configurar timestep manualmente
- [ ] Validación automática de timestep vs Tc
- [ ] Advertencias si Δt > Tc/5

---

**Última actualización:** 2025-11-09
**Revisión:** v1.0
