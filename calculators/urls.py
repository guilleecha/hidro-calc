"""
URLs para las calculadoras hidrológicas rápidas.
"""

from django.urls import path
from . import views

app_name = 'calculators'

urlpatterns = [
    # Vistas de templates (HTML)
    path('rational/', views.rational_calculator_view, name='rational'),
    path('idf/', views.idf_calculator_view, name='idf'),

    # API endpoints (JSON)
    path(
        'api/rational/calculate',
        views.api_rational_calculate,
        name='api_rational_calculate'
    ),
    path(
        'api/rational/weighted-c',
        views.api_rational_weighted_c,
        name='api_rational_weighted_c'
    ),
    path(
        'api/idf/calculate',
        views.api_idf_calculate,
        name='api_idf_calculate'
    ),
    path(
        'api/runoff-coefficients',
        views.api_runoff_coefficients,
        name='api_runoff_coefficients'
    ),
    path(
        'api/p3-10-values',
        views.api_p3_10_values,
        name='api_p3_10_values'
    ),
]
