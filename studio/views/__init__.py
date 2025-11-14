"""
Views for HidroStudio Professional
Re-exports all views for easy importing
"""

from .dashboard_views import studio_index, dashboard
from .watershed_views import (
    watershed_detail,
    watershed_create,
    watershed_edit,
    watershed_delete
)
from .hydrograph_views import hyetograph_view, hydrograph_compare
from .project_views import project_create
from .chart_helpers import (
    calculate_optimal_timestep,
    generate_hyetograph_data,
    generate_hydrograph_data
)

__all__ = [
    # Dashboard views
    'studio_index',
    'dashboard',
    # Watershed views
    'watershed_detail',
    'watershed_create',
    'watershed_edit',
    'watershed_delete',
    # Hydrograph views
    'hyetograph_view',
    'hydrograph_compare',
    # Project views
    'project_create',
    # Helper functions
    'calculate_optimal_timestep',
    'generate_hyetograph_data',
    'generate_hydrograph_data',
]
