# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## ⚡ Quick Start

**When starting a session, read in this order:**

1. **`context/current_session.md`** - Current state, last task, next steps
2. **`context/next_steps.md`** - Prioritized roadmap
3. This file - Technical reference

The `/context` system maintains project state between sessions.

---

## 🏗️ High-Level Architecture

### Django 5.2.8 + DRF Hydrological Platform

**Dual Architecture** (key design decision):

#### ⚡ Quick Calculators (`/calculators/*`)
- No login required
- Stateless calculations (Rational Method, IDF Curves, Tc, Runoff Coefficient)
- No database persistence
- PDF/Excel export

#### 🏢 HidroStudio Professional (`/studio/*`)
- Login required
- Full project management with database persistence
- Integrated workflow: Project → Watershed → Storm → Hydrograph
- Professional reports and analysis comparison
- **Status:** Phase 1 (Dashboard) complete, Phase 2 (Visualizations) next

See `docs/architecture-decisions.md` for rationale.

### Modular App Structure

**Models distributed across focused apps:**
- `projects/models.py` - Project model
- `watersheds/models.py` - Watershed model
- `hydrology/models.py` - DesignStorm, Hydrograph, RainfallData
- `core/` - Re-exports all models for backward compatibility

**Why modular?** Separation of concerns, clearer dependencies, easier testing.

### Database Schema

```
User (Django Auth)
  └─1:N─→ Project (projects app)
            └─1:N─→ Watershed (watersheds app)
                      ├─1:N─→ DesignStorm (hydrology app)
                      │         └─1:N─→ Hydrograph (hydrology app)
                      └─1:N─→ RainfallData (hydrology app)
```

**Key Details:**
- 5 models across 3 apps (projects, watersheds, hydrology)
- Primary keys: Django BigAutoField (integer auto-increment)
- Time series stored in JSON fields (`hydrograph_data`, `rainfall_series`)
- Cascading deletes: `CASCADE` for dependent data, `PROTECT` for critical refs

### API Structure

30+ REST endpoints via Django Rest Framework:
- `api/serializers.py` (~380 lines) - 15+ serializers
- `api/views.py` (~300 lines) - 5 ViewSets
- Full Swagger/ReDoc documentation at `/api/docs/`
- **Critical Gap:** Manual hydrograph creation only - auto-calculation service needed (see `docs/hydrograph-calculation.md`)

---

## 🚀 Common Commands

### Development
```bash
# Start server
python manage.py runserver

# Access points:
# http://localhost:8000/admin (admin/admin123)
# http://localhost:8000/api/docs/ (Swagger UI)
```

### Database
```bash
python manage.py migrate                    # Apply migrations
python manage.py makemigrations             # Create migrations
python manage.py seed_database --clear      # Load test data
python manage.py shell                      # Django shell
```

### Testing
```bash
python -m pytest                                      # All tests
python -m pytest tests/test_models.py::TestProject   # Single test
python -m pytest --cov=core --cov=api                # With coverage
python -m pytest -v -k "test_watershed"              # Match pattern
```

### Dependencies
```bash
pip install -r requirements_django.txt
```

---

## 🚨 Critical Development Rules

### 1. NO PARTIAL IMPLEMENTATION
Never leave TODOs, placeholders, or incomplete functionality. Implement fully or not at all.

### 2. NO CODE DUPLICATION
Always search before implementing:
```bash
# Windows
findstr /s /i "def calculate_" *.py
findstr /s /i "class.*Service" *.py

# Unix/Git Bash
grep -r "def calculate_" --include="*.py"
grep -r "class.*Service" */services.py
```

### 3. STRICT SEPARATION OF CONCERNS
- **Validation** → Serializers/Forms
- **Business logic** → Services (create `app/services/*.py` for complex logic)
- **HTTP handling** → Views
- **Database** → Models (with custom managers if needed)

NO mixed concerns. NO business logic in serializers.

**Example service location:** Hydrograph calculation → `hydrology/services/hydrograph_calculator.py`

### 4. SIZE LIMITS (Enforced)
- Functions ≤ 50 lines
- Models ≤ 15 fields (split if needed)
- Classes ≤ 10 public methods
- Files ≤ 500 lines
- Views > 30 lines → use Class-Based Views

### 5. TESTING REQUIRED
Every public function needs at least one test. No placeholder tests (`assert True`). Use real data, minimal mocking for database tests.

See `docs/coding-standards.md` for detailed rules and examples.

---

## 📁 Project Structure

```
hidro-calc/
├── context/           # Session state (current_session.md, next_steps.md, etc.)
├── docs/              # Detailed guides (coding-standards, testing, git-workflow)
├── work_log/          # Development session history
├── projects/          # Project model + admin
├── watersheds/        # Watershed model + admin
├── hydrology/         # DesignStorm, Hydrograph, RainfallData models
├── core/              # Re-exports, utilities, management commands
├── api/               # DRF - serializers, views, urls
├── calculators/       # Quick calculators (Rational, IDF, Tc)
├── studio/            # HidroStudio Professional (Phase 1 complete)
├── templates/         # Django templates (base, auth, studio)
├── static/            # CSS, JS, images
└── hidrocal_project/  # Django settings, main urls
```

**Note:** 86 Python files total (excluding .venv and backups)

---

## ⚠️ Git Safety Protocol

**NEVER:**
- Update git config
- Force push to main/master
- Skip hooks (`--no-verify`)
- Commit without explicit user request
- Commit secrets (`.env`, credentials, `*.key`)

**Commit format:**
```bash
git commit -m "$(cat <<'EOF'
<type>: <summary>

[optional body]

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

See `docs/git-workflow.md` for details.

---

## 🔧 Error Handling Strategy

- **Fail Fast:** Critical config (DB, SECRET_KEY, required models)
- **Log and Continue:** Optional features (Redis, Celery)
- **Graceful Degradation:** Non-critical external services
- **User-Friendly Messages:** Never expose stack traces to users

See `docs/error-handling.md` for implementation patterns.

---

## 🔌 Active MCP Servers

4 MCP servers configured for enhanced development:

- **Playwright** (v0.0.46) - E2E testing, UI validation
- **Filesystem** (v2025.8.21) - Advanced file operations
- **GitHub** (v2025.4.8) - Repository integration
- **Context7** (v1.0.26) - Up-to-date library documentation

See `docs/MCP_SETUP.md` for configuration details.

---

## 💡 Development Workflow

### Starting a Task
```bash
# 1. Read context (CRITICAL - do this first!)
cat context/current_session.md
cat context/next_steps.md

# 2. Search before implementing (avoid duplication)
# Windows:
findstr /s /i "def calculate_" *.py
findstr /s /i "class.*Serializer" *.py
# Unix/Git Bash:
grep -r "def calculate_" --include="*.py"
grep -r "class.*Serializer" api/

# 3. Create feature branch (if significant work)
git checkout -b feature/task-name
```

### During Development
- **ALWAYS check `context/next_steps.md`** for current priorities
- Write tests FIRST (TDD preferred)
- Keep functions < 50 lines
- Extract business logic to `app/services/` modules
- Check Django admin after model changes
- For hydrograph work: See `docs/hydrograph-calculation.md` for detailed implementation plan

### Before Committing
```bash
python -m pytest                        # Run tests
python manage.py makemigrations --check # Verify migrations
git diff                                # Review changes
# Commit only when user explicitly asks
```

---

## 📝 Session End Protocol

**Always update:**
1. `context/current_session.md` - New state, completed task
2. `context/completed_tasks.md` - Add session if significant
3. `work_log/` - Create session file if important changes

---

## 🎯 Working Style

- **Be critical:** Point out errors and better alternatives
- **Be skeptical:** Question suboptimal decisions
- **Be concise:** Direct answers, no unnecessary elaboration
- **Ask questions:** Clarify rather than assume

---

## 📚 Documentation

**Detailed technical guides:**
- `docs/coding-standards.md` - Size limits, naming, anti-patterns
- `docs/testing-guide.md` - Testing philosophy, fixtures, examples
- `docs/error-handling.md` - Error strategies, logging patterns
- `docs/git-workflow.md` - Git safety, commit format, branching
- `docs/architecture-decisions.md` - Why Django, dual architecture

**Context tracking:**
- `context/architecture_overview.md` - Complete technical overview
- `context/current_session.md` - Current project state
- `context/next_steps.md` - Prioritized roadmap

---

## 🔗 Quick Links

- **Repository:** https://github.com/guilleecha/hidro-calc
- **Django Docs:** https://docs.djangoproject.com/en/5.2/
- **DRF Docs:** https://www.django-rest-framework.org/

---

**Last Updated:** 2025-11-09
**Version:** 3.0-django
**Status:** Active development

---

## 🎯 Current Priority

**Next Task:** Hydrograph Calculation System (Sprint 1)
- Implement hietograph generation (Alternating Block method)
- Implement rainfall excess calculation (Rational & SCS)
- See `docs/hydrograph-calculation.md` for complete roadmap
- See `context/next_steps.md` for detailed task breakdown
