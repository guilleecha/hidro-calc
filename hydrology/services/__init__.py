"""
Hydrology Services - Business Logic for Hydrological Calculations

This package contains services for:
- Hyetograph generation (temporal rainfall distribution)
- Rainfall excess calculation (runoff)
- Hydrograph calculation (flow hydrographs)
"""

from .hyetograph import (
    generate_hyetograph,
    generate_hyetograph_uniform,
    generate_hyetograph_alternating_block,
    HyetographGenerationError
)

from .rainfall_excess import (
    calculate_rainfall_excess,
    calculate_rainfall_excess_rational,
    calculate_rainfall_excess_scs,
    RainfallExcessError
)

__all__ = [
    # Hyetograph
    'generate_hyetograph',
    'generate_hyetograph_uniform',
    'generate_hyetograph_alternating_block',
    'HyetographGenerationError',
    # Rainfall Excess
    'calculate_rainfall_excess',
    'calculate_rainfall_excess_rational',
    'calculate_rainfall_excess_scs',
    'RainfallExcessError',
]
