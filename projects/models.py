"""
Model: Project - Proyecto hidrológico

Modelo para gestión de proyectos de hidrología.
Contiene información general del proyecto, ubicación y metadatos.
"""

from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    """Modelo para proyectos de hidrología"""

    name = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        help_text="Nombre del proyecto"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Descripción del proyecto"
    )
    location = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Ubicación del proyecto"
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="País"
    )
    region = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Región/Departamento"
    )
    timezone = models.CharField(
        max_length=50,
        default="UTC",
        help_text="Zona horaria"
    )

    # Owner (relación con User de Django, nullable por ahora)
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='projects',
        db_index=True,
        help_text="Propietario del proyecto"
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Indica si el proyecto está activo"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Fecha de última actualización"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"

    def __str__(self):
        return self.name

    @property
    def total_watersheds(self):
        """Número total de cuencas en el proyecto"""
        return self.watersheds.count()
