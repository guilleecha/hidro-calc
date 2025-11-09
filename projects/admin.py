"""
Django Admin Configuration para Projects
"""

from django.contrib import admin
from .models import Project


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
