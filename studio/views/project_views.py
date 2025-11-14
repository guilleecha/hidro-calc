"""
Project Views - HidroStudio Professional
Vistas para gestión de proyectos (CRUD)
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from studio.forms import ProjectCreateForm


@login_required
def project_create(request):
    """Vista para crear un nuevo proyecto"""
    if request.method == 'POST':
        form = ProjectCreateForm(request.POST, user=request.user)
        if form.is_valid():
            project = form.save()
            messages.success(
                request,
                f'Proyecto "{project.name}" creado exitosamente.'
            )
            # Redirigir al dashboard del nuevo proyecto
            return redirect('studio:dashboard_project', project_id=project.id)
    else:
        form = ProjectCreateForm(user=request.user)

    context = {
        'form': form,
        'title': 'Crear Nuevo Proyecto'
    }
    return render(request, 'studio/project_create.html', context)
