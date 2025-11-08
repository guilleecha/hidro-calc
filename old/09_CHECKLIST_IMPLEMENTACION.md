# ✅ CHECKLIST DE IMPLEMENTACIÓN - HidroCalc v2.0

## 📋 RESUMEN EJECUTIVO

**Objetivo**: Agregar base de datos jerárquica a HidroCalc para guardar y comparar hidrogramas  
**Archivos a crear**: 5 archivos Python + configuración  
**Tiempo estimado**: 3-4 horas  
**Complejidad**: Media  
**Dependencias nuevas**: sqlalchemy, python-dotenv  

---

## 🎯 FASE 1: PREPARACIÓN (30 minutos)

### ☐ 1.1 Revisar arquitectura actual
- [ ] Abrir `C:\myprojects\hidro-calc\src\main.py`
- [ ] Verificar que FastAPI está funcionando
- [ ] Confirmar que el servidor corre en `http://localhost:8000`

### ☐ 1.2 Preparar entorno
- [ ] Abrir terminal en `C:\myprojects\hidro-calc`
- [ ] Activar venv: `.\venv\Scripts\activate`
- [ ] Crear carpeta `.vscode` si no existe (opcional, para debugging)

### ☐ 1.3 Actualizar requirements.txt
```bash
# Abrir C:\myprojects\hidro-calc\requirements.txt
# Agregar al final:

sqlalchemy==2.0.23
python-dotenv==1.0.0
pytest==7.4.3
pytest-asyncio==0.21.1

# Instalar
pip install -r requirements.txt
```
- [ ] Verificar que sqlalchemy se instala sin errores
- [ ] Confirmar versión: `pip show sqlalchemy`

---

## 🗂️ FASE 2: CREAR ARCHIVOS (1 hora)

### ☐ 2.1 Crear archivo `.env`
**Ubicación**: `C:\myprojects\hidro-calc\.env`

```env
DATABASE_URL=sqlite:///./hidrocal.db
SQL_ECHO=false
ENVIRONMENT=development
DEBUG=true
```

- [ ] Archivo creado
- [ ] Variables visibles en terminal: `echo %DATABASE_URL%` (PowerShell)

### ☐ 2.2 Copiar archivo `database.py`
**Origen**: `/mnt/user-data/outputs/05_database.py`  
**Destino**: `C:\myprojects\hidro-calc\src\database.py`

- [ ] Archivo copiado
- [ ] Verificar imports disponibles

### ☐ 2.3 Copiar archivo `models.py`
**Origen**: `/mnt/user-data/outputs/02_models.py`  
**Destino**: `C:\myprojects\hidro-calc\src\core\models.py`

- [ ] Archivo copiado y sobrescrito
- [ ] Verificar que contiene: Project, Watershed, DesignStorm, Hydrograph

### ☐ 2.4 Copiar archivo `schemas.py`
**Origen**: `/mnt/user-data/outputs/03_schemas.py`  
**Destino**: `C:\myprojects\hidro-calc\src\core\schemas.py`

- [ ] Archivo copiado
- [ ] Verificar que tiene validaciones Pydantic

### ☐ 2.5 Copiar archivo `routes.py`
**Origen**: `/mnt/user-data/outputs/04_routes.py`  
**Destino**: `C:\myprojects\hidro-calc\src\api\routes.py`

- [ ] Archivo copiado (sobrescribir anterior)
- [ ] Verificar endpoints de CRUD

---

## 🔧 FASE 3: CONFIGURACIÓN (30 minutos)

### ☐ 3.1 Actualizar `src/main.py`
**Cambios necesarios**:

```python
# Agregar imports al inicio:
from database import init_db, get_db_stats, SessionLocal
from api.routes import router as api_router

# En el app:
app.include_router(api_router)

# Agregar evento startup:
@app.on_event("startup")
async def startup_event():
    init_db()
    db = SessionLocal()
    try:
        stats = get_db_stats(db)
        print(f"📊 BD Inicializada: {stats['num_projects']} proyectos")
    finally:
        db.close()
```

- [ ] Imports agregados
- [ ] Router incluído
- [ ] Evento startup definido

### ☐ 3.2 Crear estructura de directorios
```bash
# Verificar que existan:
src/
├── core/
│   ├── __init__.py
│   ├── models.py         ✅ Nuevo
│   ├── schemas.py        ✅ Nuevo
│   ├── rational_method.py
│   └── ...
├── api/
│   ├── __init__.py
│   └── routes.py         ✅ Actualizado
├── database.py           ✅ Nuevo
├── main.py               ✅ Actualizado
└── ...
```

- [ ] Estructura confirmada

### ☐ 3.3 Verificar imports circulares
```bash
cd C:\myprojects\hidro-calc
python -m py_compile src/core/models.py
python -m py_compile src/core/schemas.py
python -m py_compile src/api/routes.py
python -m py_compile src/database.py
```

- [ ] Todos los archivos compilan sin errores

---

## 🗄️ FASE 4: INICIALIZAR BD (30 minutos)

### ☐ 4.1 Crear tablas vacías
```bash
cd C:\myprojects\hidro-calc
.\venv\Scripts\activate

python src/database.py init
```

**Output esperado:**
```
🔧 Inicializando base de datos...
✅ Base de datos lista
```

- [ ] Comando ejecutado sin errores
- [ ] Archivo `hidrocal.db` creado en la raíz

### ☐ 4.2 Verificar archivo BD
```bash
# El archivo debe existir:
dir hidrocal.db

# O en Linux/Mac:
ls -la hidrocal.db
```

- [ ] Archivo existe y tiene tamaño > 0

### ☐ 4.3 Cargar datos de prueba
```bash
python src/database.py seed
```

**Output esperado:**
```
🔧 Inicializando base de datos...
✅ Base de datos lista
🌱 Sembrando datos de prueba...
✅ Seed completado: 1 proyecto, 3 cuencas, 4 tormentas
```

- [ ] Seed completado con éxito
- [ ] Base de datos tiene datos de ejemplo

---

## 🚀 FASE 5: PRUEBAS (1 hora)

### ☐ 5.1 Iniciar servidor
```bash
# Asegurarse que venv está activo
.\venv\Scripts\activate

# Iniciar servidor
python src/main.py
```

**Output esperado:**
```
============================================================
🌊 HidroCalc - Herramienta de Hidrología e Hidráulica
============================================================

🔧 Inicializando base de datos...
✅ Base de datos lista

📊 Estadísticas de Base de Datos:
   • Proyectos: 1
   • Cuencas: 3
   • Tormentas: 4
   • Hidrogramas: 0

🚀 Servidor iniciado en: http://localhost:8000
📚 Documentación API: http://localhost:8000/docs
============================================================
```

- [ ] Servidor inicia sin errores
- [ ] Mensaje de estadísticas aparece
- [ ] No hay excepciones

### ☐ 5.2 Acceder a documentación API
- [ ] Abrir navegador: `http://localhost:8000/docs`
- [ ] Verificar que aparecen los endpoints
- [ ] Buscar endpoints `/projects`, `/watersheds`, `/design-storms`, `/hydrographs`

### ☐ 5.3 Prueba GET - Obtener proyectos
```bash
# En otra terminal:
curl http://localhost:8000/api/v1/projects

# O usar Postman / Insomnia
GET http://localhost:8000/api/v1/projects
```

**Response esperado:**
```json
[
  {
    "id": 1,
    "name": "Sistema de Drenaje Montevideo",
    "description": "Proyecto piloto...",
    ...
  }
]
```

- [ ] Status 200
- [ ] Proyecto de prueba retornado

### ☐ 5.4 Prueba GET - Obtener cuencas
```bash
GET http://localhost:8000/api/v1/projects/1/watersheds
```

**Response esperado:**
```json
[
  {
    "id": 1,
    "project_id": 1,
    "name": "Arroyo Miguelete Alto",
    "area_hectareas": 250,
    "tc_horas": 1.8,
    "nc_scs": 72,
    ...
  },
  ...
]
```

- [ ] Status 200
- [ ] 3 cuencas retornadas

### ☐ 5.5 Prueba GET - Obtener tormentas
```bash
GET http://localhost:8000/api/v1/watersheds/1/design-storms
```

- [ ] Status 200
- [ ] 4 tormentas retornadas (Tr=10 con duraciones 2, 6, 12, 24h)

### ☐ 5.6 Prueba POST - Crear nuevo proyecto
```bash
POST http://localhost:8000/api/v1/projects

{
  "name": "Nuevo Proyecto Test",
  "description": "Prueba POST",
  "location": "Montevideo",
  "country": "Uruguay"
}
```

**Response esperado:**
```json
{
  "id": 2,
  "name": "Nuevo Proyecto Test",
  ...
}
```

- [ ] Status 201
- [ ] Nuevo proyecto tiene ID

### ☐ 5.7 Prueba POST - Crear cuenca
```bash
POST http://localhost:8000/api/v1/projects/2/watersheds

{
  "name": "Mi Cuenca Test",
  "area_hectareas": 150,
  "tc_horas": 1.5,
  "nc_scs": 75
}
```

- [ ] Status 201
- [ ] Cuenca creada con ID

### ☐ 5.8 Prueba POST - Guardar hidrograma
```bash
POST http://localhost:8000/api/v1/design-storms/1/hydrographs

{
  "method": "rational",
  "peak_discharge_m3s": 150.5,
  "peak_discharge_lps": 150500,
  "time_to_peak_minutes": 45,
  "total_runoff_m3": 350000,
  "volume_hm3": 0.35,
  "hydrograph_data": [
    {"time_min": 0, "discharge_m3s": 0, "cumulative_volume_m3": 0},
    {"time_min": 5, "discharge_m3s": 10.2, "cumulative_volume_m3": 1275},
    {"time_min": 10, "discharge_m3s": 35.8, "cumulative_volume_m3": 5775}
  ]
}
```

- [ ] Status 201
- [ ] Hidrograma guardado con ID

### ☐ 5.9 Prueba GET - Recuperar hidrograma
```bash
GET http://localhost:8000/api/v1/hydrographs/1
```

- [ ] Status 200
- [ ] Retorna hidrograma completo con serie temporal

### ☐ 5.10 Prueba POST - Comparar hidrogramas
```bash
POST http://localhost:8000/api/v1/compare-hydrographs

{
  "watershed_id": 1,
  "return_period_years": 10,
  "durations_hours": [2.0, 6.0, 12.0, 24.0]
}
```

**Response esperado:**
```json
{
  "hydrographs": [...],
  "statistics": {
    "num_hydrographs": 4,
    "max_peak_flow": 125.45,
    ...
  }
}
```

- [ ] Status 200
- [ ] Comparación con estadísticas

---

## 📊 FASE 6: INTEGRACIÓN FRONTEND (Opcional)

### ☐ 6.1 Actualizar `templates/index.html`
Agregar sección para:
- [ ] Selector de Proyectos
- [ ] Selector de Cuencas
- [ ] Selector de Tormentas
- [ ] Botón para calcular hidrograma
- [ ] Área para gráfico del hidrograma

### ☐ 6.2 Actualizar `static/js/app.js`
Agregar funciones para:
- [ ] Cargar lista de proyectos (GET /api/v1/projects)
- [ ] Cargar cuencas (GET /api/v1/projects/{id}/watersheds)
- [ ] Cargar tormentas (GET /api/v1/watersheds/{id}/design-storms)
- [ ] Enviar hidrograma calculado (POST /api/v1/design-storms/{id}/hydrographs)
- [ ] Dibujar gráfico con Chart.js o Plotly

### ☐ 6.3 Agregar librería de gráficos
En `templates/index.html`:
```html
<!-- Chart.js para gráficos -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>

<!-- O Plotly para gráficos más complejos -->
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
```

- [ ] Una librería seleccionada
- [ ] Integrada en HTML

---

## ✅ VERIFICACIÓN FINAL

### ☐ Tests automatizados
```bash
# Crear archivo tests/test_database.py
# Ejecutar:
pytest tests/test_database.py -v
```

- [ ] Todos los tests pasan

### ☐ Documentación
- [ ] Revisar que `/docs` muestra todos los endpoints
- [ ] Endpoint descriptions son claras

### ☐ Rendimiento
```bash
# Probar con datos más grandes
python src/database.py reset

# Crear proyectos masivamente
python -c "
from database import SessionLocal
from core.models import Project
db = SessionLocal()
for i in range(10):
    p = Project(name=f'Proyecto {i}')
    db.add(p)
db.commit()
"

# Verificar que queries siguen siendo rápidas
curl http://localhost:8000/api/v1/projects
```

- [ ] Respuestas rápidas (<500ms)

---

## 📝 TAREAS PENDIENTES (Próximas Fases)

### Fase 3: Métodos Adicionales
- [ ] Implementar Método SCS en `core/scs_method.py`
- [ ] Implementar Método Snyder
- [ ] Guardar hidrogramas con diferentes métodos

### Fase 4: Visualización
- [ ] Crear gráficos interactivos
- [ ] Comparación visual de hidrogramas
- [ ] Exportar a PDF/Excel

### Fase 5: Características Avanzadas
- [ ] Autenticación de usuarios
- [ ] Permisos por proyecto
- [ ] Compartir proyectos
- [ ] Historial de cambios

### Fase 6: Deployment
- [ ] Migrar a PostgreSQL
- [ ] Desplegar en servidor
- [ ] CI/CD pipeline
- [ ] Backups automáticos

---

## 🆘 TROUBLESHOOTING

### Error: "ModuleNotFoundError: No module named 'sqlalchemy'"
```bash
pip install sqlalchemy==2.0.23
```

### Error: "UNIQUE constraint failed: projects.name"
```bash
# Base de datos tiene duplicados, limpiar:
python src/database.py reset
```

### Error: "Permission denied" al escribir hidrocal.db
```bash
# Cambiar permisos:
chmod 666 hidrocal.db

# O eliminar y recrear:
rm hidrocal.db
python src/database.py seed
```

### API lenta después de agregartablas
```bash
# Asegurarse que índices existen:
# (Ya están en los modelos)

# Verificar tamaño de BD:
ls -lh hidrocal.db
```

### ImportError en routes.py
```bash
# Verificar que database.py está en src/
# Y que los imports son relativos:
from database import get_db
```

---

## 📞 PREGUNTAS FRECUENTES

**P: ¿Puedo usar MySQL en lugar de SQLite?**  
R: Sí, cambiar en `.env`: `DATABASE_URL=mysql+pymysql://user:pass@localhost/hidrocal_db`

**P: ¿Cómo backup la BD?**  
R: SQLite: `cp hidrocal.db hidrocal_backup.db`

**P: ¿Cuántos registros soporta?**  
R: SQLite soporta millones. Para producción, usar PostgreSQL.

**P: ¿Cómo agrego mi propio método de cálculo?**  
R: Ver Ejemplo 2 en `08_EJEMPLOS_CODIGO.md`

---

## 📞 CONTACTO / SOPORTE

Si tienes problemas durante la implementación:
1. Revisar `06_GUIA_IMPLEMENTACION.md`
2. Ver ejemplos en `08_EJEMPLOS_CODIGO.md`
3. Revisar diagramas en `07_DIAGRAMAS_VISUALES.md`

---

**Estado**: Listo para implementar  
**Última actualización**: Noviembre 2025  
**Versión**: 2.0  

¡Adelante con la implementación! 🚀
