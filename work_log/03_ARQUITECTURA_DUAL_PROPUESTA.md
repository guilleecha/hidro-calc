# 🏗️ Arquitectura Dual Propuesta - HidroCalc

**Fecha:** 2025-11-08
**Estado:** 📋 En Diseño

---

## 🎯 Visión del Producto

HidroCalc debe funcionar en **DOS MODOS** distintos para diferentes tipos de uso:

### **Modo 1: Calculadora Rápida** ⚡
**Público:** Profesionales que necesitan cálculos rápidos
**Características:**
- Sin registro/login necesario
- Acceso inmediato
- Calculadoras simples e independientes
- No persiste datos (o mínimo)
- Exportar resultados a PDF/Excel

### **Modo 2: HidroStudio Professional** 🏢
**Público:** Profesionales trabajando en proyectos formales
**Características:**
- Requiere login/autenticación
- Gestión de proyectos completos
- Base de datos persistente
- Flujo hidrológico completo integrado
- Reportes, gráficos, comparaciones
- Colaboración (futuro)

---

## 🏗️ Arquitectura Propuesta

```
┌─────────────────────────────────────────────────────────┐
│                     HIDROCAL.COM                        │
│                    Página Principal                      │
└─────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┴─────────────────┐
        │                                   │
        ▼                                   ▼
┌──────────────────┐              ┌──────────────────┐
│  ⚡ CALCULADORAS │              │ 🏢 HIDROSTUDIO   │
│     RÁPIDAS      │              │   PROFESSIONAL   │
└──────────────────┘              └──────────────────┘
```

---

## ⚡ MODO 1: Calculadoras Rápidas

### **Ubicación:** `/calculators/*`

### **Páginas:**

#### `/calculators/rational`
**Método Racional Simple**
- Inputs: C, I, A
- Output: Q (inmediato)
- Botón: "Exportar PDF"
- Sin login, sin BD

#### `/calculators/idf`
**Curvas IDF Uruguay**
- Inputs: Tc, Tr, P₃,₁₀
- Output: I
- Botón: "Exportar PDF"
- Sin login, sin BD

#### `/calculators/time-concentration`
**Tiempo de Concentración**
- Varios métodos (Kirpich, California, etc.)
- Input: L, S, tipo de cuenca
- Output: Tc
- Sin login, sin BD

#### `/calculators/runoff-coefficient`
**Coeficiente Ponderado**
- Input: Tabla de superficies
- Output: C ponderado
- Ya implementado

### **Características Comunes:**
- ✅ Cálculo instantáneo
- ✅ Exportar a PDF/Excel
- ✅ Copiar/Pegar resultados
- ✅ Sin persistencia
- ✅ UI limpia y simple
- ❌ No requiere login
- ❌ No guarda en BD
- ❌ No integrado entre sí

---

## 🏢 MODO 2: HidroStudio Professional

### **Ubicación:** `/studio/*`

### **Flujo de Trabajo:**

```
LOGIN/REGISTRO
    ↓
DASHBOARD
    ├─ Mis Proyectos
    ├─ Proyectos Compartidos
    └─ Crear Nuevo Proyecto
    ↓
PROYECTO: "Sistema Drenaje Montevideo"
    ├─ Cuencas (3)
    ├─ Análisis (12)
    └─ Reportes (5)
    ↓
CUENCA: "Arroyo Miguelete Alto"
    ├─ Datos Básicos
    ├─ Análisis Hidrológico
    └─ Resultados
    ↓
ANÁLISIS COMPLETO INTEGRADO
    1. Datos de Cuenca
    2. Curvas IDF → I
    3. Método Racional → Q
    4. Hidrograma
    5. Guardar en BD
    ↓
RESULTADOS
    ├─ Visualizar
    ├─ Comparar
    ├─ Exportar
    └─ Reportar
```

### **Páginas del Studio:**

#### `/studio/dashboard`
**Panel Principal**
- Lista de proyectos
- Actividad reciente
- Accesos rápidos

#### `/studio/projects/:id`
**Vista de Proyecto**
- Cuencas del proyecto
- Análisis realizados
- Estadísticas

#### `/studio/watersheds/:id/analyze`
**Análisis Completo de Cuenca** ⭐ PÁGINA CLAVE

**Flujo Integrado:**

```
┌─────────────────────────────────────────────────┐
│ PASO 1: Datos de Cuenca                        │
├─────────────────────────────────────────────────┤
│ Nombre: Arroyo Miguelete Alto                   │
│ Área: 250 ha                                    │
│ Tc: [Calcular▼] o [Ingresar Manual]            │
│   → Si Calcular: Método Kirpich, etc.          │
│   → Resultado: Tc = 1.8 h                       │
│ NC: 72 (para SCS)                               │
│ [Guardar Cuenca]                                │
└─────────────────────────────────────────────────┘
            ↓ (automático)
┌─────────────────────────────────────────────────┐
│ PASO 2: Tormenta de Diseño (IDF)               │
├─────────────────────────────────────────────────┤
│ Método: Rodríguez Fontal (Uruguay) ▼           │
│ Tc: 1.8 h (de la cuenca) ✓                     │
│ Tr: [10▼] años                                  │
│ Duración: [2▼] horas                            │
│ P₃,₁₀: 140 mm                                   │
│                                                 │
│ [Calcular Intensidad]                           │
│ → I = 85 mm/h                                   │
│ [Guardar Tormenta de Diseño]                    │
└─────────────────────────────────────────────────┘
            ↓ (automático)
┌─────────────────────────────────────────────────┐
│ PASO 3: Método de Cálculo                      │
├─────────────────────────────────────────────────┤
│ Método: [Método Racional ▼]                    │
│   Opciones: Racional / SCS / Snyder             │
│                                                 │
│ Si Racional:                                    │
│   C: [0.65]                                     │
│   I: 85 mm/h (de paso 2) ✓                     │
│   A: 250 ha (de paso 1) ✓                      │
│                                                 │
│ [Calcular Hidrograma]                           │
└─────────────────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────────────┐
│ PASO 4: Resultados del Hidrograma              │
├─────────────────────────────────────────────────┤
│ Q pico: 36.1 m³/s                               │
│ Tiempo al pico: 1.8 h                           │
│ Volumen total: 234,000 m³                       │
│                                                 │
│ [Gráfico del Hidrograma]                        │
│ [Tabla de Valores]                              │
│                                                 │
│ ✅ Se guardó en BD automáticamente              │
└─────────────────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────────────┐
│ ACCIONES                                        │
├─────────────────────────────────────────────────┤
│ [Comparar con otros hidrogramas]                │
│ [Exportar a PDF]                                │
│ [Exportar a Excel]                              │
│ [Generar Reporte]                               │
│ [Nuevo Análisis]                                │
└─────────────────────────────────────────────────┘
```

#### `/studio/watersheds/:id/history`
**Historial de Análisis**
- Lista de todos los análisis de la cuenca
- Filtros por Tr, duración, fecha
- Comparación visual

#### `/studio/reports/:id`
**Generador de Reportes**
- Seleccionar análisis
- Template profesional
- Exportar PDF con logo

---

## 📊 Comparación de Modos

| Característica | Calculadora Rápida ⚡ | HidroStudio 🏢 |
|----------------|----------------------|----------------|
| **Login** | ❌ No necesario | ✅ Requerido |
| **Base de Datos** | ❌ No guarda | ✅ Guarda todo |
| **Flujo** | Simple, 1 paso | Completo, integrado |
| **Exportar** | ✅ PDF/Excel básico | ✅ Reportes profesionales |
| **Proyectos** | ❌ No | ✅ Sí |
| **Comparación** | ❌ No | ✅ Sí |
| **Colaboración** | ❌ No | ✅ (Futuro) |
| **Historial** | ❌ No | ✅ Sí |
| **Costo** | 🆓 Gratis | 💰 Suscripción (futuro) |

---

## 🎨 Diseño de Navegación

### **Página Principal** `/`

```
┌─────────────────────────────────────────────────┐
│             🌊 HIDROC ALC                      │
│   Herramientas de Hidrología e Hidráulica      │
├─────────────────────────────────────────────────┤
│                                                 │
│  ¿Qué necesitas hacer hoy?                     │
│                                                 │
│  ┌────────────────┐    ┌────────────────┐      │
│  │  ⚡ CALCULADORA │    │  🏢 HIDROSTUDIO│      │
│  │     RÁPIDA     │    │   PROFESSIONAL │      │
│  ├────────────────┤    ├────────────────┤      │
│  │ Cálculos       │    │ Proyectos      │      │
│  │ instantáneos   │    │ completos      │      │
│  │ sin registro   │    │ con BD         │      │
│  │                │    │                │      │
│  │ [Ir →]        │    │ [Login →]     │      │
│  └────────────────┘    └────────────────┘      │
└─────────────────────────────────────────────────┘
```

### **Menú de Calculadoras** `/calculators`

```
Calculadoras Disponibles:
  ├─ Método Racional
  ├─ Curvas IDF Uruguay
  ├─ Tiempo de Concentración
  ├─ Coeficiente de Escorrentía Ponderado
  ├─ Manning (Flujo Uniforme)
  ├─ Bernoulli (Energía)
  └─ Orificio/Vertedero
```

---

## 🔄 Migración del Código Actual

### **Lo que YA tenemos:**

✅ **Base de datos completa** (Sesión 1)
- Models, Schemas, Routes
- Funciona perfecto para HidroStudio

✅ **Calculadora Rápida del Método Racional**
- `/rational` actual
- Funciona bien como calculadora rápida
- Solo necesita quitar la integración BD

✅ **Calculadora IDF**
- `/idf` actual
- Ya funciona como calculadora rápida

### **Cambios Necesarios:**

#### **Opción A: Reorganización por Ruta**

```
Estructura Actual:
/rational → Con integración BD (confuso)
/idf → Sin integración BD

Estructura Propuesta:
/calculators/rational → SIN integración BD ⚡
/calculators/idf → SIN integración BD ⚡
/studio/analyze → CON integración BD completa 🏢
```

#### **Opción B: Modo Toggle**

```
Mantener /rational pero con selector:
┌─────────────────────────────────┐
│ Modo: [Rápido ⚡] [Studio 🏢]   │
└─────────────────────────────────┘

Si Rápido → No muestra BD
Si Studio → Muestra integración completa
```

---

## 📋 Plan de Implementación Propuesto

### **Fase 1: Limpiar lo Actual** (1 hora)
- [ ] Quitar integración BD de `/rational` actual
- [ ] Dejar solo calculadora rápida
- [ ] Mover a `/calculators/rational`

### **Fase 2: Crear Estructura Studio** (2 horas)
- [ ] Crear `/studio/dashboard`
- [ ] Crear `/studio/projects/:id`
- [ ] Sistema de autenticación básico (opcional por ahora)

### **Fase 3: Página de Análisis Completo** (3-4 horas)
- [ ] `/studio/watersheds/:id/analyze`
- [ ] Integrar: Datos Cuenca → IDF → Método → Resultado
- [ ] Guardado automático en BD
- [ ] Visualización de resultados

### **Fase 4: Historial y Comparación** (2 horas)
- [ ] `/studio/watersheds/:id/history`
- [ ] Comparación de hidrogramas
- [ ] Exportar reportes

### **Fase 5: Pulido y Documentación** (1 hora)
- [ ] Documentación de usuario
- [ ] Guías de flujo
- [ ] Tests

**Total Estimado:** 9-10 horas de desarrollo

---

## 🎯 Decisiones Pendientes

1. **¿Implementar autenticación ahora o después?**
   - Ahora: Más completo pero más tiempo
   - Después: Desarrollo más rápido, agregar después

2. **¿Reorganizar rutas o usar toggle?**
   - Rutas: Más limpio, mejor SEO
   - Toggle: Más rápido de implementar

3. **¿Priorizar calculadoras o Studio?**
   - Calculadoras: Utilidad inmediata
   - Studio: Visión a largo plazo

4. **¿Modelo de negocio?**
   - Todo gratis
   - Calculadoras gratis, Studio de pago
   - Freemium (límites en proyectos)

---

## 📸 Mockups Pendientes

- [ ] Página principal con 2 opciones
- [ ] Dashboard del Studio
- [ ] Página de análisis completo
- [ ] Vista de comparación de hidrogramas

---

## 💭 Notas y Reflexiones

**Ventajas de la Arquitectura Dual:**
- ✅ Sirve a dos públicos distintos
- ✅ Modelo de negocio claro
- ✅ Escalable
- ✅ Permite monetización futura

**Desventajas:**
- ⚠️ Más código para mantener
- ⚠️ Dos UX diferentes
- ⚠️ Puede confundir a usuarios

**Alternativa Considerada:**
- Solo Studio con período de prueba gratis
- Más simple pero menos accesible

---

**Documento creado:** 2025-11-08
**Estado:** Propuesta para discusión
**Próximo paso:** Decidir qué implementar primero
