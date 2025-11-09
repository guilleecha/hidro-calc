"""
HidroStudio Professional - Views
Dashboard para análisis hidrológico integrado
"""

import json
import math
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from projects.models import Project
from watersheds.models import Watershed
from hydrology.models import DesignStorm, Hydrograph


def studio_index(request):
    """Vista principal de HidroStudio"""
    # Si no hay login, mostrar página de bienvenida
    if not request.user.is_authenticated:
        return render(request, 'studio/welcome.html')

    # Si hay login, redirigir al primer proyecto o mostrar crear proyecto
    projects = Project.objects.filter(owner=request.user, is_active=True)

    if projects.exists():
        first_project = projects.first()
        return dashboard(request, first_project.id)

    # No hay proyectos, mostrar página para crear
    return render(request, 'studio/no_projects.html')


def dashboard(request, project_id=None):
    """Dashboard principal del proyecto"""

    # Si no hay project_id, intentar usar el primer proyecto del usuario
    if project_id is None:
        if request.user.is_authenticated:
            project = Project.objects.filter(
                owner=request.user,
                is_active=True
            ).first()
            if project:
                project_id = project.id

    # Obtener proyecto o 404
    project = get_object_or_404(Project, id=project_id) if project_id else None

    # Obtener todas las cuencas del proyecto
    watersheds = []
    selected_watershed = None

    if project:
        watersheds = Watershed.objects.filter(project=project).select_related('project')

        # Seleccionar cuenca (primera por defecto o la especificada)
        watershed_id = request.GET.get('watershed')
        if watershed_id:
            selected_watershed = get_object_or_404(Watershed, id=watershed_id, project=project)
        elif watersheds.exists():
            selected_watershed = watersheds.first()

    # Obtener datos de la cuenca seleccionada
    design_storms = []
    hydrographs = []
    latest_storm = None

    if selected_watershed:
        design_storms = DesignStorm.objects.filter(
            watershed=selected_watershed
        ).order_by('-created_at')

        if design_storms.exists():
            latest_storm = design_storms.first()
            hydrographs = Hydrograph.objects.filter(
                design_storm=latest_storm
            ).order_by('method')

    # Calcular estadísticas rápidas
    stats = {}
    if hydrographs:
        stats = {
            'peak_discharge_max': max(h.peak_discharge_m3s for h in hydrographs),
            'peak_discharge_min': min(h.peak_discharge_m3s for h in hydrographs),
            'total_hydrographs': hydrographs.count(),
            'methods_used': [h.method for h in hydrographs],
        }

    # Obtener todos los proyectos del usuario (para sidebar)
    all_projects = []
    if request.user.is_authenticated:
        all_projects = Project.objects.filter(
            owner=request.user,
            is_active=True
        ).prefetch_related('watersheds')

    # Generar datos para gráficos
    hyetograph_data = None
    hydrographs_data = []

    if latest_storm:
        # Generar datos de hietograma
        hyetograph_data = generate_hyetograph_data(latest_storm)

    if hydrographs:
        # Generar datos de hidrogramas para comparación
        for hydro in hydrographs:
            hydrographs_data.append(generate_hydrograph_data(hydro))

    context = {
        'project': project,
        'all_projects': all_projects,
        'watersheds': watersheds,
        'selected_watershed': selected_watershed,
        'design_storms': design_storms,
        'latest_storm': latest_storm,
        'hydrographs': hydrographs,
        'stats': stats,
        # Chart data
        'hyetograph_data': json.dumps(hyetograph_data) if hyetograph_data else None,
        'hydrographs_data': json.dumps(hydrographs_data) if hydrographs_data else None,
    }

    return render(request, 'studio/dashboard.html', context)


def watershed_detail(request, watershed_id):
    """Vista detallada de una cuenca"""
    watershed = get_object_or_404(Watershed, id=watershed_id)

    # Obtener tormentas y hidrogramas
    design_storms = DesignStorm.objects.filter(watershed=watershed).order_by('-created_at')

    context = {
        'watershed': watershed,
        'project': watershed.project,
        'design_storms': design_storms,
    }

    return render(request, 'studio/watershed_detail.html', context)


def hyetograph_view(request, storm_id):
    """Vista de hietograma de una tormenta"""
    storm = get_object_or_404(DesignStorm, id=storm_id)

    # TODO: Generar datos del hietograma
    # Por ahora mostramos datos básicos

    context = {
        'storm': storm,
        'watershed': storm.watershed,
        'project': storm.watershed.project,
    }

    return render(request, 'studio/hyetograph.html', context)


def hydrograph_compare(request, project_id):
    """Vista de comparación de hidrogramas"""
    project = get_object_or_404(Project, id=project_id)

    # Obtener IDs de hidrogramas a comparar (de query params)
    hydrograph_ids = request.GET.getlist('ids')

    hydrographs = []
    if hydrograph_ids:
        hydrographs = Hydrograph.objects.filter(
            id__in=hydrograph_ids
        ).select_related('design_storm__watershed')

    context = {
        'project': project,
        'hydrographs': hydrographs,
    }

    return render(request, 'studio/hydrograph_compare.html', context)


# =============================================================================
# Helper Functions for Chart Data Generation
# =============================================================================

def calculate_optimal_timestep(storm, custom_timestep=None):
    """
    Calculate optimal timestep for hyetograph discretization

    Based on:
    - HEC-HMS: Δt ≤ Tc/5
    - NRCS: Δt = 0.2 × Tc
    - Duration-based rules for large storms

    Args:
        storm: DesignStorm instance
        custom_timestep: Optional user-defined timestep in minutes

    Returns:
        float: Optimal timestep in minutes
    """
    if custom_timestep:
        return float(custom_timestep)

    watershed = storm.watershed
    duration_hours = float(storm.duration_hours)

    # If watershed has Tc, use it to calculate timestep
    if watershed and watershed.tc_minutes:
        tc_minutes = float(watershed.tc_minutes)

        # Rule: Δt ≤ Tc/5 (HEC-HMS)
        timestep_from_tc = tc_minutes / 5

        # Cap at reasonable limits
        if timestep_from_tc < 1:
            timestep = 1  # Minimum 1 minute
        elif timestep_from_tc > 30:
            timestep = 30  # Maximum 30 minutes
        else:
            # Round to nearest 5 minutes for practical purposes
            timestep = round(timestep_from_tc / 5) * 5
            if timestep == 0:
                timestep = 5
    else:
        # Fallback: Duration-based rules (when Tc not available)
        if duration_hours <= 1:
            timestep = 5  # 5 min for short storms
        elif duration_hours <= 6:
            timestep = 10  # 10 min for medium storms
        elif duration_hours <= 24:
            timestep = 15  # 15 min for daily storms
        else:
            timestep = 30  # 30 min for multi-day storms

    return timestep


def generate_hyetograph_data(storm, custom_timestep=None):
    """
    Generate hyetograph data (rainfall distribution over time)
    Uses Alternating Block Method

    Timestep priority:
    1. custom_timestep parameter (if provided)
    2. storm.time_step_minutes (if not default)
    3. Auto-calculated from Tc (Δt ≤ Tc/5 per HEC-HMS)
    4. Auto-calculated from duration (fallback)

    Args:
        storm: DesignStorm instance
        custom_timestep: Optional override timestep in minutes

    Returns:
        dict: {
            'time_steps': [...],
            'intensity': [...],
            'timestep': float,
            'method': str
        }
    """
    duration_hours = float(storm.duration_hours)
    total_rainfall = float(storm.total_rainfall_mm)

    # Determine timestep with priority
    if custom_timestep:
        interval = float(custom_timestep)
        method = f"Custom override ({interval} min)"
    elif storm.time_step_minutes and storm.time_step_minutes != 5:
        # User explicitly set a timestep (not default)
        interval = float(storm.time_step_minutes)
        method = f"User-defined ({interval} min)"
    else:
        # Auto-calculate optimal timestep
        interval = calculate_optimal_timestep(storm, None)
        if storm.watershed and storm.watershed.tc_minutes:
            method = f"Auto Tc-based ({interval} min, Tc={storm.watershed.tc_minutes:.0f} min)"
        else:
            method = f"Auto duration-based ({interval} min)"

    num_intervals = int((duration_hours * 60) / interval)
    time_steps = []
    intensity = []

    # Alternating Block: peak in the middle
    peak_index = num_intervals // 2

    for i in range(num_intervals):
        time_steps.append(round(i * interval, 1))

        # Distance from peak
        dist_from_peak = abs(i - peak_index)
        # Intensity decreases with distance from peak
        relative_intensity = 1 - (dist_from_peak / num_intervals)
        # Calculate intensity (convert mm to mm/h)
        intensity_value = (total_rainfall / duration_hours) * (1 + relative_intensity)

        intensity.append(round(intensity_value, 2))

    return {
        'time_steps': time_steps,
        'intensity': intensity,
        'timestep': interval,
        'method': method
    }


def generate_hydrograph_data(hydrograph):
    """
    Generate hydrograph data from stored hydrograph_data JSON
    or create sample triangular hydrograph

    Args:
        hydrograph: Hydrograph instance

    Returns:
        dict: {'time_steps': [...], 'discharge': [...], 'name': '...'}
    """
    # If hydrograph_data exists, use it
    if hydrograph.hydrograph_data:
        data = json.loads(hydrograph.hydrograph_data) if isinstance(hydrograph.hydrograph_data, str) else hydrograph.hydrograph_data
        return {
            'name': hydrograph.get_method_display(),
            'time_steps': data.get('time_steps', []),
            'discharge': data.get('discharge', [])
        }

    # Otherwise, generate sample triangular hydrograph
    peak_discharge = float(hydrograph.peak_discharge_m3s)
    time_to_peak = float(hydrograph.time_to_peak_minutes)
    base_time = time_to_peak * 3  # Approximate base time
    interval = 5  # 5 minutes

    time_steps = []
    discharge = []

    t = 0
    while t <= base_time:
        time_steps.append(t)

        if t <= time_to_peak:
            # Rising limb
            q = (peak_discharge / time_to_peak) * t
        else:
            # Falling limb
            time_from_peak = t - time_to_peak
            falling_time = base_time - time_to_peak
            q = peak_discharge * (1 - (time_from_peak / falling_time))

        discharge.append(round(max(0, q), 2))
        t += interval

    return {
        'name': hydrograph.get_method_display(),
        'time_steps': time_steps,
        'discharge': discharge
    }
