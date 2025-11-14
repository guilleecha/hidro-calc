"""
Hydrograph Views - HidroStudio Professional
Vistas para visualización de hietogramas e hidrogramas
"""

from django.shortcuts import render, get_object_or_404
from projects.models import Project
from hydrology.models import DesignStorm, Hydrograph


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
