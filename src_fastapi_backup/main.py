"""
Servidor principal de HidroCalc.

Aplicación FastAPI para cálculos de hidrología e hidráulica.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
from pathlib import Path

import sys
from pathlib import Path

# Agregar el directorio raíz al path de Python
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.models.hydrology import (
    RationalMethodInput,
    RationalMethodOutput,
    WeightedCInput,
    WeightedCOutput,
    ErrorResponse
)
from src.models.idf import IDFInput, IDFOutput
from src.core.rational_method import (
    calculate_rational_flow_detailed,
    calculate_weighted_C,
    RUNOFF_COEFFICIENTS
)
from src.core.idf_uruguay import calculate_intensity_idf
from src.utils.constants import PROJECT_NAME, PROJECT_VERSION, PROJECT_DESCRIPTION
from database import init_db, get_db_stats, SessionLocal
from api.routes import router as api_router

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Crear instancia de FastAPI
app = FastAPI(
    title=PROJECT_NAME,
    version=PROJECT_VERSION,
    description=PROJECT_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir router de API con BD
app.include_router(api_router)

# Configurar rutas de archivos estáticos y templates
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

logger.info(f"Static directory: {STATIC_DIR}")
logger.info(f"Templates directory: {TEMPLATES_DIR}")


# ===== RUTAS FRONTEND =====

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Página principal."""
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": PROJECT_NAME}
    )


@app.get("/simple", response_class=HTMLResponse)
async def simple_index(request: Request):
    """Página simplificada según especificaciones del MVP."""
    return templates.TemplateResponse(
        "index_simple.html",
        {"request": request, "title": PROJECT_NAME}
    )


@app.get("/rational", response_class=HTMLResponse)
async def rational_method_page(request: Request):
    """Página del Método Racional."""
    return templates.TemplateResponse(
        "rational.html",
        {
            "request": request,
            "title": "Método Racional - " + PROJECT_NAME,
            "runoff_coefficients": RUNOFF_COEFFICIENTS
        }
    )


@app.get("/idf", response_class=HTMLResponse)
async def idf_page(request: Request):
    """Página de Curvas IDF - Uruguay."""
    return templates.TemplateResponse(
        "idf.html",
        {"request": request, "title": "Curvas IDF - Uruguay"}
    )


# ===== ENDPOINTS API =====

@app.get("/api/health")
async def health_check():
    """Endpoint de salud del servidor."""
    return {
        "status": "healthy",
        "project": PROJECT_NAME,
        "version": PROJECT_VERSION
    }


@app.post(
    "/api/rational",
    response_model=RationalMethodOutput,
    responses={
        400: {"model": ErrorResponse},
        422: {"model": ErrorResponse}
    },
    summary="Calcular caudal con Método Racional",
    description="""
    Calcula el caudal de diseño usando el Método Racional.

    **Fórmula:** Q = C × I × A × 2.778

    **Parámetros:**
    - **C**: Coeficiente de escorrentía (0-1)
    - **I**: Intensidad de lluvia (mm/h)
    - **A**: Área de la cuenca (ha)

    **Retorna:**
    - Caudal en L/s, m³/s y m³/h
    - Datos de entrada con conversiones
    - Advertencias si corresponde
    """
)
async def calculate_rational(data: RationalMethodInput):
    """
    Endpoint para calcular el caudal con el Método Racional.

    Args:
        data: Datos de entrada validados por Pydantic

    Returns:
        RationalMethodOutput: Resultado del cálculo con todos los detalles

    Raises:
        HTTPException: Si hay errores en el cálculo
    """
    try:
        logger.info(f"Calculando Método Racional: C={data.C}, I={data.I_mmh}, A={data.A_ha}")

        result = calculate_rational_flow_detailed(
            C=data.C,
            I_mmh=data.I_mmh,
            A_ha=data.A_ha,
            description=data.description
        )

        logger.info(f"Resultado: Q={result['Q_ls']} L/s")

        return RationalMethodOutput(**result)

    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )


# Alias para compatibilidad con las instrucciones del MVP
@app.post(
    "/api/calculate-rational",
    response_model=RationalMethodOutput,
    responses={
        400: {"model": ErrorResponse},
        422: {"model": ErrorResponse}
    },
    summary="Calcular caudal con Método Racional (alias)",
    description="Alias del endpoint /api/rational para compatibilidad"
)
async def calculate_rational_alias(data: RationalMethodInput):
    """Alias que llama al endpoint principal."""
    return await calculate_rational(data)


@app.post(
    "/api/weighted-c",
    response_model=WeightedCOutput,
    responses={
        400: {"model": ErrorResponse},
        422: {"model": ErrorResponse}
    },
    summary="Calcular coeficiente de escorrentía ponderado",
    description="""
    Calcula el coeficiente de escorrentía ponderado para cuencas con múltiples superficies.

    **Fórmula:** C_ponderado = Σ(Ci × Ai) / A_total

    **Parámetros:**
    - Lista de superficies, cada una con área (ha) y coeficiente C

    **Retorna:**
    - Coeficiente C ponderado
    - Área total
    - Detalle de cada superficie con porcentajes
    """
)
async def calculate_weighted_c_endpoint(data: WeightedCInput):
    """
    Endpoint para calcular el coeficiente de escorrentía ponderado.

    Args:
        data: Lista de superficies con área y coeficiente

    Returns:
        WeightedCOutput: Coeficiente ponderado y detalles

    Raises:
        HTTPException: Si hay errores en el cálculo
    """
    try:
        logger.info(f"Calculando C ponderado para {len(data.surfaces)} superficies")

        # Extraer tuplas (area, C) para el cálculo
        areas_coefficients = [
            (surface['area_ha'], surface['C'])
            for surface in data.surfaces
        ]

        # Calcular C ponderado
        C_weighted = calculate_weighted_C(areas_coefficients)

        # Calcular área total
        total_area = sum(s['area_ha'] for s in data.surfaces)

        # Agregar porcentajes a cada superficie
        surfaces_with_percentage = []
        for surface in data.surfaces:
            surface_copy = surface.copy()
            surface_copy['percentage'] = round(
                (surface['area_ha'] / total_area) * 100, 2
            )
            surfaces_with_percentage.append(surface_copy)

        result = {
            "C_weighted": round(C_weighted, 4),
            "total_area_ha": round(total_area, 2),
            "surfaces": surfaces_with_percentage
        }

        logger.info(f"C ponderado calculado: {result['C_weighted']}")

        return WeightedCOutput(**result)

    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )


@app.get(
    "/api/runoff-coefficients",
    summary="Obtener coeficientes de escorrentía de referencia",
    description="Retorna una lista de coeficientes de escorrentía típicos por tipo de superficie"
)
async def get_runoff_coefficients():
    """
    Endpoint para obtener coeficientes de escorrentía de referencia.

    Returns:
        Dict con coeficientes organizados por tipo de superficie
    """
    return {
        "coefficients": RUNOFF_COEFFICIENTS,
        "note": "Valores de referencia. Ajustar según condiciones locales."
    }


@app.post(
    "/api/calculate-idf",
    response_model=IDFOutput,
    responses={
        400: {"model": ErrorResponse},
        422: {"model": ErrorResponse}
    },
    summary="Calcular intensidad de lluvia con Curvas IDF de Uruguay",
    description="""
    Calcula la intensidad de lluvia usando las Curvas IDF específicas de Uruguay
    desarrolladas por Rodríguez Fontal (1980).

    **Fórmula:** I = P₃,₁₀ × CT × CD × CA / d

    **Parámetros:**
    - **P₃,₁₀**: Precipitación de 3 horas y 10 años (mm)
    - **Tr**: Período de retorno (años)
    - **d**: Duración de la tormenta (horas)
    - **Ac**: Área de cuenca (km²) - opcional

    **Factores de corrección:**
    - **CT**: Corrección por período de retorno
    - **CD**: Corrección por duración
    - **CA**: Corrección por área de cuenca

    **Retorna:**
    - Intensidad de lluvia (mm/h)
    - Precipitación total (mm)
    - Factores de corrección calculados
    """
)
async def calculate_idf(data: IDFInput):
    """
    Endpoint para calcular intensidad de lluvia con Curvas IDF de Uruguay.

    Args:
        data: Datos de entrada validados por Pydantic

    Returns:
        IDFOutput: Resultado del cálculo con intensidad y factores

    Raises:
        HTTPException: Si hay errores en el cálculo
    """
    try:
        logger.info(
            f"Calculando IDF: P3_10={data.P3_10}, Tr={data.Tr}, "
            f"d={data.d}, Ac={data.Ac}"
        )

        result = calculate_intensity_idf(
            P3_10=data.P3_10,
            Tr=data.Tr,
            d=data.d,
            Ac=data.Ac
        )

        logger.info(f"Resultado: I={result['I_mmh']} mm/h")

        return IDFOutput(**result)

    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error en cálculo IDF: {str(e)}"
        )


# ===== MANEJADOR DE ERRORES =====

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Manejador para errores 404."""
    return JSONResponse(
        status_code=404,
        content={
            "error": "NotFound",
            "message": f"Ruta no encontrada: {request.url.path}"
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    """Manejador para errores 500."""
    logger.error(f"Error interno: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "message": "Error interno del servidor"
        }
    )


# ===== EVENTO DE INICIO =====

@app.on_event("startup")
async def startup_event():
    """Evento ejecutado al iniciar el servidor."""
    logger.info(f"Iniciando {PROJECT_NAME} v{PROJECT_VERSION}")

    # Inicializar base de datos
    init_db()

    # Mostrar estadísticas de BD
    db = SessionLocal()
    try:
        stats = get_db_stats(db)
        logger.info("📊 Estadísticas de Base de Datos:")
        logger.info(f"   • Proyectos: {stats['num_projects']}")
        logger.info(f"   • Cuencas: {stats['num_watersheds']}")
        logger.info(f"   • Tormentas: {stats['num_design_storms']}")
        logger.info(f"   • Hidrogramas: {stats['num_hydrographs']}")
    finally:
        db.close()

    logger.info(f"Documentación disponible en: http://localhost:8000/docs")
    logger.info(f"Interfaz web disponible en: http://localhost:8000")


@app.on_event("shutdown")
async def shutdown_event():
    """Evento ejecutado al detener el servidor."""
    logger.info(f"Deteniendo {PROJECT_NAME}")


# ===== PUNTO DE ENTRADA =====

if __name__ == "__main__":
    import uvicorn

    # Configuración del servidor
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Recarga automática en desarrollo
        log_level="info"
    )
