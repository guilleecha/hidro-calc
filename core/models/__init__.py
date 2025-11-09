"""
Models de HidroCalc - Re-exports para backward compatibility

Los modelos ahora viven en apps especializadas:
- projects.models.Project
- watersheds.models.Watershed
- hydrology.models.DesignStorm
- hydrology.models.Hydrograph
- hydrology.models.RainfallData

Este __init__.py mantiene los imports antiguos funcionando.
"""

# Imports desde las nuevas apps
from projects.models import Project
from watersheds.models import Watershed
from hydrology.models import DesignStorm, Hydrograph, RainfallData

__all__ = [
    'Project',
    'Watershed',
    'DesignStorm',
    'Hydrograph',
    'RainfallData',
]
