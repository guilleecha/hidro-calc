"""
Design Storm Views - HidroStudio Professional
Vistas relacionadas con tormentas de diseño
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from watersheds.models import Watershed
from hydrology.models import DesignStorm
from studio.forms import DesignStormCreateForm, DesignStormEditForm


@login_required
def design_storm_create(request, watershed_id):
    """Vista para crear una nueva tormenta de diseño en una cuenca"""
    # Obtener la cuenca y verificar acceso
    watershed = get_object_or_404(Watershed, id=watershed_id)

    # Verificar que el usuario es propietario del proyecto
    if watershed.project.owner != request.user:
        messages.error(request, 'No tienes permiso para crear tormentas en esta cuenca.')
        return redirect('studio:index')

    if request.method == 'POST':
        form = DesignStormCreateForm(watershed, request.POST)
        if form.is_valid():
            design_storm = form.save()
            messages.success(
                request,
                f'Tormenta de diseño "{design_storm.name}" creada exitosamente.'
            )
            # Redirigir al dashboard del proyecto
            return redirect('studio:dashboard_project', project_id=watershed.project.id)
    else:
        form = DesignStormCreateForm(watershed)

    context = {
        'form': form,
        'title': 'Crear Nueva Tormenta de Diseño',
        'watershed': watershed,
        'project': watershed.project,
    }
    return render(request, 'studio/design_storm_create.html', context)


@login_required
def design_storm_edit(request, design_storm_id):
    """Vista para editar una tormenta de diseño existente"""
    # Obtener la tormenta de diseño y verificar acceso
    design_storm = get_object_or_404(DesignStorm, id=design_storm_id)

    # Verificar que el usuario es propietario del proyecto
    if design_storm.watershed.project.owner != request.user:
        messages.error(request, 'No tienes permiso para editar esta tormenta de diseño.')
        return redirect('studio:index')

    if request.method == 'POST':
        form = DesignStormEditForm(request.POST, instance=design_storm)
        if form.is_valid():
            design_storm = form.save()
            messages.success(
                request,
                f'Tormenta de diseño "{design_storm.name}" actualizada exitosamente.'
            )
            return redirect('studio:dashboard_project', project_id=design_storm.watershed.project.id)
    else:
        form = DesignStormEditForm(instance=design_storm)

    context = {
        'form': form,
        'title': 'Editar Tormenta de Diseño',
        'design_storm': design_storm,
        'watershed': design_storm.watershed,
        'project': design_storm.watershed.project,
    }
    return render(request, 'studio/design_storm_edit.html', context)


@login_required
def design_storm_delete(request, design_storm_id):
    """Vista para eliminar una tormenta de diseño"""
    design_storm = get_object_or_404(DesignStorm, id=design_storm_id)

    # Verificar acceso
    if design_storm.watershed.project.owner != request.user:
        messages.error(request, 'No tienes permiso para eliminar esta tormenta de diseño.')
        return redirect('studio:index')

    if request.method == 'POST':
        project_id = design_storm.watershed.project.id
        design_storm_name = design_storm.name
        design_storm.delete()
        messages.success(
            request,
            f'Tormenta de diseño "{design_storm_name}" eliminada exitosamente.'
        )
        return redirect('studio:dashboard_project', project_id=project_id)

    context = {
        'title': 'Confirmar Eliminación',
        'design_storm': design_storm,
        'watershed': design_storm.watershed,
        'project': design_storm.watershed.project,
    }
    return render(request, 'studio/design_storm_delete.html', context)
