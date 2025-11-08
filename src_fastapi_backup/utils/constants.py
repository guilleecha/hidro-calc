"""
Constantes físicas y valores de referencia para cálculos hidrológicos e hidráulicos.
"""

# ===== CONSTANTES FÍSICAS =====

GRAVITY_MS2 = 9.81  # Aceleración de la gravedad (m/s²)
WATER_DENSITY_KG_M3 = 1000  # Densidad del agua (kg/m³)
KINEMATIC_VISCOSITY_M2_S = 1.004e-6  # Viscosidad cinemática del agua a 20°C (m²/s)

# ===== CONVERSIÓN DE UNIDADES =====

# Área
HA_TO_M2 = 10000  # 1 hectárea = 10,000 m²
HA_TO_KM2 = 0.01  # 1 hectárea = 0.01 km²
M2_TO_HA = 0.0001  # 1 m² = 0.0001 ha

# Caudal
LS_TO_M3S = 0.001  # 1 L/s = 0.001 m³/s
M3S_TO_LS = 1000  # 1 m³/s = 1000 L/s
M3S_TO_M3H = 3600  # 1 m³/s = 3600 m³/h

# Intensidad de lluvia (factor de conversión para método racional)
# Q(L/s) = C × I(mm/h) × A(ha) × RATIONAL_FACTOR
RATIONAL_FACTOR = 2.778  # = 1000/360

# ===== COEFICIENTES DE ESCORRENTÍA =====
# Valores típicos según el tipo de superficie

RUNOFF_COEFFICIENTS = {
    # Superficies impermeables
    "techos": {
        "min": 0.75,
        "max": 0.95,
        "tipico": 0.85,
        "descripcion": "Techos de cualquier material"
    },
    "pavimento_asfalto": {
        "min": 0.70,
        "max": 0.95,
        "tipico": 0.85,
        "descripcion": "Pavimento de asfalto"
    },
    "pavimento_hormigon": {
        "min": 0.80,
        "max": 0.95,
        "tipico": 0.90,
        "descripcion": "Pavimento de hormigón"
    },
    "pavimento_adoquines": {
        "min": 0.70,
        "max": 0.85,
        "tipico": 0.75,
        "descripcion": "Pavimento de adoquines con juntas"
    },

    # Superficies permeables
    "grava": {
        "min": 0.15,
        "max": 0.30,
        "tipico": 0.20,
        "descripcion": "Superficie de grava"
    },
    "cesped_plano_2pct": {
        "min": 0.05,
        "max": 0.10,
        "tipico": 0.08,
        "descripcion": "Césped, pendiente < 2%"
    },
    "cesped_medio_2_7pct": {
        "min": 0.10,
        "max": 0.15,
        "tipico": 0.13,
        "descripcion": "Césped, pendiente 2-7%"
    },
    "cesped_inclinado_7pct": {
        "min": 0.15,
        "max": 0.35,
        "tipico": 0.20,
        "descripcion": "Césped, pendiente > 7%"
    },
    "parques_jardines": {
        "min": 0.10,
        "max": 0.25,
        "tipico": 0.15,
        "descripcion": "Parques y jardines"
    },
    "bosques": {
        "min": 0.05,
        "max": 0.25,
        "tipico": 0.15,
        "descripcion": "Bosques y zonas forestales"
    },

    # Zonas urbanas
    "comercial": {
        "min": 0.70,
        "max": 0.95,
        "tipico": 0.80,
        "descripcion": "Zona comercial"
    },
    "industrial": {
        "min": 0.50,
        "max": 0.90,
        "tipico": 0.70,
        "descripcion": "Zona industrial"
    },
    "residencial_alta_densidad": {
        "min": 0.50,
        "max": 0.70,
        "tipico": 0.60,
        "descripcion": "Residencial alta densidad"
    },
    "residencial_media_densidad": {
        "min": 0.40,
        "max": 0.60,
        "tipico": 0.50,
        "descripcion": "Residencial media densidad"
    },
    "residencial_baja_densidad": {
        "min": 0.30,
        "max": 0.50,
        "tipico": 0.40,
        "descripcion": "Residencial baja densidad"
    }
}

# ===== COEFICIENTES DE RUGOSIDAD DE MANNING =====
# Valores típicos del coeficiente n para diferentes materiales y condiciones

MANNING_N = {
    # Tuberías y conductos cerrados
    "pvc": {
        "min": 0.009,
        "max": 0.011,
        "tipico": 0.010,
        "descripcion": "Tubería de PVC"
    },
    "hormigon_liso": {
        "min": 0.011,
        "max": 0.013,
        "tipico": 0.012,
        "descripcion": "Hormigón liso, bien terminado"
    },
    "hormigon_rugoso": {
        "min": 0.014,
        "max": 0.017,
        "tipico": 0.015,
        "descripcion": "Hormigón rugoso"
    },
    "acero_nuevo": {
        "min": 0.010,
        "max": 0.013,
        "tipico": 0.011,
        "descripcion": "Acero nuevo"
    },

    # Canales artificiales
    "canal_hormigon_terminado": {
        "min": 0.012,
        "max": 0.014,
        "tipico": 0.013,
        "descripcion": "Canal de hormigón bien terminado"
    },
    "canal_mamposteria": {
        "min": 0.017,
        "max": 0.030,
        "tipico": 0.020,
        "descripcion": "Canal de mampostería"
    },
    "canal_tierra_limpio": {
        "min": 0.018,
        "max": 0.025,
        "tipico": 0.022,
        "descripcion": "Canal de tierra limpio"
    },
    "canal_tierra_vegetacion": {
        "min": 0.025,
        "max": 0.040,
        "tipico": 0.030,
        "descripcion": "Canal de tierra con vegetación"
    },

    # Cauces naturales
    "rio_limpio_recto": {
        "min": 0.025,
        "max": 0.033,
        "tipico": 0.030,
        "descripcion": "Río limpio y recto"
    },
    "rio_sinuoso": {
        "min": 0.033,
        "max": 0.045,
        "tipico": 0.040,
        "descripcion": "Río sinuoso con vegetación"
    },
    "arroyo_limpio": {
        "min": 0.030,
        "max": 0.040,
        "tipico": 0.035,
        "descripcion": "Arroyo limpio"
    }
}

# ===== LÍMITES RECOMENDADOS =====

# Método Racional
RATIONAL_MAX_AREA_HA = 200  # Área máxima recomendada (ha)
RATIONAL_MAX_TC_MIN = 60  # Tiempo de concentración máximo recomendado (min)

# Velocidades en tuberías y canales
MIN_VELOCITY_MS = 0.60  # Velocidad mínima para evitar sedimentación (m/s)
MAX_VELOCITY_MS = 5.00  # Velocidad máxima para evitar erosión (m/s)

# Pendientes
MIN_SLOPE = 0.0005  # Pendiente mínima recomendada
MAX_SLOPE = 0.10  # Pendiente máxima típica

# ===== PERIODOS DE RETORNO TÍPICOS =====

RETURN_PERIODS = {
    "alcantarillado_residencial": {"Tr_años": 5, "descripcion": "Alcantarillado pluvial residencial"},
    "alcantarillado_comercial": {"Tr_años": 10, "descripcion": "Alcantarillado pluvial comercial"},
    "obras_mayores": {"Tr_años": 25, "descripcion": "Obras de drenaje mayores"},
    "obras_importantes": {"Tr_años": 50, "descripcion": "Obras importantes"},
    "obras_criticas": {"Tr_años": 100, "descripcion": "Obras críticas o de gran importancia"}
}

# ===== INFORMACIÓN DEL PROYECTO =====

PROJECT_NAME = "HidroCalc"
PROJECT_VERSION = "1.0.0"
PROJECT_DESCRIPTION = "Herramienta web para cálculos de hidrología e hidráulica"
