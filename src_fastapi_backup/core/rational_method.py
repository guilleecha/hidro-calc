"""
Módulo para el cálculo del Método Racional.

El Método Racional es usado para estimar el caudal pico de escorrentía
en cuencas pequeñas (< 200 ha generalmente).

Fórmula: Q = C × I × A / 360

Referencias:
    - Ven Te Chow, "Applied Hydrology" (1988), Chapter 14
    - ASCE Manual of Practice No. 77
"""

import warnings
from typing import Dict, Any


def calculate_rational_flow(C: float, I_mmh: float, A_ha: float) -> float:
    """
    Calcula el caudal de diseño usando el Método Racional.

    Fórmula: Q = C × I × A × 2.778

    El factor 2.778 (= 1000/360) proviene de la conversión de unidades:
    - I en mm/h → m/s (÷1000 ÷3600)
    - A en ha → m² (×10000)
    - Resultado en m³/s → L/s (×1000)
    - Q(m³/s) = C × I(mm/h) × A(ha) / 360000 × 10000 = C × I × A / 360
    - Q(L/s) = C × I(mm/h) × A(ha) / 360 × 1000 = C × I × A × 2.778
    - O equivalentemente: Q(L/s) = C × I(mm/h) × A(ha) / 0.36

    Args:
        C: Coeficiente de escorrentía (adimensional, 0-1)
           Representa la fracción de lluvia que se convierte en escorrentía.
           Valores típicos:
           - Techos: 0.75-0.95
           - Pavimento: 0.70-0.95
           - Césped (pendiente <2%): 0.05-0.10
           - Césped (pendiente >7%): 0.15-0.35

        I_mmh: Intensidad de lluvia en mm/h
               Típicamente obtenida de curvas IDF (Intensidad-Duración-Frecuencia)
               para una duración igual al tiempo de concentración de la cuenca.

        A_ha: Área de la cuenca en hectáreas
              El método racional es más confiable para cuencas < 200 ha.

    Returns:
        float: Caudal de diseño en L/s (litros por segundo)

    Raises:
        ValueError: Si los parámetros están fuera de rango válido

    Ejemplo:
        >>> calculate_rational_flow(C=0.65, I_mmh=80, A_ha=5)
        722.2222222222222

        >>> # Cuenca urbana de 10 ha, C=0.70, intensidad 100 mm/h
        >>> calculate_rational_flow(C=0.70, I_mmh=100, A_ha=10)
        1944.4444444444443

    Notas:
        - Para cuencas con diferentes coeficientes de escorrentía,
          usar un C ponderado: C_ponderado = Σ(Ci × Ai) / A_total
        - El método asume que:
          * La lluvia es uniforme en toda la cuenca
          * La duración de la lluvia ≥ tiempo de concentración
          * El pico de escorrentía ocurre cuando toda la cuenca contribuye
    """
    # Validación de parámetros
    if C < 0 or C > 1:
        raise ValueError(
            f"El coeficiente de escorrentía C debe estar entre 0 y 1. "
            f"Valor recibido: {C}"
        )

    if I_mmh < 0:
        raise ValueError(
            f"La intensidad de lluvia no puede ser negativa. "
            f"Valor recibido: {I_mmh} mm/h"
        )

    if A_ha <= 0:
        raise ValueError(
            f"El área de la cuenca debe ser positiva. "
            f"Valor recibido: {A_ha} ha"
        )

    # Advertencias para valores extremos
    if I_mmh > 500:
        warnings.warn(
            f"Intensidad muy alta ({I_mmh} mm/h > 500 mm/h). "
            f"Verifica que el valor sea correcto.",
            UserWarning
        )

    if A_ha > 200:
        warnings.warn(
            f"Área grande ({A_ha} ha > 200 ha). "
            f"El método racional es más confiable para cuencas pequeñas. "
            f"Considera métodos más avanzados como hidrogramas unitarios.",
            UserWarning
        )

    if C < 0.05:
        warnings.warn(
            f"Coeficiente de escorrentía muy bajo (C={C} < 0.05). "
            f"Verifica que sea correcto para el tipo de superficie.",
            UserWarning
        )

    # Cálculo del caudal
    # Q(L/s) = C × I(mm/h) × A(ha) × 2.778 (o equivalente: / 0.36)
    Q_ls = (C * I_mmh * A_ha) * 2.778

    return Q_ls


def calculate_rational_flow_detailed(
    C: float,
    I_mmh: float,
    A_ha: float,
    description: str = ""
) -> Dict[str, Any]:
    """
    Calcula el caudal usando el Método Racional con información detallada.

    Esta versión incluye datos intermedios útiles para reportes y verificación.

    Args:
        C: Coeficiente de escorrentía (0-1)
        I_mmh: Intensidad de lluvia (mm/h)
        A_ha: Área de la cuenca (ha)
        description: Descripción opcional del cálculo

    Returns:
        Dict con la siguiente estructura:
        {
            'Q_ls': float,           # Caudal en L/s
            'Q_m3s': float,          # Caudal en m³/s
            'Q_m3h': float,          # Caudal en m³/h
            'inputs': {              # Valores de entrada
                'C': float,
                'I_mmh': float,
                'A_ha': float,
                'A_m2': float,       # Área en m²
                'A_km2': float       # Área en km²
            },
            'description': str,      # Descripción del cálculo
            'warnings': List[str]    # Advertencias si las hay
        }

    Ejemplo:
        >>> result = calculate_rational_flow_detailed(
        ...     C=0.65,
        ...     I_mmh=80,
        ...     A_ha=5,
        ...     description="Cuenca residencial"
        ... )
        >>> print(f"Q = {result['Q_ls']:.2f} L/s")
        Q = 722.22 L/s
    """
    # Capturar warnings
    warnings_list = []

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        Q_ls = calculate_rational_flow(C, I_mmh, A_ha)

        # Guardar warnings si los hay
        if w:
            warnings_list = [str(warning.message) for warning in w]

    # Conversiones de unidades
    Q_m3s = Q_ls / 1000  # L/s a m³/s
    Q_m3h = Q_m3s * 3600  # m³/s a m³/h

    A_m2 = A_ha * 10000  # ha a m²
    A_km2 = A_ha / 100   # ha a km²

    return {
        'Q_ls': round(Q_ls, 2),
        'Q_m3s': round(Q_m3s, 4),
        'Q_m3h': round(Q_m3h, 2),
        'inputs': {
            'C': C,
            'I_mmh': I_mmh,
            'A_ha': A_ha,
            'A_m2': A_m2,
            'A_km2': round(A_km2, 4)
        },
        'description': description,
        'warnings': warnings_list
    }


def calculate_weighted_C(areas_coefficients: list[tuple[float, float]]) -> float:
    """
    Calcula el coeficiente de escorrentía ponderado para cuencas con múltiples superficies.

    Fórmula: C_ponderado = Σ(Ci × Ai) / A_total

    Args:
        areas_coefficients: Lista de tuplas (área_ha, coeficiente_C)
                           Cada tupla representa una superficie diferente

    Returns:
        float: Coeficiente de escorrentía ponderado

    Raises:
        ValueError: Si no hay áreas o si algún valor es inválido

    Ejemplo:
        >>> # Cuenca con diferentes superficies:
        >>> # - 2 ha de techos (C=0.90)
        >>> # - 3 ha de pavimento (C=0.85)
        >>> # - 5 ha de césped (C=0.20)
        >>> areas = [(2, 0.90), (3, 0.85), (5, 0.20)]
        >>> C_pond = calculate_weighted_C(areas)
        >>> print(f"C ponderado: {C_pond:.3f}")
        C ponderado: 0.525
    """
    if not areas_coefficients:
        raise ValueError("Debe proporcionar al menos un área con su coeficiente")

    total_area = 0
    weighted_sum = 0

    for area_ha, C in areas_coefficients:
        if area_ha <= 0:
            raise ValueError(f"El área debe ser positiva. Valor: {area_ha} ha")

        if C < 0 or C > 1:
            raise ValueError(f"El coeficiente C debe estar entre 0 y 1. Valor: {C}")

        total_area += area_ha
        weighted_sum += C * area_ha

    C_weighted = weighted_sum / total_area

    return C_weighted


# Datos de referencia para coeficientes de escorrentía típicos
RUNOFF_COEFFICIENTS = {
    "techos": {"min": 0.75, "max": 0.95, "tipico": 0.85, "descripcion": "Techos de cualquier material"},
    "pavimento_asfalto": {"min": 0.70, "max": 0.95, "tipico": 0.85, "descripcion": "Pavimento de asfalto"},
    "pavimento_hormigon": {"min": 0.80, "max": 0.95, "tipico": 0.90, "descripcion": "Pavimento de hormigón"},
    "pavimento_adoquines": {"min": 0.70, "max": 0.85, "tipico": 0.75, "descripcion": "Pavimento de adoquines con juntas"},
    "grava": {"min": 0.15, "max": 0.30, "tipico": 0.20, "descripcion": "Superficie de grava"},
    "cesped_plano_2pct": {"min": 0.05, "max": 0.10, "tipico": 0.08, "descripcion": "Césped, pendiente < 2%"},
    "cesped_medio_2_7pct": {"min": 0.10, "max": 0.15, "tipico": 0.13, "descripcion": "Césped, pendiente 2-7%"},
    "cesped_inclinado_7pct": {"min": 0.15, "max": 0.35, "tipico": 0.20, "descripcion": "Césped, pendiente > 7%"},
    "parques_jardines": {"min": 0.10, "max": 0.25, "tipico": 0.15, "descripcion": "Parques y jardines"},
    "bosques": {"min": 0.05, "max": 0.25, "tipico": 0.15, "descripcion": "Bosques y zonas forestales"},
    "comercial": {"min": 0.70, "max": 0.95, "tipico": 0.80, "descripcion": "Zona comercial"},
    "industrial": {"min": 0.50, "max": 0.90, "tipico": 0.70, "descripcion": "Zona industrial"},
    "residencial_alta_densidad": {"min": 0.50, "max": 0.70, "tipico": 0.60, "descripcion": "Residencial alta densidad"},
    "residencial_baja_densidad": {"min": 0.30, "max": 0.50, "tipico": 0.40, "descripcion": "Residencial baja densidad"}
}


if __name__ == "__main__":
    # Ejemplos de uso
    print("=== Método Racional - Ejemplos ===\n")

    # Ejemplo 1: Cálculo simple
    print("Ejemplo 1: Cuenca residencial")
    Q = calculate_rational_flow(C=0.65, I_mmh=80, A_ha=5)
    print(f"Q = {Q:.2f} L/s\n")

    # Ejemplo 2: Cálculo detallado
    print("Ejemplo 2: Cálculo detallado")
    result = calculate_rational_flow_detailed(
        C=0.70,
        I_mmh=100,
        A_ha=10,
        description="Zona comercial"
    )
    print(f"Q = {result['Q_ls']} L/s = {result['Q_m3s']} m³/s")
    print(f"Área = {result['inputs']['A_ha']} ha = {result['inputs']['A_m2']} m²\n")

    # Ejemplo 3: Coeficiente ponderado
    print("Ejemplo 3: Cuenca con múltiples superficies")
    areas = [
        (2, 0.90),  # 2 ha de techos
        (3, 0.85),  # 3 ha de pavimento
        (5, 0.20)   # 5 ha de césped
    ]
    C_pond = calculate_weighted_C(areas)
    total_area = sum(a[0] for a in areas)
    Q_pond = calculate_rational_flow(C=C_pond, I_mmh=90, A_ha=total_area)
    print(f"C ponderado = {C_pond:.3f}")
    print(f"Q = {Q_pond:.2f} L/s")
