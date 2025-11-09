"""
Hyetograph Generation Service

Genera distribuciones temporales de lluvia (hietogramas) a partir de tormentas de diseño.

Métodos implementados:
- Alternating Block Method (Chow et al., 1988)
- Uniform Distribution (para testing)

Referencias:
- Chow, V.T., Maidment, D.R., Mays, L.W. (1988). Applied Hydrology. McGraw-Hill.
- SCS (1986). Urban Hydrology for Small Watersheds. TR-55.
"""

from typing import Dict, List
from calculators.services.idf import calculate_intensity_idf


class HyetographGenerationError(Exception):
    """Error en generación de hietograma"""
    pass


def generate_hyetograph_uniform(
    total_rainfall_mm: float,
    duration_hours: float,
    time_step_minutes: float = 5
) -> Dict:
    """
    Genera hietograma con distribución uniforme (lluvia constante).

    Útil para testing y como baseline de comparación.

    Args:
        total_rainfall_mm: Precipitación total de la tormenta (mm)
        duration_hours: Duración de la tormenta (horas)
        time_step_minutes: Intervalo de tiempo (minutos)

    Returns:
        Dict con estructura:
        {
            'time_steps': [0, 5, 10, 15, ...],  # minutos
            'rainfall_mm': [2.1, 2.1, 2.1, ...],  # mm en cada Δt
            'intensity_mmh': [25.2, 25.2, 25.2, ...],  # mm/h constante
            'cumulative_mm': [2.1, 4.2, 6.3, ...],
            'method': 'uniform',
            'duration_hours': float,
            'total_rainfall_mm': float,
            'time_step_minutes': float,
            'num_intervals': int
        }

    Raises:
        ValueError: Si los parámetros son inválidos
        HyetographGenerationError: Si ocurre error en cálculo

    Example:
        >>> result = generate_hyetograph_uniform(50.0, 2.0, 5)
        >>> result['intensity_mmh']
        [25.0, 25.0, 25.0, ...]  # Intensidad constante
    """
    # Validaciones
    if total_rainfall_mm <= 0:
        raise ValueError(f"Precipitación total debe ser > 0. Valor: {total_rainfall_mm}")
    if duration_hours <= 0:
        raise ValueError(f"Duración debe ser > 0. Valor: {duration_hours}")
    if time_step_minutes <= 0 or time_step_minutes > duration_hours * 60:
        raise ValueError(f"Time step inválido: {time_step_minutes} min")

    # Convertir duración a minutos
    duration_minutes = duration_hours * 60

    # Número de intervalos
    num_intervals = int(duration_minutes / time_step_minutes)

    # Intensidad constante
    intensity_mmh = total_rainfall_mm / duration_hours

    # Lluvia por intervalo
    rainfall_per_interval = (intensity_mmh * time_step_minutes) / 60

    # Generar series temporales
    time_steps = [i * time_step_minutes for i in range(num_intervals + 1)]
    rainfall_mm = [rainfall_per_interval if i > 0 else 0 for i in range(num_intervals + 1)]
    intensity_series = [intensity_mmh if i > 0 else 0 for i in range(num_intervals + 1)]
    cumulative_mm = []

    cumulative = 0
    for rain in rainfall_mm:
        cumulative += rain
        cumulative_mm.append(cumulative)

    return {
        'time_steps': time_steps,
        'rainfall_mm': rainfall_mm,
        'intensity_mmh': intensity_series,
        'cumulative_mm': cumulative_mm,
        'method': 'uniform',
        'duration_hours': duration_hours,
        'total_rainfall_mm': total_rainfall_mm,
        'time_step_minutes': time_step_minutes,
        'num_intervals': num_intervals
    }


def generate_hyetograph_alternating_block(
    total_rainfall_mm: float,
    duration_hours: float,
    P3_10: float,
    Tr: float,
    area_km2: float = None,
    time_step_minutes: float = 5
) -> Dict:
    """
    Genera hietograma usando el Método de Bloques Alternados.

    Proceso:
    1. Divide la duración en intervalos de Δt
    2. Calcula intensidad para cada duración acumulada usando curva IDF
    3. Calcula incrementos de precipitación
    4. Ordena incrementos en patrón alternado (pico al centro)

    Args:
        total_rainfall_mm: Precipitación total de la tormenta (mm)
        duration_hours: Duración de la tormenta (horas)
        P3_10: Parámetro P₃,₁₀ para curva IDF (mm)
        Tr: Período de retorno (años)
        area_km2: Área de cuenca en km² (None para puntual)
        time_step_minutes: Intervalo de tiempo (minutos, típico 5-15)

    Returns:
        Dict con misma estructura que generate_hyetograph_uniform pero con:
        - Patrón de lluvia no uniforme
        - Pico de intensidad al centro de la tormenta
        - method: 'alternating_block'
        - idf_params: Dict con parámetros IDF usados

    Raises:
        ValueError: Parámetros inválidos
        HyetographGenerationError: Error en cálculo IDF

    Example:
        >>> result = generate_hyetograph_alternating_block(
        ...     total_rainfall_mm=50.0,
        ...     duration_hours=2.0,
        ...     P3_10=70,
        ...     Tr=10,
        ...     time_step_minutes=10
        ... )
        >>> max_idx = result['intensity_mmh'].index(max(result['intensity_mmh']))
        >>> # El pico debería estar cerca del centro
    """
    # Validaciones
    if total_rainfall_mm <= 0:
        raise ValueError(f"Precipitación total debe ser > 0. Valor: {total_rainfall_mm}")
    if duration_hours <= 0:
        raise ValueError(f"Duración debe ser > 0. Valor: {duration_hours}")
    if time_step_minutes <= 0 or time_step_minutes > duration_hours * 60:
        raise ValueError(f"Time step inválido: {time_step_minutes} min")
    if P3_10 < 50 or P3_10 > 100:
        raise ValueError(f"P3_10 debe estar entre 50-100mm. Valor: {P3_10}")
    if Tr < 2:
        raise ValueError(f"Período de retorno debe ser >= 2 años. Valor: {Tr}")

    try:
        # Convertir duración a minutos
        duration_minutes = duration_hours * 60

        # Número de intervalos
        num_intervals = int(duration_minutes / time_step_minutes)
        time_step_hours = time_step_minutes / 60

        # Paso 1: Calcular intensidades para duraciones acumuladas usando IDF
        intensities = []
        precipitations = []

        for i in range(1, num_intervals + 1):
            duration_i = i * time_step_hours

            # Calcular intensidad usando curva IDF
            idf_result = calculate_intensity_idf(
                P3_10=P3_10,
                Tr=Tr,
                d=duration_i,
                Ac=area_km2
            )

            intensity = idf_result['I_mmh']
            precipitation = idf_result['P_mm']

            intensities.append(intensity)
            precipitations.append(precipitation)

        # Paso 2: Calcular incrementos de precipitación
        increments = []
        increments.append(precipitations[0])  # Primer incremento

        for i in range(1, len(precipitations)):
            increment = precipitations[i] - precipitations[i-1]
            increments.append(increment)

        # Paso 3: Ordenar incrementos en patrón alternado (pico al centro)
        # Ordenar de mayor a menor
        sorted_increments = sorted(increments, reverse=True)

        # Crear patrón alternado: colocar el más alto al centro
        alternating_pattern = []
        left = []
        right = []

        for i, value in enumerate(sorted_increments):
            if i % 2 == 0:
                right.append(value)
            else:
                left.insert(0, value)  # Insertar al inicio

        alternating_pattern = left + right

        # Paso 4: Generar series temporales
        time_steps = [i * time_step_minutes for i in range(num_intervals + 1)]

        # Lluvia por intervalo (agregar 0 al inicio)
        rainfall_mm = [0] + alternating_pattern

        # Calcular intensidades correspondientes
        intensity_series = []
        for rain in rainfall_mm:
            # I (mm/h) = rainfall (mm) / time_step (h)
            intensity = (rain / time_step_hours) if time_step_hours > 0 else 0
            intensity_series.append(intensity)

        # Calcular acumulados
        cumulative_mm = []
        cumulative = 0
        for rain in rainfall_mm:
            cumulative += rain
            cumulative_mm.append(cumulative)

        # Ajustar si la suma no coincide exactamente con total_rainfall_mm
        # (por errores de redondeo)
        actual_total = sum(alternating_pattern)
        if abs(actual_total - total_rainfall_mm) > 0.1:  # Tolerancia 0.1mm
            # Aplicar factor de corrección
            correction_factor = total_rainfall_mm / actual_total
            rainfall_mm = [r * correction_factor for r in rainfall_mm]
            intensity_series = [i * correction_factor for i in intensity_series]
            cumulative_mm = []
            cumulative = 0
            for rain in rainfall_mm:
                cumulative += rain
                cumulative_mm.append(cumulative)

        return {
            'time_steps': time_steps,
            'rainfall_mm': rainfall_mm,
            'intensity_mmh': intensity_series,
            'cumulative_mm': cumulative_mm,
            'method': 'alternating_block',
            'duration_hours': duration_hours,
            'total_rainfall_mm': total_rainfall_mm,
            'time_step_minutes': time_step_minutes,
            'num_intervals': num_intervals,
            'idf_params': {
                'P3_10': P3_10,
                'Tr': Tr,
                'area_km2': area_km2
            },
            'peak_intensity_mmh': max(intensity_series),
            'peak_time_minutes': time_steps[intensity_series.index(max(intensity_series))]
        }

    except Exception as e:
        raise HyetographGenerationError(f"Error generando hietograma: {str(e)}") from e


def generate_hyetograph(
    total_rainfall_mm: float,
    duration_hours: float,
    method: str = 'alternating_block',
    time_step_minutes: float = 5,
    P3_10: float = None,
    Tr: float = None,
    area_km2: float = None
) -> Dict:
    """
    Función principal para generar hietogramas.

    Orquesta la generación de hietogramas según el método seleccionado.

    Args:
        total_rainfall_mm: Precipitación total (mm)
        duration_hours: Duración (horas)
        method: 'uniform' | 'alternating_block'
        time_step_minutes: Intervalo de tiempo (minutos)
        P3_10: Parámetro P₃,₁₀ para IDF (requerido si method='alternating_block')
        Tr: Período de retorno (requerido si method='alternating_block')
        area_km2: Área de cuenca (opcional)

    Returns:
        Dict con estructura de hietograma

    Raises:
        ValueError: Método no soportado o parámetros faltantes
        HyetographGenerationError: Error en generación

    Example:
        >>> # Método uniforme
        >>> h1 = generate_hyetograph(50.0, 2.0, method='uniform')
        >>>
        >>> # Método alternating block
        >>> h2 = generate_hyetograph(
        ...     50.0, 2.0,
        ...     method='alternating_block',
        ...     P3_10=70, Tr=10
        ... )
    """
    valid_methods = ['uniform', 'alternating_block']

    if method not in valid_methods:
        raise ValueError(f"Método '{method}' no soportado. Opciones: {valid_methods}")

    if method == 'uniform':
        return generate_hyetograph_uniform(
            total_rainfall_mm=total_rainfall_mm,
            duration_hours=duration_hours,
            time_step_minutes=time_step_minutes
        )

    elif method == 'alternating_block':
        if P3_10 is None or Tr is None:
            raise ValueError(
                "Para method='alternating_block' se requieren P3_10 y Tr"
            )

        return generate_hyetograph_alternating_block(
            total_rainfall_mm=total_rainfall_mm,
            duration_hours=duration_hours,
            P3_10=P3_10,
            Tr=Tr,
            area_km2=area_km2,
            time_step_minutes=time_step_minutes
        )
