# 📚 Documentation Directory

Documentación detallada del proyecto HidroCalc, separada del CLAUDE.md principal para mantenerlo conciso.

---

## 📁 Structure

### **[coding-standards.md](coding-standards.md)**
**Tamaño:** ~400 líneas

Reglas detalladas de código:
- Tamaños máximos (funciones, modelos, clases, archivos)
- Naming conventions
- Class-Based Views vs Function-Based Views
- Separation of Concerns
- Resource Management
- Pre-commit checklist

**Cuándo consultar:**
- Antes de escribir código nuevo
- Durante code review
- Al refactorizar

---

### **[testing-guide.md](testing-guide.md)**
**Tamaño:** ~450 líneas

Guía completa de testing:
- Testing philosophy y reglas
- Setup de pytest-django
- Fixtures y ejemplos
- Tests de modelos, API, cálculos
- E2E testing con Playwright
- Coverage goals
- TDD workflow

**Cuándo consultar:**
- Antes de escribir tests
- Al configurar testing
- Para ejemplos de buenos tests

---

### **[error-handling.md](error-handling.md)**
**Tamaño:** ~350 líneas

Estrategia de manejo de errores:
- Fail Fast, Log and Continue, Graceful Degradation
- Validación de entrada
- Manejo de transacciones
- Logging best practices
- Anti-patterns
- Exception handler personalizado

**Cuándo consultar:**
- Al manejar errores
- Al implementar validación
- Para configurar logging

---

### **[git-workflow.md](git-workflow.md)**
**Tamaño:** ~500 líneas

Git workflow y safety:
- Git safety protocol
- Commit message format
- Branch strategy
- Pull request protocol
- Manejo de secretos
- Merge vs rebase
- Tags y releases
- Emergency procedures

**Cuándo consultar:**
- Antes de commits
- Al crear PRs
- Para comandos Git específicos
- En emergencias (revert, recovery)

---

### **[architecture-decisions.md](architecture-decisions.md)**
**Tamaño:** ~350 líneas

Decisiones arquitectónicas documentadas:
- Por qué Django sobre FastAPI
- Por qué arquitectura dual
- Por qué SQLite en desarrollo
- Por qué DRF
- Por qué Celery
- Y otras 6 decisiones clave

**Cuándo consultar:**
- Para entender el "por qué" detrás de decisiones
- Al proponer cambios arquitectónicos
- Para onboarding de nuevos developers

---

## 🎯 How to Use This Documentation

### **Al comenzar una sesión:**
1. Leer `context/current_session.md` primero
2. Consultar estos archivos según necesidad

### **Durante desarrollo:**
- `coding-standards.md` - Para reglas de código
- `testing-guide.md` - Para escribir tests
- `error-handling.md` - Para manejar errores

### **Al hacer commits:**
- `git-workflow.md` - Para formato y safety

### **Al tomar decisiones arquitectónicas:**
- `architecture-decisions.md` - Para contexto de decisiones pasadas

---

## 📏 Size Comparison

| File | Lines | Purpose |
|------|-------|---------|
| `CLAUDE.md` (original) | 1,317 | ❌ Demasiado largo |
| `CLAUDE.md` (nuevo) | 304 | ✅ Conciso, referencias |
| **Reduction** | **77%** | **Better readability** |

---

## 🔄 Maintenance

**Al actualizar:**
- Mantener archivos focused en su tema
- Incluir ejemplos prácticos
- Links a documentación oficial cuando sea relevante
- Actualizar fecha de última modificación

**Al agregar nuevo contenido:**
- Considerar si pertenece a archivo existente o nuevo
- Mantener estructura consistente
- Actualizar este README si se agrega archivo nuevo

---

**Última actualización:** 2025-11-08
