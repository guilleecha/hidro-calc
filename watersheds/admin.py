"""
Django Admin Configuration para Watersheds
"""

from django.contrib import admin
from .models import Watershed


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
