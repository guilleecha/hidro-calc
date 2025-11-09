# 🎯 Próximos Pasos - HidroCalc

**Última actualización:** 2025-11-09
**Estado actual:** HidroStudio Phase 1 completado

---

## 🔥 ALTA PRIORIDAD (Hacer Ahora)

### 1. **Sistema de Cálculo de Hidrogramas** ⭐⭐⭐ CRÍTICO
**Estimado:** 8-12 días (ver plan detallado en `docs/hydrograph-calculation.md`)
**Estado:** En documentación - Listo para implementar
**Última actualización:** 2025-11-09

**Objetivo:** Implementar cálculo automatizado de hidrogramas a partir de tormentas de diseño

**Problema actual:**
- Datos de seed_database eran completamente incorrectos (0.73mm en 24h para Tr=10 años) ❌
- Endpoint `/api/hydrographs/` requiere enviar hidrograma completo ya calculado (no práctico)
- NO existe servicio de cálculo automático de hidrogramas
- Falta herramienta para ponderar C y CN por área de subcuencas

**Solución implementada/en progreso:**
- ✅ Corregidas curvas IDF en seed_database usando Rodríguez Fontal (1980) - Datos ahora realistas (127mm/24h)
- ✅ Home page con login funcional
- ✅ Templates de autenticación profesionales
- ✅ Configuración de redirects después de login
- 🔄 **PRÓXIMO:** Implementar servicios de cálculo de hidrogramas

**Plan de implementación (ver docs/hydrograph-calculation.md):**

**Sprint 1: Hietogramas y Lluvia Efectiva** (2-3 días) ⭐ SIGUIENTE
- [ ] Crear `core/services/hyetograph.py`
  - [ ] `generate_alternating_block()` - Distribución temporal de lluvia
  - [ ] `generate_chicago()` - Método de Chicago (opcional)
- [ ] Crear `core/services/rainfall_excess.py`
  - [ ] `calculate_rainfall_excess_rational()` - Pe = C × P
  - [ ] `calculate_rainfall_excess_scs()` - SCS Curve Number (futuro)
- [ ] Tests unitarios para ambos módulos

**Sprint 2: Hidrograma Racional** (2-3 días)
- [ ] Crear `core/services/hydrograph_calculator.py`
  - [ ] `calculate_hydrograph_rational()` - Hidrograma triangular
  - [ ] `calculate_hydrograph()` - Orquestador principal
- [ ] Integración: hietograma → lluvia efectiva → hidrograma
- [ ] Tests de integración

**Sprint 3: API Endpoint** (1-2 días)
- [ ] Crear `POST /api/hydrographs/calculate/`
  - Body: `{design_storm_id, method, name, custom_params}`
  - Returns: Hydrograph completo calculado y guardado
- [ ] Serializers de request/response
- [ ] Manejo de errores robusto
- [ ] Actualizar documentación Swagger

**Sprint 4: Herramienta de Ponderación** (2-3 días)
- [ ] Crear `core/services/parameter_weighting.py`
  - [ ] `calculate_weighted_C()` - C ponderado por área
  - [ ] `calculate_weighted_CN()` - CN ponderado por área
- [ ] Endpoint `POST /api/watersheds/calculate-weighted-parameters/`
- [ ] UI en HidroStudio para calcular parámetros ponderados
- [ ] Tests

**Sprint 5: Testing End-to-End** (1 día)
- [ ] Flujo completo: Login → Dashboard → Seleccionar tormenta → Calcular hidrograma → Visualizar
- [ ] Comparación de múltiples hidrogramas
- [ ] Verificar datos realistas en visualizaciones
- [ ] Documentación de usuario

**Flujo de usuario objetivo:**
```
1. Login → Dashboard
2. Seleccionar proyecto → cuenca → tormenta de diseño
3. Click "Calcular Hidrograma"
4. Seleccionar método (Racional/SCS/Sintético)
5. Revisar/ajustar parámetros (C, NC, Tc)
6. Sistema genera automáticamente:
   - Hietograma (distribución temporal de lluvia)
   - Lluvia efectiva (con pérdidas por infiltración)
   - Hidrograma resultante
7. Visualización interactiva con Plotly
8. Comparar con otros métodos
```

**Archivos a crear:**
- `core/services/hyetograph.py` (nuevo)
- `core/services/rainfall_excess.py` (nuevo)
- `core/services/hydrograph_calculator.py` (nuevo)
- `core/services/parameter_weighting.py` (nuevo)
- `tests/core/test_hyetograph.py` (nuevo)
- `tests/core/test_rainfall_excess.py` (nuevo)
- `tests/core/test_hydrograph_calculator.py` (nuevo)

**Archivos a modificar:**
- `api/views.py` - Agregar action `calculate()` en HydrographViewSet
- `api/serializers.py` - Agregar serializer para request de cálculo
- `studio/views.py` - Integrar con UI (futuro)
- `templates/studio/dashboard.html` - Botón "Calcular Hidrograma" (futuro)

**Beneficios:**
- ✅ Datos de prueba ahora son realistas (IDF Uruguay)
- ✅ Usuario puede generar hidrogramas automáticamente
- ✅ Comparación de metodologías (Racional vs SCS vs Sintético)
- ✅ Herramienta profesional de ponderación de parámetros
- ✅ Base sólida para análisis hidrológico completo

**Referencias técnicas:**
- Ver documento completo: `docs/hydrograph-calculation.md`
- Curvas IDF: `calculators/services/idf.py` (Rodríguez Fontal 1980)
- Método Racional: `calculators/services/rational.py`

---

### 2. **Actualizar seed_database Command**
**Estimado:** 30 min
**Estado:** Pendiente

**Tareas:**
- [ ] Asignar owner automáticamente (admin user)
- [ ] Generar hidrogramas de ejemplo (mínimo 3 por tormenta)
- [ ] Calcular stats para stats cards
- [ ] Agregar opciones de configuración

**Archivos a modificar:**
- `core/management/commands/seed_database.py`

**Beneficio:**
- Dashboard muestra datos reales en stats cards
- Testing más completo y realista

---

## 🟡 MEDIA PRIORIDAD (Hacer Pronto)

### 3. **HidroStudio Phase 3: Comparación Avanzada**
**Estimado:** 2-3 horas
**Estado:** Pendiente (requiere Phase 2)

**Tareas:**
- [ ] Vista de comparación mejorada con multi-select
- [ ] Tabla comparativa (Q pico, T pico, volumen, diferencias %)
- [ ] Análisis de sensibilidad (variación de C, NC, Tc)
- [ ] Recomendaciones basadas en comparación

**Archivos a crear/modificar:**
- `templates/studio/hydrograph_compare.html` (mejorar)
- `studio/views.py` (mejorar hydrograph_compare)

---

### 4. **HidroStudio Phase 4: CRUD Completo**
**Estimado:** 3-4 horas
**Estado:** Pendiente

**Tareas:**
- [ ] Forms Django para Project, Watershed, DesignStorm
- [ ] Vistas de crear/editar (CreateView, UpdateView)
- [ ] UI para calcular hidrogramas con diferentes métodos
- [ ] Guardar análisis
- [ ] Validación de datos

**Archivos a crear:**
- `studio/forms.py`
- `templates/studio/project_form.html`
- `templates/studio/watershed_form.html`
- `templates/studio/storm_form.html`

---

### 5. **Configurar Testing Automatizado**
**Estimado:** 3-4 horas
**Requiere:** pytest-django, Playwright

**Tareas:**
- [ ] Setup pytest-django
- [ ] Configurar fixtures
- [ ] Tests unitarios de modelos (5 tests)
- [ ] Tests de serializers (15+ tests)
- [ ] Tests de API endpoints (30+ tests)
- [ ] Tests E2E con Playwright (opcional)
- [ ] Setup CI/CD con GitHub Actions (futuro)

**Beneficio:**
- Detectar bugs temprano
- Refactoring seguro
- Documentación viva del comportamiento

---

### 6. **Implementar Autenticación Completa**
**Estimado:** 3 horas
**Requiere:** Django Allauth, JWT

**Tareas:**
- [ ] Configurar Django Allauth
- [ ] Templates de login/registro
- [ ] JWT para API
- [ ] Permisos por usuario
- [ ] Vincular proyectos con usuarios
- [ ] Middleware de autenticación

**Beneficio:**
- Usuarios pueden guardar sus proyectos
- Seguridad de la API
- Base para HidroStudio Professional

---

## 🟢 BAJA PRIORIDAD (Backlog)

### 7. **HidroStudio Phase 5: Exportación**
**Estimado:** 2-3 horas
**Estado:** Pendiente

**Tareas:**
- [ ] PDF con reportlab (incluir gráficos)
- [ ] Excel con openpyxl (múltiples hojas)
- [ ] CSV para otros software (HEC-RAS, SWMM)
- [ ] Descarga de archivos

---

### 8. **Migrar a PostgreSQL**
**Estimado:** 2 horas
**Requiere:** PostgreSQL instalado

**Tareas:**
- [ ] Instalar PostgreSQL
- [ ] Crear base de datos
- [ ] Actualizar DATABASE_URL en .env
- [ ] Migrar datos de SQLite
- [ ] Testing de queries

**Beneficio:**
- Mejor para producción
- Queries más eficientes
- Soporte para funciones avanzadas

---

### 9. **Deployment en Producción**
**Estimado:** 4-6 horas
**Requiere:** Servidor (Railway, Render, AWS)

**Tareas:**
- [ ] Configurar variables de entorno
- [ ] Configurar static files (Whitenoise)
- [ ] Configurar Gunicorn
- [ ] Setup PostgreSQL en producción
- [ ] Configurar dominio
- [ ] SSL/HTTPS
- [ ] Monitoreo y logs

---

### 10. **Machine Learning Features**
**Estimado:** 8-10 horas
**Requiere:** Scikit-learn, Celery

**Tareas:**
- [ ] Modelo de predicción de caudales
- [ ] Training asíncrono con Celery
- [ ] API para predicciones
- [ ] Visualización de resultados

---

### 11. **Colaboración Multi-Usuario**
**Estimado:** 5-6 horas
**Requiere:** Permisos, WebSockets (opcional)

**Tareas:**
- [ ] Compartir proyectos entre usuarios
- [ ] Roles (owner, editor, viewer)
- [ ] Comentarios en análisis
- [ ] Notificaciones (opcional)

---

## 🎯 Ruta Recomendada (Orden Sugerido)

```
✅ Sesión 1-7: Base del Proyecto              ← COMPLETADO
✅ Sesión 8: HidroStudio Phase 1              ← COMPLETADO
🔥 Sesión 9: HidroStudio Phase 2 (Plotly)    ← PRÓXIMO (3-4h)
   Sesión 10: seed_database mejorado (30min)
   Sesión 11: HidroStudio Phase 3 (2-3h)
   Sesión 12: HidroStudio Phase 4 (3-4h)
   Sesión 13: HidroStudio Phase 5 (2-3h)
   Sesión 14: Testing Setup (3-4h)
   Sesión 15: Autenticación (3h)
   Sesión 16: PostgreSQL + Deploy (6-8h)
```

**Progreso HidroStudio:**
- ✅ Phase 1: Dashboard básico (2h)
- 🔥 Phase 2: Visualizaciones (3-4h) - PRÓXIMO
- ⏳ Phase 3: Comparación (2-3h)
- ⏳ Phase 4: CRUD (3-4h)
- ⏳ Phase 5: Exportación (2-3h)

**Total HidroStudio:** ~14-18 horas (2h completadas)

---

## 📊 Métricas de Progreso

**Completado:** 60%
- ✅ Base de datos (Django ORM)
- ✅ API REST (30+ endpoints)
- ✅ Admin panel configurado
- ✅ MCP instalado
- ✅ Proyecto organizado (multi-app)
- ✅ GitHub repository
- ✅ API Documentation (Swagger/ReDoc)
- ✅ HidroStudio Phase 1 (Dashboard básico)
- ✅ Arquitectura multi-app (projects, watersheds, hydrology)
- ✅ CSS modular
- ✅ Calculadoras básicas (Rational, IDF)

**En Progreso:** 10%
- 🔄 HidroStudio Phase 2 (Visualizaciones con Plotly.js)

**Pendiente:** 30%
- ⏳ HidroStudio Phase 3-5
- ⏳ Testing extendido
- ⏳ Autenticación
- ⏳ Deployment

---

**Actualizado:** 2025-11-09
**Próxima acción:** Phase 2 - Integrar Plotly.js y visualizaciones
**Última sesión:** #10 - HidroStudio Phase 1 completado
