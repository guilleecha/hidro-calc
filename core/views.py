"""
Core Views - Vistas principales del sitio
"""

from django.shortcuts import render


def home(request):
    """
    Vista principal/home del sitio
    Muestra landing page con acceso a calculadoras y HidroStudio
    """
    context = {
        'user_authenticated': request.user.is_authenticated,
    }
    return render(request, 'home.html', context)
