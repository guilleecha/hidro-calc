"""
Dashboard Views - HidroStudio Professional
Vista principal y dashboard del proyecto
"""

import json
from django.shortcuts import render, get_object_or_404
from projects.models import Project
from watersheds.models import Watershed
from hydrology.models import DesignStorm, Hydrograph
from .chart_helpers import generate_hyetograph_data, generate_hydrograph_data


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
