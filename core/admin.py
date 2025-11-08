"""
Django Admin Configuration para HidroCalc Core Models
"""

from django.contrib import admin
from .models import Project, Watershed, DesignStorm, Hydrograph, RainfallData


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin para proyectos"""
    list_display = ['name', 'location', 'country', 'owner', 'is_active', 'total_watersheds', 'created_at']
    list_filter = ['is_active', 'country', 'created_at']
    search_fields = ['name', 'location', 'description']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'description', 'owner', 'is_active')
        }),
        ('Ubicación', {
            'fields': ('location', 'country', 'region', 'timezone')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Watershed)
class WatershedAdmin(admin.ModelAdmin):
    """Admin para cuencas"""
    list_display = ['name', 'project', 'area_hectareas', 'tc_horas', 'nc_scs', 'created_at']
    list_filter = ['project', 'created_at']
    search_fields = ['name', 'description', 'project__name']
    readonly_fields = ['created_at', 'updated_at', 'area_m2', 'tc_minutes']

    fieldsets = (
        ('Información Básica', {
            'fields': ('project', 'name', 'description')
        }),
        ('Características Hidráulicas', {
            'fields': ('area_hectareas', 'tc_horas', 'nc_scs', 'c_racional')
        }),
        ('Ubicación', {
            'fields': ('latitude', 'longitude', 'elevation_m')
        }),
        ('Metadata', {
            'fields': ('extra_metadata',),
            'classes': ('collapse',)
        }),
        ('Información del Sistema', {
            'fields': ('created_at', 'updated_at', 'area_m2', 'tc_minutes'),
            'classes': ('collapse',)
        }),
    )


@admin.register(DesignStorm)
class DesignStormAdmin(admin.ModelAdmin):
    """Admin para tormentas de diseño"""
    list_display = ['name', 'watershed', 'return_period_years', 'duration_hours', 'total_rainfall_mm', 'distribution_type', 'created_at']
    list_filter = ['return_period_years', 'distribution_type', 'created_at']
    search_fields = ['name', 'description', 'watershed__name']
    readonly_fields = ['created_at', 'updated_at', 'duration_minutes', 'average_intensity_mm_h']

    fieldsets = (
        ('Información Básica', {
            'fields': ('watershed', 'name', 'description')
        }),
        ('Parámetros de Tormenta', {
            'fields': ('return_period_years', 'duration_hours', 'total_rainfall_mm', 'distribution_type', 'time_step_minutes')
        }),
        ('Parámetros SCS', {
            'fields': ('initial_abstraction_mm', 'storage_parameter_mm'),
            'classes': ('collapse',)
        }),
        ('Valores Calculados', {
            'fields': ('duration_minutes', 'average_intensity_mm_h'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('extra_metadata', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Hydrograph)
class HydrographAdmin(admin.ModelAdmin):
    """Admin para hidrogramas"""
    list_display = ['name', 'design_storm', 'method', 'peak_discharge_m3s', 'time_to_peak_minutes', 'created_at']
    list_filter = ['method', 'created_at']
    search_fields = ['name', 'notes', 'design_storm__name']
    readonly_fields = ['created_at', 'updated_at', 'peak_discharge_lps_calculated', 'time_to_peak_hours']

    fieldsets = (
        ('Información Básica', {
            'fields': ('design_storm', 'name', 'method')
        }),
        ('Resultados - Caudal', {
            'fields': ('peak_discharge_m3s', 'peak_discharge_lps', 'time_to_peak_minutes')
        }),
        ('Resultados - Volumen', {
            'fields': ('total_runoff_mm', 'total_runoff_m3', 'volume_hm3')
        }),
        ('Serie Temporal', {
            'fields': ('hydrograph_data',),
            'description': 'Serie temporal del hidrograma en formato JSON'
        }),
        ('Metadata de Cálculo', {
            'fields': ('rainfall_excess_mm', 'infiltration_total_mm', 'notes'),
            'classes': ('collapse',)
        }),
        ('Valores Calculados', {
            'fields': ('peak_discharge_lps_calculated', 'time_to_peak_hours', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(RainfallData)
class RainfallDataAdmin(admin.ModelAdmin):
    """Admin para datos de lluvia"""
    list_display = ['event_date', 'watershed', 'total_rainfall_mm', 'return_period_years', 'duration_hours', 'source']
    list_filter = ['event_date', 'source', 'watershed']
    search_fields = ['notes', 'watershed__name', 'source']
    readonly_fields = ['created_at']

    fieldsets = (
        ('Información del Evento', {
            'fields': ('watershed', 'event_date', 'source')
        }),
        ('Datos de Lluvia', {
            'fields': ('total_rainfall_mm', 'duration_hours', 'return_period_years')
        }),
        ('Serie Temporal', {
            'fields': ('rainfall_series',),
            'description': 'Serie temporal de lluvia en formato JSON'
        }),
        ('Notas', {
            'fields': ('notes', 'created_at'),
            'classes': ('collapse',)
        }),
    )
