"""
Watershed Views - HidroStudio Professional
Vistas relacionadas con cuencas hidrográficas
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from projects.models import Project
from watersheds.models import Watershed
from hydrology.models import DesignStorm
from studio.forms import WatershedCreateForm, WatershedEditForm


@login_required
def watershed_create(request, project_id):
    """Vista para crear una nueva cuenca en un proyecto"""
    # Obtener el proyecto y verificar que pertenece al usuario
    project = get_object_or_404(Project, id=project_id, owner=request.user)

    if request.method == 'POST':
        form = WatershedCreateForm(request.POST, project=project)
        if form.is_valid():
            watershed = form.save()
            messages.success(
                request,
                f'Cuenca "{watershed.name}" creada exitosamente.'
            )
            # Redirigir al dashboard del proyecto
            return redirect('studio:dashboard_project', project_id=project.id)
    else:
        form = WatershedCreateForm(project=project)

    context = {
        'form': form,
        'title': 'Crear Nueva Cuenca',
        'project': project,
    }
    return render(request, 'studio/watershed_create.html', context)


@login_required
def watershed_edit(request, watershed_id):
    """Vista para editar una cuenca existente"""
    # Obtener la cuenca y verificar acceso
    watershed = get_object_or_404(Watershed, id=watershed_id)

    # Verificar que el usuario es propietario del proyecto
    if watershed.project.owner != request.user:
        messages.error(request, 'No tienes permiso para editar esta cuenca.')
        return redirect('studio:studio_index')

    if request.method == 'POST':
        form = WatershedEditForm(request.POST, instance=watershed, project=watershed.project)
        if form.is_valid():
            watershed = form.save()
            messages.success(
                request,
                f'Cuenca "{watershed.name}" actualizada exitosamente.'
            )
            return redirect('studio:dashboard_project', project_id=watershed.project.id)
    else:
        form = WatershedEditForm(instance=watershed, project=watershed.project)

    context = {
        'form': form,
        'title': 'Editar Cuenca',
        'watershed': watershed,
        'project': watershed.project,
    }
    return render(request, 'studio/watershed_edit.html', context)


@login_required
def watershed_delete(request, watershed_id):
    """Vista para eliminar una cuenca"""
    watershed = get_object_or_404(Watershed, id=watershed_id)

    # Verificar acceso
    if watershed.project.owner != request.user:
        messages.error(request, 'No tienes permiso para eliminar esta cuenca.')
        return redirect('studio:studio_index')

    if request.method == 'POST':
        project_id = watershed.project.id
        watershed_name = watershed.name
        watershed.delete()
        messages.success(
            request,
            f'Cuenca "{watershed_name}" eliminada exitosamente.'
        )
        return redirect('studio:dashboard_project', project_id=project_id)

    context = {
        'title': 'Confirmar Eliminación',
        'watershed': watershed,
        'project': watershed.project,
    }
    return render(request, 'studio/watershed_delete.html', context)


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
