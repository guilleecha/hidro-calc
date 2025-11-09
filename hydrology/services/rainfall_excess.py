"""
Rainfall Excess Calculation Service

Calcula lluvia efectiva (escorrentía) considerando pérdidas por infiltración.
Métodos: Racional (C × P) y SCS Curve Number
"""

from typing import Dict, List


class RainfallExcessError(Exception):
    """Error en cálculo de lluvia efectiva"""
    pass


def calculate_rainfall_excess_rational(
    rainfall_series: List[float],
    C: float,
    time_step_minutes: float = 5
) -> Dict:
    """Calcula lluvia efectiva usando Método Racional: Pe = C × P"""
    if not isinstance(rainfall_series, list) or len(rainfall_series) == 0:
        raise ValueError("rainfall_series debe ser lista no vacía")
    if C < 0 or C > 1:
        raise ValueError(f"C debe estar entre 0-1. Valor: {C}")

    excess_series = []
    infiltration_series = []
    cumulative_excess = []
    cumulative_infiltration = []
    sum_excess = 0
    sum_infiltration = 0

    for rainfall in rainfall_series:
        if rainfall < 0:
            raise ValueError(f"Rainfall negativo: {rainfall}")

        excess = C * rainfall
        infiltration = rainfall - excess

        excess_series.append(excess)
        infiltration_series.append(infiltration)
        sum_excess += excess
        sum_infiltration += infiltration
        cumulative_excess.append(sum_excess)
        cumulative_infiltration.append(sum_infiltration)

    total_rainfall = sum(rainfall_series)

    return {
        'excess_series': excess_series,
        'infiltration_series': infiltration_series,
        'cumulative_excess_mm': cumulative_excess,
        'cumulative_infiltration_mm': cumulative_infiltration,
        'total_rainfall_mm': total_rainfall,
        'total_excess_mm': sum_excess,
        'total_infiltration_mm': sum_infiltration,
        'runoff_coefficient': C,
        'method': 'rational',
        'time_step_minutes': time_step_minutes,
        'num_intervals': len(rainfall_series)
    }


def calculate_rainfall_excess_scs(
    rainfall_series: List[float],
    CN: int,
    time_step_minutes: float = 5,
    antecedent_condition: str = 'AMC-II'
) -> Dict:
    """Calcula lluvia efectiva usando SCS Curve Number"""
    if CN < 30 or CN > 100:
        raise ValueError(f"CN debe estar entre 30-100. Valor: {CN}")

    # Ajustar CN por AMC
    CN_adjusted = CN
    if antecedent_condition == 'AMC-I':
        CN_adjusted = CN / (2.281 - 0.01281 * CN)
    elif antecedent_condition == 'AMC-III':
        CN_adjusted = CN / (0.427 + 0.00573 * CN)

    CN_adjusted = round(CN_adjusted, 1)
    S_mm = (25400 / CN_adjusted) - 254
    Ia_mm = 0.2 * S_mm

    excess_series = []
    infiltration_series = []
    cumulative_rainfall = []
    cumulative_excess = []
    P_accumulated = 0
    Pe_accumulated = 0

    for rainfall in rainfall_series:
        P_accumulated += rainfall
        cumulative_rainfall.append(P_accumulated)

        if P_accumulated <= Ia_mm:
            Pe_accumulated_new = 0
        else:
            numerator = (P_accumulated - Ia_mm) ** 2
            denominator = P_accumulated - Ia_mm + S_mm
            Pe_accumulated_new = numerator / denominator if denominator > 0 else 0

        Pe_increment = Pe_accumulated_new - Pe_accumulated
        Pe_accumulated = Pe_accumulated_new
        infiltration_increment = rainfall - Pe_increment

        excess_series.append(Pe_increment)
        infiltration_series.append(infiltration_increment)
        cumulative_excess.append(Pe_accumulated)

    total_rainfall = sum(rainfall_series)
    total_excess = cumulative_excess[-1] if cumulative_excess else 0

    return {
        'excess_series': excess_series,
        'infiltration_series': infiltration_series,
        'cumulative_excess_mm': cumulative_excess,
        'total_rainfall_mm': total_rainfall,
        'total_excess_mm': total_excess,
        'total_infiltration_mm': total_rainfall - total_excess,
        'runoff_coefficient': total_excess / total_rainfall if total_rainfall > 0 else 0,
        'method': 'scs_curve_number',
        'CN_original': CN,
        'CN_adjusted': CN_adjusted,
        'S_mm': S_mm,
        'Ia_mm': Ia_mm,
        'time_step_minutes': time_step_minutes
    }


def calculate_rainfall_excess(
    rainfall_series: List[float],
    method: str = 'rational',
    time_step_minutes: float = 5,
    C: float = None,
    CN: int = None,
    antecedent_condition: str = 'AMC-II'
) -> Dict:
    """Función principal para calcular lluvia efectiva"""
    if method == 'rational':
        if C is None:
            raise ValueError("method='rational' requiere C")
        return calculate_rainfall_excess_rational(rainfall_series, C, time_step_minutes)
    elif method == 'scs_curve_number':
        if CN is None:
            raise ValueError("method='scs_curve_number' requiere CN")
        return calculate_rainfall_excess_scs(rainfall_series, CN, time_step_minutes, antecedent_condition)
    else:
        raise ValueError(f"Método '{method}' no soportado")
