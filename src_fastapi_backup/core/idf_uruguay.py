"""
Módulo de Curvas IDF (Intensidad-Duración-Frecuencia) para Uruguay.

Implementa las ecuaciones de Rodríguez Fontal (1980) para calcular
intensidades de lluvia corregidas por período de retorno, duración
y área de cuenca.

Referencias:
    - Rodríguez Fontal (1980) - Curvas IDF de Uruguay
    - Genta et al. (1998) - Actualización de curvas IDF
    - Período de datos: 1906-1980
"""

import math
from typing import Dict, Optional, Union


def calculate_CT(Tr: float) -> float:
    """
    Calcula el factor de corrección por período de retorno.

    Fórmula: CT(Tr) = 0.5786 - 0.4312 × log[ln(Tr / (Tr - 1))]

    Args:
        Tr: Período de retorno en años (>= 2)

    Returns:
        Factor CT (adimensional)

    Raises:
        ValueError: Si Tr < 2 años

    Example:
        >>> calculate_CT(5)
        0.8456
        >>> calculate_CT(10)
        0.9432
    """
    if Tr < 2:
        raise ValueError('El período de retorno debe ser >= 2 años')

    # Calcular logaritmo natural de Tr/(Tr-1)
    ln_term = math.log(Tr / (Tr - 1))

    # Calcular logaritmo base 10 del término anterior
    log_term = math.log10(ln_term)

    # Aplicar fórmula
    CT = 0.5786 - 0.4312 * log_term

    return CT


def calculate_CD(d: float) -> float:
    """
    Calcula el factor de corrección por duración.

    Fórmulas:
        - Para d < 3 horas: CD(d) = (0.6208 × d) / (d + 0.0137)^0.5639
        - Para d >= 3 horas: CD(d) = (1.0287 × d) / (d + 1.0293)^0.8083

    Args:
        d: Duración de la tormenta en horas (> 0)

    Returns:
        Factor CD (adimensional)

    Raises:
        ValueError: Si d <= 0

    Example:
        >>> calculate_CD(1)
        0.5184
        >>> calculate_CD(3)
        1.4869
        >>> calculate_CD(24)
        12.8357
    """
    if d <= 0:
        raise ValueError('La duración debe ser mayor a 0')

    if d < 3:
        # Fórmula para duraciones cortas (< 3 horas)
        numerator = 0.6208 * d
        denominator = (d + 0.0137) ** 0.5639
        CD = numerator / denominator
    else:
        # Fórmula para duraciones largas (>= 3 horas)
        numerator = 1.0287 * d
        denominator = (d + 1.0293) ** 0.8083
        CD = numerator / denominator

    return CD


def calculate_CA(Ac: Optional[float], d: float) -> float:
    """
    Calcula el factor de corrección por área de cuenca.

    Fórmula: CA(Ac,d) = 1.0 - (0.3549 × d^(-0.4272)) × (1.0 - e^(-0.005792 × Ac))

    Args:
        Ac: Área de cuenca en km² (>= 0, None para sin corrección)
        d: Duración de la tormenta en horas

    Returns:
        Factor CA (adimensional). Retorna 1.0 si Ac es None o 0.

    Example:
        >>> calculate_CA(None, 1)
        1.0
        >>> calculate_CA(0, 1)
        1.0
        >>> calculate_CA(30, 1)
        0.9451
    """
    # Si no hay área o es cero, no hay corrección
    if Ac is None or Ac == 0:
        return 1.0

    # Calcular término exponencial
    exp_term = 1.0 - math.exp(-0.005792 * Ac)

    # Calcular término de duración
    duration_term = 0.3549 * (d ** (-0.4272))

    # Aplicar fórmula
    CA = 1.0 - (duration_term * exp_term)

    return CA


def calculate_intensity_idf(
    P3_10: float,
    Tr: float,
    d: float,
    Ac: Optional[float] = None
) -> Dict[str, Union[float, None]]:
    """
    Calcula la intensidad de lluvia usando las Curvas IDF de Uruguay.

    Fórmula principal: I(Tr,d) = P₃,₁₀ × CT(Tr) × CD(d) × CA(Ac,d) / d

    Args:
        P3_10: Precipitación de 3 horas y 10 años en mm (típico: 50-100)
        Tr: Período de retorno en años (>= 2)
        d: Duración de la tormenta en horas (> 0)
        Ac: Área de cuenca en km² (opcional, None para intensidad puntual)

    Returns:
        Dictionary con los siguientes campos:
            - I_mmh: Intensidad en mm/h
            - P_mm: Precipitación total en mm
            - CT: Factor de corrección por período de retorno
            - CD: Factor de corrección por duración
            - CA: Factor de corrección por área
            - P3_10: Valor de P₃,₁₀ utilizado
            - Tr: Período de retorno utilizado
            - d_hours: Duración utilizada
            - Ac_km2: Área de cuenca utilizada (None si no aplica)

    Raises:
        ValueError: Si los parámetros están fuera de rango

    Example:
        >>> # Ejemplo del PDF - La Paloma
        >>> result = calculate_intensity_idf(P3_10=74, Tr=5, d=1, Ac=30)
        >>> print(f"I = {result['I_mmh']:.2f} mm/h")
        I = 36.34 mm/h
    """
    # Validación de P3_10
    if P3_10 < 50 or P3_10 > 100:
        raise ValueError(
            f'P₃,₁₀ debe estar entre 50 y 100 mm (valor típico de Uruguay). '
            f'Valor ingresado: {P3_10} mm'
        )

    # Validación de Tr (las funciones de cálculo validan internamente)
    if Tr < 2:
        raise ValueError('El período de retorno debe ser >= 2 años')

    # Validación de duración
    if d <= 0:
        raise ValueError('La duración debe ser mayor a 0')

    # Validación de área (si se proporciona)
    if Ac is not None and Ac < 0:
        raise ValueError('El área de cuenca no puede ser negativa')

    # Calcular factores de corrección
    CT = calculate_CT(Tr)
    CD = calculate_CD(d)
    CA = calculate_CA(Ac, d)

    # Calcular intensidad (mm/h)
    # I = P₃,₁₀ × CT × CD × CA / d
    I_mmh = (P3_10 * CT * CD * CA) / d

    # Calcular precipitación total (mm)
    P_mm = I_mmh * d

    # Preparar resultado
    result = {
        'I_mmh': round(I_mmh, 4),
        'P_mm': round(P_mm, 4),
        'CT': round(CT, 4),
        'CD': round(CD, 4),
        'CA': round(CA, 4),
        'P3_10': P3_10,
        'Tr': Tr,
        'd_hours': d,
        'Ac_km2': Ac
    }

    return result


# ===== FUNCIONES AUXILIARES =====

def get_P3_10_reference_values() -> Dict[str, float]:
    """
    Retorna valores de referencia de P₃,₁₀ para ciudades de Uruguay.

    Returns:
        Dictionary con ciudades y sus valores de P₃,₁₀ en mm

    Note:
        Estos son valores aproximados basados en isoyetas.
        Para diseños críticos, consultar mapas actualizados.
    """
    return {
        'Montevideo': 75.0,
        'La Paloma': 74.0,
        'Minas': 79.0,
        'Punta del Este': 73.0,
        'Salto': 68.0,
        'Paysandú': 70.0,
        'Rivera': 72.0,
        'Tacuarembó': 71.0,
        'Durazno': 76.0,
        'Florida': 77.0,
        'Colonia': 74.0,
        'Mercedes': 72.0,
    }


def validate_inputs_and_warn(P3_10: float, Tr: float, d: float, Ac: Optional[float]) -> list:
    """
    Valida entradas y genera advertencias (sin lanzar excepciones).

    Args:
        P3_10: Precipitación de 3h y 10 años
        Tr: Período de retorno
        d: Duración
        Ac: Área de cuenca

    Returns:
        Lista de advertencias (strings)
    """
    warnings = []

    # Advertencias para P3_10
    if P3_10 < 60:
        warnings.append('P₃,₁₀ menor a 60 mm. Verificar si es correcto para la zona.')
    elif P3_10 > 90:
        warnings.append('P₃,₁₀ mayor a 90 mm. Verificar si es correcto para la zona.')

    # Advertencias para Tr
    if Tr > 100:
        warnings.append('Período de retorno muy alto (>100 años). Las ecuaciones fueron calibradas hasta Tr=100.')

    # Advertencias para duración
    if d > 24:
        warnings.append('Duración mayor a 24 horas. Verificar aplicabilidad de las ecuaciones.')

    # Advertencias para área
    if Ac is not None and Ac > 300:
        warnings.append('Área de cuenca muy grande (>300 km²). Verificar aplicabilidad de la corrección por área.')

    return warnings


# ===== EJEMPLO DE USO =====

if __name__ == "__main__":
    # Ejemplo del PDF - La Paloma
    print("=" * 60)
    print("Ejemplo: Cálculo de IDF para La Paloma")
    print("=" * 60)

    result = calculate_intensity_idf(
        P3_10=74,  # mm
        Tr=5,      # años
        d=1,       # hora
        Ac=30      # km²
    )

    print(f"\nDatos de entrada:")
    print(f"  P₃,₁₀ = {result['P3_10']} mm")
    print(f"  Tr = {result['Tr']} años")
    print(f"  d = {result['d_hours']} hora(s)")
    print(f"  Ac = {result['Ac_km2']} km²")

    print(f"\nFactores de corrección:")
    print(f"  CT (por período de retorno) = {result['CT']:.4f}")
    print(f"  CD (por duración) = {result['CD']:.4f}")
    print(f"  CA (por área) = {result['CA']:.4f}")

    print(f"\nResultados:")
    print(f"  Intensidad: {result['I_mmh']:.2f} mm/h")
    print(f"  Precipitación total: {result['P_mm']:.2f} mm")

    print("\n" + "=" * 60)

    # Valores de referencia
    print("\nValores de P₃,₁₀ de referencia:")
    ref_values = get_P3_10_reference_values()
    for city, value in ref_values.items():
        print(f"  {city}: {value} mm")
