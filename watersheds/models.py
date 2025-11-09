"""
Model: Watershed - Cuenca hidrográfica

Modelo para cuencas hidrográficas dentro de un proyecto.
Contiene parámetros físicos y características de la cuenca.
"""

from django.db import models
from projects.models import Project


class Watershed(models.Model):
    """Modelo para cuencas hidrográficas"""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='watersheds',
        db_index=True,
        help_text="Proyecto al que pertenece la cuenca"
    )

    name = models.CharField(
        max_length=255,
        help_text="Nombre de la cuenca"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Descripción de la cuenca"
    )

    # Características hidráulicas
    area_hectareas = models.FloatField(
        db_index=True,
        help_text="Área en hectáreas"
    )
    tc_horas = models.FloatField(
        help_text="Tiempo de concentración en horas"
    )
    nc_scs = models.IntegerField(
        blank=True,
        null=True,
        help_text="Número de curva SCS (30-100)"
    )

    # Ubicación
    latitude = models.FloatField(
        blank=True,
        null=True,
        help_text="Latitud (grados decimales)"
    )
    longitude = models.FloatField(
        blank=True,
        null=True,
        help_text="Longitud (grados decimales)"
    )
    elevation_m = models.FloatField(
        blank=True,
        null=True,
        help_text="Elevación en metros"
    )

    # Coeficiente de escorrentía
    c_racional = models.FloatField(
        blank=True,
        null=True,
        help_text="Coeficiente de escorrentía para Método Racional (0-1)"
    )

    # Metadata adicional (JSON)
    extra_metadata = models.JSONField(
        blank=True,
        null=True,
        help_text="Metadata adicional en formato JSON"
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
        verbose_name = "Cuenca"
        verbose_name_plural = "Cuencas"
        indexes = [
            models.Index(fields=['project', 'name']),
        ]

    def __str__(self):
        return f"{self.name} ({self.area_hectareas} ha)"

    @property
    def area_m2(self):
        """Área en metros cuadrados"""
        return self.area_hectareas * 10000

    @property
    def tc_minutes(self):
        """Tiempo de concentración en minutos"""
        return self.tc_horas * 60
