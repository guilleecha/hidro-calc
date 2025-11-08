"""
URLs para API REST de HidroCalc
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProjectViewSet,
    WatershedViewSet,
    DesignStormViewSet,
    HydrographViewSet,
    RainfallDataViewSet,
)

# Router de DRF para registrar ViewSets
router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'watersheds', WatershedViewSet, basename='watershed')
router.register(r'design-storms', DesignStormViewSet, basename='designstorm')
router.register(r'hydrographs', HydrographViewSet, basename='hydrograph')
router.register(r'rainfall-data', RainfallDataViewSet, basename='rainfalldata')

urlpatterns = [
    path('', include(router.urls)),
]
