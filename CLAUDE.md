# 🌊 HidroCalc - Project Instructions

> Plataforma web profesional para cálculos hidrológicos e hidráulicos con Django 5.2.8

---

## ⚡ QUICK START

**🎯 AL COMENZAR UNA SESIÓN, LEER EN ESTE ORDEN:**

1. **context/current_session.md** ⭐ **PRIMERO** - Estado actual, última tarea, próximos pasos
2. **context/next_steps.md** - Roadmap priorizado
3. Este archivo - Referencia técnica

**💡 TIP:** El sistema de contexto en `/context` mantiene el estado del proyecto entre sesiones.

---

## 📚 Documentation Structure

**Detailed guides in `/docs` folder:**

- **[docs/coding-standards.md](docs/coding-standards.md)** - Tamaños máximos, naming conventions, anti-patterns
- **[docs/testing-guide.md](docs/testing-guide.md)** - Testing philosophy, fixtures, ejemplos
- **[docs/error-handling.md](docs/error-handling.md)** - Error handling strategy, logging
- **[docs/git-workflow.md](docs/git-workflow.md)** - Git safety protocol, commit format, branching
- **[docs/architecture-decisions.md](docs/architecture-decisions.md)** - Por qué Django, arquitectura dual, etc.

**Context files in `/context`:**
- `current_session.md` - Estado actual del proyecto
- `completed_tasks.md` - Historial de sesiones
- `next_steps.md` - Tareas pendientes priorizadas
- `architecture_overview.md` - Overview técnico completo

**Work log in `/work_log`:**
- `00_INDICE_TRABAJO.md` - Índice de todas las sesiones
- `01-07_*.md` - Documentación detallada de cada sesión

---

## 🏗️ Stack Tecnológico

### **Backend**
- Django 5.2.8
- Django Rest Framework 3.16.1
- SQLite (dev) / PostgreSQL (prod)
- Celery 5.5.3 + Redis 7.0.1

### **Frontend**
- Django Templates
- Vanilla JavaScript
- Custom CSS (Tailwind-like)

### **Analysis**
- NumPy 2.3.4, Pandas 2.3.3, SciPy 1.16.3
- Matplotlib 3.10.7, Plotly.js 6.4.0

---

## 🎯 Arquitectura Dual

**⚡ Calculadoras Rápidas** (`/calculators/*`):
- Sin login, no persiste datos
- Método Racional, IDF, Tc, Coeficiente Escorrentía

**🏢 HidroStudio Professional** (`/studio/*`):
- Login requerido, BD persistente
- Gestión de proyectos, flujo integrado completo

**Ver detalles:** `docs/architecture-decisions.md`

---

## 📦 Project Structure

```
hidro-calc/
├── core/              # Models, admin, services
├── api/               # DRF serializers, views, urls
├── calculators/       # Calculadoras rápidas (sin BD)
├── studio/            # HidroStudio Professional (con BD)
├── context/           # Sistema de contexto de sesiones
├── docs/              # Documentación detallada
├── work_log/          # Historial de sesiones
└── hidrocal_project/  # Settings, main urls
```

---

## 🚀 Common Commands

### **Development server:**
```bash
python manage.py runserver

# URLs disponibles:
# http://localhost:8000/admin (admin/admin123)
# http://localhost:8000/api/
# http://localhost:8000/api/docs/ (Swagger UI)
# http://localhost:8000/api/redoc/ (ReDoc)
```

### **Database:**
```bash
python manage.py migrate              # Aplicar migraciones
python manage.py makemigrations       # Crear migraciones
python manage.py seed_database --clear  # Cargar datos de prueba
python manage.py shell                # Django shell
```

### **Testing:**
```bash
python -m pytest                      # Run all tests
python -m pytest --cov=core --cov=api  # With coverage
python -m pytest -v                   # Verbose
```

**Ver detalles:** `docs/testing-guide.md`

---

## 🚨 Critical Rules

### **1. NO PARTIAL IMPLEMENTATION**
❌ NEVER leave TODOs or placeholders
✅ Implement complete functionality or nothing

### **2. NO CODE DUPLICATION**
Always search before writing:
```bash
grep -r "def calculate_" core/
grep -r "class.*Service" */services.py
```

### **3. SEPARATION OF CONCERNS**
- Validation → Serializers/Forms
- Business logic → Services
- HTTP handling → Views
- NO mixed concerns

### **4. TEST EVERY FUNCTION**
- Cada función pública = 1 test mínimo
- NO cheater tests (assert True)
- Use real data, no mocks for DB

### **5. SIZE LIMITS**
- Functions ≤ 50 lines
- Models ≤ 15 fields (split if needed)
- Classes ≤ 10 public methods
- Files ≤ 500 lines
- Views > 30 lines → use CBV

**Ver más:** `docs/coding-standards.md`

---

## ⚠️ Git Safety

### **NEVER:**
- ❌ Update git config
- ❌ Force push to main/master
- ❌ Skip hooks (--no-verify)
- ❌ Commit without explicit user request
- ❌ Commit secrets (.env, credentials, *.key)

### **Commit format:**
```bash
git commit -m "$(cat <<'EOF'
<type>: <summary>

[optional body]

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

**Ver detalles:** `docs/git-workflow.md`

---

## 🧪 Error Handling Strategy

- **Fail Fast:** Config crítica (DB, SECRET_KEY, models requeridos)
- **Log and Continue:** Features opcionales (Redis, Celery)
- **Graceful Degradation:** Servicios externos no críticos
- **User-Friendly Messages:** Nunca mostrar stack traces al usuario

**Ver detalles:** `docs/error-handling.md`

---

## 📊 Database Models

```
User (Django Auth)
  └─1:N─→ Project
            └─1:N─→ Watershed
                      ├─1:N─→ DesignStorm
                      │         └─1:N─→ Hydrograph
                      └─1:N─→ RainfallData
```

**Primary Keys:** Django BigAutoField (integer auto-increment)
**Ver detalles:** `context/architecture_overview.md`

---

## 🔌 API Endpoints

**30+ endpoints disponibles:**

```
GET    /api/projects/
POST   /api/projects/
GET    /api/projects/{id}/
GET    /api/projects/{id}/watersheds/

GET    /api/watersheds/
POST   /api/watersheds/
GET    /api/watersheds/{id}/stats/

GET    /api/design-storms/
POST   /api/design-storms/
GET    /api/design-storms/?watershed_id=X

GET    /api/hydrographs/
POST   /api/hydrographs/
GET    /api/hydrographs/compare/?ids=1,2,3
```

**Documentación completa:** http://localhost:8000/api/docs/

---

## 💡 Development Workflow

### **1. Starting a task:**
```bash
# Read context first
cat context/current_session.md
cat context/next_steps.md

# Create feature branch
git checkout -b feature/task-name
```

### **2. During development:**
- Write tests FIRST (TDD)
- Keep functions < 50 lines
- Separate business logic to services
- NO code duplication

### **3. Before committing:**
```bash
# Run tests
python -m pytest

# Check code style
python -m flake8

# Review changes
git diff

# Commit (only when user asks!)
```

**Ver detalles:** `docs/git-workflow.md`

---

## 🎯 Tone and Behavior

- **Be Critical:** Señalar errores y mejores alternativas
- **Be Skeptical:** Cuestionar decisiones subóptimas
- **Be Concise:** Respuestas directas, sin florituras
- **No Flattery:** No dar cumplidos innecesarios
- **Ask Questions:** Ante duda, preguntar en lugar de asumir

---

## 📝 Al Finalizar una Sesión

**SIEMPRE actualizar:**
1. `context/current_session.md` - Estado nuevo, última tarea completada
2. `context/completed_tasks.md` - Agregar sesión si es significativa
3. `work_log/` - Crear archivo de sesión si cambios importantes

---

## 🔗 Quick References

- **Repository:** https://github.com/guilleecha/hidro-calc
- **Django Docs:** https://docs.djangoproject.com/en/5.2/
- **DRF Docs:** https://www.django-rest-framework.org/
- **Swagger UI:** http://localhost:8000/api/docs/

---

**Última actualización:** 2025-11-08
**Versión:** 3.0-django
**Estado:** En desarrollo activo
