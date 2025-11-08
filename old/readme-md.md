# 🌊 HidroCalc

Herramienta web para cálculos de hidrología e hidráulica, diseñada para ingenieros civiles especializados en sistemas de drenaje pluvial.

## 🎯 Descripción

HidroCalc es una aplicación web que permite realizar cálculos hidrológicos e hidráulicos de manera rápida y precisa, con una interfaz intuitiva y profesional.

### Características Principales

- ✅ **Método Racional**: Cálculo de caudales de diseño (Q = C × I × A)
- 🌧️ **Tormentas de Diseño**: Generación de hietogramas y curvas IDF
- 📊 **Hidrogramas**: Método del hidrograma unitario SCS
- 🌊 **Flujo Gradualmente Variado**: Perfiles de flujo en canales
- 🏗️ **Diseño de Canales**: Cálculos de flujo uniforme
- 🔧 **Obras Hidráulicas**: Alcantarillas, vertederos, orificios

## 🚀 Inicio Rápido

### Prerrequisitos

- Python 3.9 o superior
- Git

### Instalación

```bash
# Clonar el repositorio
git clone [URL_DEL_REPO]
cd hidro-calc

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
.\venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Ejecutar la Aplicación

```bash
# Iniciar servidor
python src/main.py

# La aplicación estará disponible en:
# http://localhost:8000
```

### Documentación API

Una vez que el servidor esté corriendo, accede a la documentación interactiva:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📚 Módulos Disponibles

### 1. Método Racional
Cálculo de caudales máximos de diseño usando la fórmula:

```
Q = C × I × A × 2.778
```

Donde:
- `Q`: Caudal (L/s)
- `C`: Coeficiente de escorrentía (0-1)
- `I`: Intensidad de lluvia (mm/h)
- `A`: Área de la cuenca (ha)

### 2. Tormentas de Diseño *(Próximamente)*
- Curvas IDF personalizables
- Método de bloques alternos
- Distribución temporal SCS

### 3. Hidrología Avanzada *(Próximamente)*
- Hidrograma Unitario
- Número de Curva (CN)
- Tiempos de concentración

## 🛠️ Tecnologías Utilizadas

- **Backend**: FastAPI, Python 3.14
- **Cálculos**: NumPy, SciPy, Pandas
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Gráficos**: Matplotlib, Chart.js
- **Documentación**: Swagger UI (automática)

## 📁 Estructura del Proyecto

```
hidro-calc/
├── src/
│   ├── main.py              # Servidor principal
│   ├── core/                # Lógica de cálculo
│   ├── api/                 # Endpoints API
│   ├── models/              # Modelos de datos
│   └── utils/               # Utilidades
├── templates/               # Templates HTML
├── static/                  # CSS, JS, imágenes
├── data/                    # Datos de referencia
├── tests/                   # Tests unitarios
└── docs/                    # Documentación

```

## 🧪 Tests

```bash
# Ejecutar todos los tests
pytest tests/ -v

# Ejecutar tests específicos
pytest tests/test_rational.py -v

# Ver cobertura
pytest --cov=src tests/
```

## 📖 Documentación Adicional

- [CLAUDE.md](CLAUDE.md) - Instrucciones para desarrollo con Claude CLI
- [DESARROLLO.md](DESARROLLO.md) - Plan de desarrollo y roadmap
- [docs/API.md](docs/API.md) - Documentación detallada de la API
- [docs/FORMULAS.md](docs/FORMULAS.md) - Referencias técnicas y fórmulas

## 🤝 Contribuciones

Este es un proyecto personal de herramientas para ingeniería civil. Si tienes sugerencias o mejoras, no dudes en abrir un issue.

## 📝 Licencia

[Por definir]

## 👤 Autor

Ingeniero Civil - Especialización en Drenaje Pluvial

## 🙏 Referencias

- Ven Te Chow - "Applied Hydrology" (1988)
- Ven Te Chow - "Open Channel Hydraulics" (1959)
- USDA - "Urban Hydrology for Small Watersheds" (TR-55)
- HEC-HMS Reference Manual

## 📧 Contacto

[Por definir]

---

**Versión**: 1.0.0  
**Última actualización**: Noviembre 2025