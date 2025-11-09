"""
URLs para HidroStudio Professional
"""

from django.urls import path
from . import views

app_name = 'studio'

urlpatterns = [
    # Vista principal
    path('', views.studio_index, name='index'),

    # Dashboard del proyecto
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/<int:project_id>/', views.dashboard, name='dashboard_project'),

    # Detalle de cuenca
    path('watershed/<int:watershed_id>/', views.watershed_detail, name='watershed_detail'),

    # Hietograma
    path('hyetograph/<int:storm_id>/', views.hyetograph_view, name='hyetograph'),

    # Comparación de hidrogramas
    path('compare/<int:project_id>/', views.hydrograph_compare, name='hydrograph_compare'),
]
