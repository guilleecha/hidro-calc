# 🌊 HidroCalc

Plataforma web profesional para cálculos hidrológicos e hidráulicos desarrollada con Django.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2.8-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.16.1-red.svg)](https://www.django-rest-framework.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Descripción

HidroCalc es una plataforma web que proporciona herramientas profesionales para cálculos hidrológicos e hidráulicos, diseñada específicamente para ingenieros civiles, hidrólogos y profesionales del agua.

### **Arquitectura Dual**

El proyecto funciona en dos modos:

#### ⚡ **Calculadoras Rápidas** (Sin autenticación)
- Acceso inmediato sin registro
- Cálculos independientes:
  - Método Racional
  - Curvas IDF Uruguay
  - Tiempo de Concentración
  - Coeficiente de Escorrentía
- Exportación a PDF/Excel

#### 🏢 **HidroStudio Professional** (Con autenticación)
- Gestión completa de proyectos hidrológicos
- Base de datos persistente
- Flujo integrado: Cuenca → IDF → Método → Hidrograma
- Reportes profesionales
- Historial y comparación de análisis

---

## 🚀 Características Principales

- ✅ **API REST completa** con Django Rest Framework
- ✅ **30+ endpoints** para gestión de proyectos, cuencas, tormentas e hidrogramas
- ✅ **Admin panel** de Django configurado
- ✅ **5 modelos de base de datos** (Project, Watershed, DesignStorm, Hydrograph, RainfallData)
- ✅ **Sistema de contexto** para tracking de desarrollo
- ✅ **MCP Servers** configurados (Playwright, GitHub, Context7, etc.)

---

## 🛠️ Stack Tecnológico

### **Backend**
- **Django** 5.2.8
- **Django Rest Framework** 3.16.1
- **SQLite** (desarrollo) / **PostgreSQL** (producción)
- **Celery** 5.5.3 (tareas asíncronas)
- **Redis** 7.0.1 (cache)

### **Frontend**
- Django Templates
- Vanilla JavaScript
- Custom CSS (Tailwind-like)

### **Análisis y Gráficos**
- **NumPy** 2.3.4
- **Pandas** 2.3.3
- **SciPy** 1.16.3
- **Matplotlib** 3.10.7
- **Plotly.js** 6.4.0

### **Exportación**
- **ReportLab** (PDF)
- **OpenPyXL** (Excel)

---

## 📦 Instalación

### **Requisitos**
- Python 3.10+
- Node.js 16+ (para MCP servers)
- Git

### **Pasos**

```bash
# 1. Clonar el repositorio
git clone https://github.com/guilleecha/hidro-calc.git
cd hidro-calc

# 2. Crear entorno virtual
python -m venv .venv

# 3. Activar entorno virtual
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements_django.txt

# 5. Configurar variables de entorno
cp .env.django.example .env.django
# Editar .env.django con tus configuraciones

# 6. Aplicar migraciones
python manage.py migrate

# 7. Crear superusuario (opcional)
python manage.py createsuperuser

# 8. Cargar datos de prueba (opcional)
python manage.py seed_database

# 9. Iniciar servidor de desarrollo
python manage.py runserver
```

Acceder a:
- **App:** http://localhost:8000
- **Admin:** http://localhost:8000/admin
- **API:** http://localhost:8000/api/

---

## 📖 Documentación

- **[CLAUDE.md](CLAUDE.md)** - Guía de arquitectura completa
- **[context/](context/)** - Sistema de contexto del proyecto
  - `current_session.md` - Estado actual
  - `architecture_overview.md` - Overview técnico
  - `next_steps.md` - Roadmap
- **[work_log/](work_log/)** - Documentación de sesiones de desarrollo
- **[MCP_SETUP.md](MCP_SETUP.md)** - Configuración de MCP servers

---

## 🗄️ Modelos de Base de Datos

```
User (Django Auth)
  └─1:N─→ Project
            └─1:N─→ Watershed
                      ├─1:N─→ DesignStorm
                      │         └─1:N─→ Hydrograph
                      └─1:N─→ RainfallData
```

---

## 🔌 API REST

### **Endpoints Principales**

```
GET    /api/projects/                    # Listar proyectos
POST   /api/projects/                    # Crear proyecto
GET    /api/projects/{id}/               # Detalle proyecto
GET    /api/projects/{id}/watersheds/   # Cuencas del proyecto

GET    /api/watersheds/                  # Listar cuencas
POST   /api/watersheds/                  # Crear cuenca

GET    /api/design-storms/               # Listar tormentas
POST   /api/design-storms/               # Crear tormenta

GET    /api/hydrographs/                 # Listar hidrogramas
POST   /api/hydrographs/                 # Crear hidrograma
GET    /api/hydrographs/compare/?ids=1,2,3  # Comparar hidrogramas
```

**Total:** 30+ endpoints disponibles

---

## 🧪 Testing

```bash
# Ejecutar tests
python -m pytest

# Con coverage
python -m pytest --cov=core --cov=api

# Tests específicos
python -m pytest tests/test_models.py
```

---

## 🚧 Estado del Proyecto

**Versión:** 3.0-django
**Estado:** En desarrollo activo

### ✅ Completado
- [x] Migración de FastAPI a Django
- [x] API REST completa con DRF
- [x] Modelos de base de datos
- [x] Django Admin configurado
- [x] Sistema de contexto implementado
- [x] MCP servers instalados

### 🔄 En Progreso
- [ ] Migración de calculadoras a Django templates
- [ ] Implementación de HidroStudio Professional
- [ ] Sistema de autenticación completo

### ⏳ Pendiente
- [ ] Testing automatizado
- [ ] Exportación de reportes PDF/Excel
- [ ] Análisis hidrológico completo
- [ ] Deployment a producción
- [ ] Machine Learning features

Ver [context/next_steps.md](context/next_steps.md) para roadmap detallado.

---

## 👥 Contribución

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo [LICENSE](LICENSE) para más detalles.

---

## 📧 Contacto

**Guillermo Echavarria**
Email: guilleechavarria@gmail.com
GitHub: [@guilleecha](https://github.com/guilleecha)

**Repositorio:** https://github.com/guilleecha/hidro-calc

---

## 🙏 Agradecimientos

- Basado en métodos hidrológicos estándar de ASCE y Ven Te Chow
- Curvas IDF para Uruguay (Rodríguez Fontal)
- Comunidad de Django y DRF

---

**⭐ Si este proyecto te resulta útil, dale una estrella en GitHub!**
