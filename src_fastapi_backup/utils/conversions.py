"""
Funciones de conversión de unidades para cálculos hidrológicos e hidráulicos.
"""

from typing import Dict


# ===== CONVERSIONES DE ÁREA =====

def ha_to_m2(area_ha: float) -> float:
    """Convierte hectáreas a metros cuadrados."""
    return area_ha * 10000


def m2_to_ha(area_m2: float) -> float:
    """Convierte metros cuadrados a hectáreas."""
    return area_m2 / 10000


def ha_to_km2(area_ha: float) -> float:
    """Convierte hectáreas a kilómetros cuadrados."""
    return area_ha / 100


def km2_to_ha(area_km2: float) -> float:
    """Convierte kilómetros cuadrados a hectáreas."""
    return area_km2 * 100


# ===== CONVERSIONES DE CAUDAL =====

def ls_to_m3s(flow_ls: float) -> float:
    """Convierte litros por segundo a metros cúbicos por segundo."""
    return flow_ls / 1000


def m3s_to_ls(flow_m3s: float) -> float:
    """Convierte metros cúbicos por segundo a litros por segundo."""
    return flow_m3s * 1000


def m3s_to_m3h(flow_m3s: float) -> float:
    """Convierte m³/s a m³/h."""
    return flow_m3s * 3600


def m3h_to_m3s(flow_m3h: float) -> float:
    """Convierte m³/h a m³/s."""
    return flow_m3h / 3600


def ls_to_m3h(flow_ls: float) -> float:
    """Convierte L/s a m³/h."""
    return flow_ls * 3.6


def m3h_to_ls(flow_m3h: float) -> float:
    """Convierte m³/h a L/s."""
    return flow_m3h / 3.6


# ===== CONVERSIONES DE LONGITUD =====

def mm_to_m(length_mm: float) -> float:
    """Convierte milímetros a metros."""
    return length_mm / 1000


def m_to_mm(length_m: float) -> float:
    """Convierte metros a milímetros."""
    return length_m * 1000


def km_to_m(length_km: float) -> float:
    """Convierte kilómetros a metros."""
    return length_km * 1000


def m_to_km(length_m: float) -> float:
    """Convierte metros a kilómetros."""
    return length_m / 1000


# ===== CONVERSIONES DE VELOCIDAD =====

def ms_to_kmh(velocity_ms: float) -> float:
    """Convierte m/s a km/h."""
    return velocity_ms * 3.6


def kmh_to_ms(velocity_kmh: float) -> float:
    """Convierte km/h a m/s."""
    return velocity_kmh / 3.6


# ===== CONVERSIONES DE INTENSIDAD DE LLUVIA =====

def mmh_to_ms(intensity_mmh: float) -> float:
    """Convierte mm/h a m/s."""
    return intensity_mmh / (1000 * 3600)


def ms_to_mmh(intensity_ms: float) -> float:
    """Convierte m/s a mm/h."""
    return intensity_ms * 1000 * 3600


# ===== FUNCIÓN UNIVERSAL DE CONVERSIÓN =====

def convert_units(
    value: float,
    from_unit: str,
    to_unit: str
) -> float:
    """
    Función universal de conversión de unidades.

    Args:
        value: Valor a convertir
        from_unit: Unidad de origen
        to_unit: Unidad de destino

    Returns:
        float: Valor convertido

    Raises:
        ValueError: Si las unidades no son soportadas o incompatibles

    Ejemplo:
        >>> convert_units(100, "L/s", "m3/s")
        0.1
        >>> convert_units(5, "ha", "m2")
        50000.0
    """
    # Normalizar nombres de unidades
    from_unit = from_unit.lower().replace(" ", "").replace("/", "")
    to_unit = to_unit.lower().replace(" ", "").replace("/", "")

    # Si las unidades son iguales, no hay conversión
    if from_unit == to_unit:
        return value

    # Diccionario de conversiones
    conversions = {
        # Área
        ("ha", "m2"): lambda x: ha_to_m2(x),
        ("m2", "ha"): lambda x: m2_to_ha(x),
        ("ha", "km2"): lambda x: ha_to_km2(x),
        ("km2", "ha"): lambda x: km2_to_ha(x),

        # Caudal
        ("ls", "m3s"): lambda x: ls_to_m3s(x),
        ("m3s", "ls"): lambda x: m3s_to_ls(x),
        ("m3s", "m3h"): lambda x: m3s_to_m3h(x),
        ("m3h", "m3s"): lambda x: m3h_to_m3s(x),
        ("ls", "m3h"): lambda x: ls_to_m3h(x),
        ("m3h", "ls"): lambda x: m3h_to_ls(x),

        # Longitud
        ("mm", "m"): lambda x: mm_to_m(x),
        ("m", "mm"): lambda x: m_to_mm(x),
        ("km", "m"): lambda x: km_to_m(x),
        ("m", "km"): lambda x: m_to_km(x),

        # Velocidad
        ("ms", "kmh"): lambda x: ms_to_kmh(x),
        ("kmh", "ms"): lambda x: kmh_to_ms(x),

        # Intensidad
        ("mmh", "ms"): lambda x: mmh_to_ms(x),
        ("ms", "mmh"): lambda x: ms_to_mmh(x),
    }

    # Buscar la conversión
    key = (from_unit, to_unit)
    if key in conversions:
        return conversions[key](value)
    else:
        raise ValueError(
            f"Conversión no soportada: {from_unit} → {to_unit}"
        )


def get_flow_in_multiple_units(flow_ls: float) -> Dict[str, float]:
    """
    Convierte un caudal en L/s a múltiples unidades.

    Args:
        flow_ls: Caudal en L/s

    Returns:
        Dict con el caudal en diferentes unidades

    Ejemplo:
        >>> get_flow_in_multiple_units(100)
        {
            'L/s': 100.0,
            'm3/s': 0.1,
            'm3/h': 360.0,
            'm3/day': 8640.0
        }
    """
    return {
        "L/s": round(flow_ls, 2),
        "m3/s": round(ls_to_m3s(flow_ls), 4),
        "m3/h": round(ls_to_m3h(flow_ls), 2),
        "m3/day": round(ls_to_m3h(flow_ls) * 24, 2)
    }


def get_area_in_multiple_units(area_ha: float) -> Dict[str, float]:
    """
    Convierte un área en ha a múltiples unidades.

    Args:
        area_ha: Área en hectáreas

    Returns:
        Dict con el área en diferentes unidades

    Ejemplo:
        >>> get_area_in_multiple_units(5)
        {
            'ha': 5.0,
            'm2': 50000.0,
            'km2': 0.05
        }
    """
    return {
        "ha": round(area_ha, 4),
        "m2": round(ha_to_m2(area_ha), 2),
        "km2": round(ha_to_km2(area_ha), 4)
    }


if __name__ == "__main__":
    # Ejemplos de uso
    print("=== Conversiones de Unidades ===\n")

    print("Área:")
    print(f"5 ha = {ha_to_m2(5)} m²")
    print(f"5 ha = {ha_to_km2(5)} km²\n")

    print("Caudal:")
    print(f"100 L/s = {ls_to_m3s(100)} m³/s")
    print(f"100 L/s = {ls_to_m3h(100)} m³/h\n")

    print("Caudal en múltiples unidades:")
    flow_dict = get_flow_in_multiple_units(150)
    for unit, value in flow_dict.items():
        print(f"  {value} {unit}")
