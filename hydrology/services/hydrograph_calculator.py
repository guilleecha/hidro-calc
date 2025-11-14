"""
Hydrograph Calculation Service

Calcula hidrogramas usando diferentes métodos hidrológicos.

Métodos implementados:
- Rational Method (Hidrograma triangular/trapezoidal)
- Convolution method (convolución lluvia efectiva con hidrograma unitario)

Referencias:
- Chow, V.T., Maidment, D.R., Mays, L.W. (1988). Applied Hydrology. McGraw-Hill.
- Ven Te Chow (1964). Handbook of Applied Hydrology.
"""

from typing import Dict, List, Optional
from .hyetograph import generate_hyetograph
from .rainfall_excess import calculate_rainfall_excess


class HydrographCalculationError(Exception):
    """Error en cálculo de hidrograma"""
    pass


def calculate_hydrograph_rational(
    area_km2: float,
    tc_minutes: float,
    rainfall_excess_series: List[float],
    time_step_minutes: float = 5
) -> Dict:
    """
    Calcula hidrograma usando Método Racional (hidrograma triangular).

    Q = C × i × A (para pico)
    Hidrograma triangular con:
    - Tiempo al pico = Tc
    - Tiempo base = 2.67 × Tc (aproximación común)

    Args:
        area_km2: Área de la cuenca en km²
        tc_minutes: Tiempo de concentración en minutos
        rainfall_excess_series: Serie de lluvia efectiva (mm)
        time_step_minutes: Paso de tiempo en minutos

    Returns:
        Dict con estructura:
        {
            'time_steps': [0, 5, 10, ...],  # minutos
            'discharge_m3s': [0, 1.2, 5.4, ...],  # m³/s
            'cumulative_volume_m3': [0, 360, 1980, ...],
            'peak_discharge_m3s': float,
            'time_to_peak_minutes': float,
            'time_base_minutes': float,
            'total_volume_m3': float,
            'method': 'rational'
        }
    """
    # Validaciones
    if area_km2 <= 0:
        raise ValueError(f"Área debe ser > 0. Valor: {area_km2}")
    if tc_minutes <= 0:
        raise ValueError(f"Tc debe ser > 0. Valor: {tc_minutes}")
    if not rainfall_excess_series or len(rainfall_excess_series) == 0:
        raise ValueError("rainfall_excess_series no puede estar vacía")

    # Convertir área a m²
    area_m2 = area_km2 * 1_000_000

    # Calcular intensidad promedio de lluvia efectiva (mm/h)
    total_excess_mm = sum(rainfall_excess_series)
    duration_hours = len(rainfall_excess_series) * time_step_minutes / 60

    if duration_hours == 0:
        raise HydrographCalculationError("Duración de tormenta es 0")

    avg_intensity_mmh = total_excess_mm / duration_hours

    # Caudal pico usando fórmula racional: Q = (C × i × A) / 360
    # Como ya tenemos lluvia efectiva (C × P), usamos la intensidad efectiva
    # Q (m³/s) = (i_eff [mm/h] × A [ha]) / 360
    area_ha = area_km2 * 100
    peak_discharge_m3s = (avg_intensity_mmh * area_ha) / 360

    # Parámetros del hidrograma triangular
    time_to_peak = tc_minutes
    time_base = 2.67 * tc_minutes  # Aproximación común

    # Generar hidrograma triangular usando convolución
    # Crear hidrograma unitario triangular (1 mm de lluvia efectiva)
    num_intervals = int((time_base / time_step_minutes) + 2)
    unit_hydrograph = []

    for i in range(num_intervals):
        t = i * time_step_minutes

        if t <= time_to_peak:
            # Rama ascendente
            q_unit = (peak_discharge_m3s / (total_excess_mm if total_excess_mm > 0 else 1)) * (t / time_to_peak)
        elif t <= time_base:
            # Rama descendente
            q_unit = (peak_discharge_m3s / (total_excess_mm if total_excess_mm > 0 else 1)) * \
                     (time_base - t) / (time_base - time_to_peak)
        else:
            q_unit = 0

        unit_hydrograph.append(max(0, q_unit))

    # Convolución: hidrograma = lluvia efectiva ⊗ hidrograma unitario
    discharge_series = convolve_rainfall_with_unit_hydrograph(
        rainfall_excess_series,
        unit_hydrograph,
        time_step_minutes,
        area_m2
    )

    # Calcular volúmenes acumulados
    cumulative_volume = []
    volume = 0

    for q in discharge_series:
        volume += q * time_step_minutes * 60  # m³ (Q en m³/s × tiempo en segundos)
        cumulative_volume.append(volume)

    # Serie temporal
    time_steps = [i * time_step_minutes for i in range(len(discharge_series))]

    # Encontrar caudal pico real y tiempo al pico
    actual_peak = max(discharge_series) if discharge_series else 0
    peak_index = discharge_series.index(actual_peak) if actual_peak > 0 else 0
    actual_time_to_peak = peak_index * time_step_minutes

    return {
        'time_steps': time_steps,
        'discharge_m3s': discharge_series,
        'cumulative_volume_m3': cumulative_volume,
        'peak_discharge_m3s': actual_peak,
        'time_to_peak_minutes': actual_time_to_peak,
        'time_base_minutes': time_steps[-1] if time_steps else 0,
        'total_volume_m3': volume,
        'method': 'rational',
        'area_km2': area_km2,
        'tc_minutes': tc_minutes,
        'time_step_minutes': time_step_minutes
    }


def convolve_rainfall_with_unit_hydrograph(
    rainfall_excess_mm: List[float],
    unit_hydrograph_m3s_per_mm: List[float],
    time_step_minutes: float,
    area_m2: float
) -> List[float]:
    """
    Realiza convolución discreta entre lluvia efectiva e hidrograma unitario.

    Q(t) = Σ [Pe(i) × U(t-i)]

    Args:
        rainfall_excess_mm: Serie de lluvia efectiva [mm]
        unit_hydrograph_m3s_per_mm: Hidrograma unitario [m³/s por mm]
        time_step_minutes: Paso de tiempo [min]
        area_m2: Área de la cuenca [m²]

    Returns:
        Serie de caudales [m³/s]
    """
    n_rain = len(rainfall_excess_mm)
    n_uh = len(unit_hydrograph_m3s_per_mm)
    n_total = n_rain + n_uh - 1

    discharge = [0.0] * n_total

    # Convolución discreta
    for i in range(n_rain):
        for j in range(n_uh):
            if rainfall_excess_mm[i] > 0:
                discharge[i + j] += rainfall_excess_mm[i] * unit_hydrograph_m3s_per_mm[j]

    return discharge


def calculate_hydrograph(
    total_rainfall_mm: float,
    duration_hours: float,
    area_km2: float,
    tc_minutes: float,
    method: str = 'rational',
    hyetograph_method: str = 'alternating_block',
    excess_method: str = 'rational',
    C: float = None,
    CN: int = None,
    time_step_minutes: float = None,
    peak_position_ratio: float = 0.5,
    P3_10: float = None,
    Tr: float = None,
    **kwargs
) -> Dict:
    """
    Función orquestadora principal para calcular hidrograma completo.

    Flujo:
    1. Genera hietograma (distribución temporal de lluvia)
    2. Calcula lluvia efectiva (considera infiltración)
    3. Calcula hidrograma (convierte lluvia en caudal)

    Args:
        total_rainfall_mm: Precipitación total [mm]
        duration_hours: Duración de tormenta [h]
        area_km2: Área de cuenca [km²]
        tc_minutes: Tiempo de concentración [min]
        method: Método de hidrograma ('rational', 'scs_unit_hydrograph')
        hyetograph_method: Método de hietograma ('alternating_block', 'uniform')
        excess_method: Método de lluvia efectiva ('rational', 'scs_curve_number')
        C: Coeficiente de escorrentía (para método racional)
        CN: Curve Number (para método SCS)
        time_step_minutes: Paso de tiempo [min] (auto si None)
        peak_position_ratio: Posición del pico en hietograma (0.0-1.0)
        P3_10: Precipitación de referencia IDF [mm]
        Tr: Período de retorno [años]
        **kwargs: Parámetros adicionales

    Returns:
        Dict con estructura completa:
        {
            'hyetograph': {...},  # Resultado de generate_hyetograph()
            'rainfall_excess': {...},  # Resultado de calculate_rainfall_excess()
            'hydrograph': {...},  # Resultado de calculate_hydrograph_rational()
            'summary': {
                'peak_discharge_m3s': float,
                'time_to_peak_minutes': float,
                'total_volume_m3': float,
                'total_rainfall_mm': float,
                'rainfall_excess_mm': float,
                'infiltration_mm': float,
                'runoff_coefficient': float
            }
        }

    Raises:
        ValueError: Si faltan parámetros requeridos
        HydrographCalculationError: Si ocurre error en cálculo

    Example:
        >>> result = calculate_hydrograph(
        ...     total_rainfall_mm=127,
        ...     duration_hours=24,
        ...     area_km2=5.2,
        ...     tc_minutes=45,
        ...     C=0.6,
        ...     P3_10=70,
        ...     Tr=10
        ... )
        >>> result['summary']['peak_discharge_m3s']
        8.45
    """
    # Validar parámetros de entrada
    if total_rainfall_mm <= 0:
        raise ValueError(f"total_rainfall_mm debe ser > 0. Valor: {total_rainfall_mm}")
    if duration_hours <= 0:
        raise ValueError(f"duration_hours debe ser > 0. Valor: {duration_hours}")
    if area_km2 <= 0:
        raise ValueError(f"area_km2 debe ser > 0. Valor: {area_km2}")
    if tc_minutes <= 0:
        raise ValueError(f"tc_minutes debe ser > 0. Valor: {tc_minutes}")

    # Validar parámetros según método de excess
    if excess_method == 'rational' and C is None:
        raise ValueError("excess_method='rational' requiere parámetro C")
    if excess_method == 'scs_curve_number' and CN is None:
        raise ValueError("excess_method='scs_curve_number' requiere parámetro CN")

    # Calcular time_step óptimo si no se especificó
    if time_step_minutes is None:
        # Regla: Δt ≤ Tc/5 (HEC-HMS)
        time_step_minutes = max(1, min(30, tc_minutes / 5))
        time_step_minutes = round(time_step_minutes / 5) * 5  # Redondear a múltiplo de 5
        if time_step_minutes == 0:
            time_step_minutes = 5

    # Paso 1: Generar hietograma
    try:
        hyetograph_result = generate_hyetograph(
            total_rainfall_mm=total_rainfall_mm,
            duration_hours=duration_hours,
            method=hyetograph_method,
            time_step_minutes=time_step_minutes,
            peak_position_ratio=peak_position_ratio,
            P3_10=P3_10,
            Tr=Tr,
            area_km2=area_km2
        )
    except Exception as e:
        raise HydrographCalculationError(f"Error generando hietograma: {str(e)}")

    # Paso 2: Calcular lluvia efectiva
    try:
        rainfall_series = hyetograph_result.get('rainfall_mm', [])

        excess_result = calculate_rainfall_excess(
            rainfall_series=rainfall_series,
            method=excess_method,
            time_step_minutes=time_step_minutes,
            C=C,
            CN=CN,
            **kwargs
        )
    except Exception as e:
        raise HydrographCalculationError(f"Error calculando lluvia efectiva: {str(e)}")

    # Paso 3: Calcular hidrograma
    try:
        rainfall_excess_series = excess_result.get('excess_series', [])

        if method == 'rational':
            hydrograph_result = calculate_hydrograph_rational(
                area_km2=area_km2,
                tc_minutes=tc_minutes,
                rainfall_excess_series=rainfall_excess_series,
                time_step_minutes=time_step_minutes
            )
        else:
            raise ValueError(f"Método de hidrograma '{method}' no implementado aún")
    except Exception as e:
        raise HydrographCalculationError(f"Error calculando hidrograma: {str(e)}")

    # Resumen consolidado
    summary = {
        'peak_discharge_m3s': hydrograph_result['peak_discharge_m3s'],
        'peak_discharge_lps': hydrograph_result['peak_discharge_m3s'] * 1000,
        'time_to_peak_minutes': hydrograph_result['time_to_peak_minutes'],
        'time_to_peak_hours': hydrograph_result['time_to_peak_minutes'] / 60,
        'time_base_minutes': hydrograph_result['time_base_minutes'],
        'total_volume_m3': hydrograph_result['total_volume_m3'],
        'total_volume_hm3': hydrograph_result['total_volume_m3'] / 1_000_000,
        'total_rainfall_mm': total_rainfall_mm,
        'rainfall_excess_mm': excess_result['total_excess_mm'],
        'infiltration_mm': excess_result['total_infiltration_mm'],
        'runoff_coefficient': excess_result['runoff_coefficient'],
        'area_km2': area_km2,
        'tc_minutes': tc_minutes,
        'time_step_minutes': time_step_minutes,
        'method': method,
        'hyetograph_method': hyetograph_method,
        'excess_method': excess_method
    }

    return {
        'hyetograph': hyetograph_result,
        'rainfall_excess': excess_result,
        'hydrograph': hydrograph_result,
        'summary': summary
    }
