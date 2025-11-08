# 🏗️ Architecture Decisions - HidroCalc

Documentación de decisiones arquitectónicas y su justificación.

---

## 🎯 Decisiones de Diseño Importantes

### **1. ¿Por qué Django sobre FastAPI?**

**Decisión:** Migrar de FastAPI a Django

**Razones:**
- **Visión a largo plazo:** ML, análisis de datos, proyectos complejos
- **Admin Panel:** Gestión de datos sin código adicional (Django Admin)
- **ORM Maduro:** Más estable para proyectos grandes con relaciones complejas
- **Ecosistema:** Miles de paquetes probados y maduros
- **Celery Integration:** Procesamiento ML asíncrono mejor integrado
- **Escalabilidad:** Mejor para proyectos que crecen en complejidad

**Trade-offs:**
- ✅ Ganamos: Admin panel, ORM robusto, ecosystem maduro
- ⚠️ Perdemos: Velocidad pura de FastAPI, async nativo
- ✅ Justificado: Proyecto de gestión hidrológica requiere robustez > velocidad

---

### **2. ¿Por qué Arquitectura Dual?**

**Decisión:** Dos modos distintos (Calculadoras Rápidas + HidroStudio Professional)

#### **⚡ Calculadoras Rápidas** (`/calculators/*`)
- Sin login requerido
- No persiste datos
- Acceso inmediato

#### **🏢 HidroStudio Professional** (`/studio/*`)
- Login requerido
- Base de datos persistente
- Flujo integrado completo

**Razones:**
- **Dos públicos distintos:** Usuarios rápidos vs profesionales en proyectos
- **Modelo de negocio:** Calculadoras gratis, Studio de pago (futuro)
- **Escalabilidad:** Permite monetización sin afectar herramientas gratuitas
- **UX diferenciada:** Experiencias optimizadas para cada caso de uso

**Trade-offs:**
- ✅ Ganamos: Flexibilidad, modelo de negocio, audiencia amplia
- ⚠️ Mantenemos: Dos flujos separados de código
- ✅ Justificado: Maximiza valor para ambos tipos de usuarios

---

### **3. ¿Por qué SQLite en desarrollo?**

**Decisión:** SQLite para desarrollo, PostgreSQL para producción

**Razones SQLite (desarrollo):**
- **Simplicidad:** No requiere servicios externos
- **Portabilidad:** Base de datos en un archivo
- **Velocidad:** Setup instantáneo
- **Facilidad:** Perfecto para desarrollo y testing

**Migración a PostgreSQL (producción):**
- **Concurrencia:** Mejor manejo de múltiples usuarios
- **Features avanzadas:** Full-text search, JSON fields, arrays
- **Escalabilidad:** Mejor para datasets grandes
- **Hosting:** Soportado por todas las plataformas cloud

**Trade-offs:**
- ✅ Ganamos: Desarrollo rápido, testing sencillo
- ⚠️ Mantenemos: Diferencia dev/prod (mínima con Django ORM)
- ✅ Justificado: Workflow de desarrollo optimizado

---

### **4. ¿Por qué Django Rest Framework?**

**Decisión:** DRF para API REST

**Razones:**
- **Integration:** Perfecto con Django models
- **Serializers:** Validación robusta, similar a Pydantic
- **Viewsets:** CRUD en pocas líneas
- **Browsable API:** Interface web automática para testing
- **Authentication:** JWT, OAuth, Session - todos integrados
- **Documentation:** drf-spectacular para Swagger/ReDoc automático

**Alternativas consideradas:**
- FastAPI: Más rápido, pero ya decidimos Django como base
- Django Ninja: Más nuevo, menos maduro que DRF
- Plain Django Views: Mucho más código manual

**Trade-offs:**
- ✅ Ganamos: Ecosystem maduro, documentación excelente, patterns establecidos
- ⚠️ Perdemos: Algo de performance (mínimo para nuestro caso)
- ✅ Justificado: Productividad > Performance para este proyecto

---

### **5. ¿Por qué Celery para tareas asíncronas?**

**Decisión:** Celery + Redis para procesamiento asíncrono

**Casos de uso:**
- Generación de reportes PDF/Excel pesados
- Entrenamiento de modelos ML
- Procesamiento de datasets grandes
- Cálculos hidrológicos complejos

**Razones:**
- **Distributed:** Puede escalar a múltiples workers
- **Scheduling:** Tareas programadas con celery-beat
- **Retry:** Lógica de reintentos integrada
- **Monitoring:** Flower para visualización

**Alternativas consideradas:**
- Django Q: Más simple pero menos features
- Huey: Lightweight pero menos documentación
- RQ: Simple pero menos robusto

**Trade-offs:**
- ✅ Ganamos: Escalabilidad, robustez, monitoreo
- ⚠️ Mantenemos: Servicio adicional (Redis)
- ✅ Justificado: Necesario para ML y reportes pesados

---

### **6. ¿Por qué Class-Based Views?**

**Decisión:** Preferir CBV para vistas > 30 líneas

**Razones:**
- **DRY:** Herencia evita duplicación
- **Mixins:** Funcionalidad compartida (LoginRequired, Permissions)
- **Patterns:** Patterns establecidos de Django (ListView, DetailView, etc.)
- **Testing:** Más fácil de testear con herencia
- **Mantenibilidad:** Cambios en un lugar afectan todas las vistas heredadas

**Cuándo usar FBV:**
- Vistas simples < 20 líneas
- Lógica muy específica
- API endpoints simples

**Trade-offs:**
- ✅ Ganamos: Menos código, más reusable
- ⚠️ Perdemos: Algo de claridad para beginners
- ✅ Justificado: Proyecto de mediano-largo plazo

---

### **7. ¿Por qué separar Serializers por operación?**

**Decisión:** Serializers diferentes para Create/List/Detail

**Ejemplo:**
```python
ProjectListSerializer  # Solo campos esenciales
ProjectDetailSerializer  # Incluye relaciones (watersheds, etc.)
ProjectCreateSerializer  # Solo campos writeables
```

**Razones:**
- **Performance:** List no carga relaciones innecesarias
- **Security:** Create no expone campos read-only
- **Clarity:** Cada serializer tiene un propósito claro
- **Validation:** Reglas de validación diferentes por operación

**Trade-offs:**
- ✅ Ganamos: Performance, seguridad, claridad
- ⚠️ Mantenemos: Más archivos/clases
- ✅ Justificado: Proyecto profesional requiere este nivel de control

---

### **8. ¿Por qué Services Layer?**

**Decisión:** Separar lógica de negocio en `services.py`

**Estructura:**
```
api/views.py         # HTTP handling, validation
core/services.py     # Business logic
core/models.py       # Data models
```

**Razones:**
- **Testability:** Services se testean sin HTTP
- **Reusability:** Misma lógica desde API, admin, Celery tasks
- **Clarity:** Vistas limpias, lógica concentrada
- **Maintenance:** Cambios de lógica no afectan vistas

**Ejemplo:**
```python
# core/services.py
def calculate_watershed_metrics(watershed):
    # Lógica compleja aquí
    return metrics

# api/views.py (limpia)
def watershed_metrics_view(request, pk):
    watershed = get_object_or_404(Watershed, pk=pk)
    metrics = calculate_watershed_metrics(watershed)
    return Response(metrics)
```

**Trade-offs:**
- ✅ Ganamos: Testing, reusabilidad, claridad
- ⚠️ Mantenemos: Capa adicional
- ✅ Justificado: Esencial para proyectos complejos

---

### **9. ¿Por qué contexto de sesión?**

**Decisión:** Sistema de contexto en `/context` folder

**Archivos:**
- `current_session.md` - Estado actual
- `completed_tasks.md` - Historial
- `next_steps.md` - Roadmap
- `architecture_overview.md` - Visión técnica

**Razones:**
- **Continuidad:** Retomar trabajo entre sesiones
- **Documentation:** Auto-documentación del progreso
- **Planning:** Roadmap claro y priorizado
- **Communication:** Claude Code puede leer contexto y continuar

**Trade-offs:**
- ✅ Ganamos: Continuidad perfecta entre sesiones
- ⚠️ Mantenemos: Archivos adicionales a actualizar
- ✅ Justificado: Esencial para proyectos de largo plazo

---

### **10. ¿Por qué drf-spectacular sobre otras opciones?**

**Decisión:** drf-spectacular para documentación API

**Alternativas:**
- drf-yasg: Más antiguo, menos features
- Swagger UI manual: Mucho trabajo manual
- ReDoc manual: Idem

**Razones:**
- **OpenAPI 3.0:** Estándar moderno
- **Auto-generation:** Schema generado de serializers
- **Swagger + ReDoc:** Ambas interfaces incluidas
- **Customization:** Alta personalización de metadata
- **Maintenance:** Activamente mantenido

**Trade-offs:**
- ✅ Ganamos: Documentación automática siempre actualizada
- ⚠️ Mantenemos: Dependencia adicional
- ✅ Justificado: Documentación es crítica para APIs

---

### **11. ¿Por qué MCP Servers?**

**Decisión:** Playwright, Filesystem, GitHub, PostgreSQL, Context7

**Razones:**
- **Playwright:** Testing E2E automatizado de calculadoras
- **Filesystem:** Operaciones avanzadas de archivos
- **GitHub:** Integración con repositorio
- **PostgreSQL:** Gestión de BD (cuando migremos)
- **Context7:** Documentación de librerías actualizada

**Trade-offs:**
- ✅ Ganamos: Herramientas de desarrollo potentes
- ⚠️ Mantenemos: Setup adicional
- ✅ Justificado: Mejora significativa en productividad

---

## 🔮 Futuras Decisiones Pendientes

### **Autenticación:**
- Django Allauth vs django-rest-auth
- Social login (Google, GitHub) - ¿necesario?

### **Deployment:**
- Railway vs Render vs AWS
- Docker containerization - ¿sí o no?

### **Frontend:**
- Mantener Django templates vs migrar a React/Vue
- Tailwind CSS vs Material UI

### **Analytics:**
- Google Analytics vs PostHog vs Plausible

### **Monitoring:**
- Sentry para error tracking
- DataDog vs NewRelic para performance

---

**Última actualización:** 2025-11-08
