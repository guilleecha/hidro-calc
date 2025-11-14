"""
URLs para HidroStudio Professional
"""

from django.urls import path
from . import views

app_name = 'studio'

urlpatterns = [
    # Vista principal
    path('', views.studio_index, name='index'),

    # Project Management
    path('project/create/', views.project_create, name='project_create'),

    # Dashboard del proyecto
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/<int:project_id>/', views.dashboard, name='dashboard_project'),

    # Watershed Management (CRUD)
    path('project/<int:project_id>/watershed/create/', views.watershed_create, name='watershed_create'),
    path('watershed/<int:watershed_id>/', views.watershed_detail, name='watershed_detail'),
    path('watershed/<int:watershed_id>/edit/', views.watershed_edit, name='watershed_edit'),
    path('watershed/<int:watershed_id>/delete/', views.watershed_delete, name='watershed_delete'),

    # Hietograma
    path('hyetograph/<int:storm_id>/', views.hyetograph_view, name='hyetograph'),

    # Comparación de hidrogramas
    path('compare/<int:project_id>/', views.hydrograph_compare, name='hydrograph_compare'),
]
