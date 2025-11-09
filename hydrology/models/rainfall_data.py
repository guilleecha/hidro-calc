"""
RainfallData Model - Datos de Lluvia Observados
"""

from django.db import models
from watersheds.models import Watershed


class RainfallData(models.Model):
    """Modelo para datos de lluvia medidos (opcional)"""

    watershed = models.ForeignKey(
        Watershed,
        on_delete=models.CASCADE,
        related_name='rainfall_data',
        db_index=True,
        help_text="Cuenca donde se midió la lluvia"
    )

    event_date = models.DateField(
        db_index=True,
        help_text="Fecha del evento de lluvia"
    )
    return_period_years = models.IntegerField(
        blank=True,
        null=True,
        help_text="Período de retorno estimado (años)"
    )
    duration_hours = models.FloatField(
        blank=True,
        null=True,
        help_text="Duración del evento en horas"
    )
    total_rainfall_mm = models.FloatField(
        help_text="Lluvia total en mm"
    )

    # Serie de intensidades (JSON)
    # Array de: {time_min, intensity_mm_h, cumulative_mm}
    rainfall_series = models.JSONField(
        help_text="Serie temporal de lluvia: [{time_min, intensity_mm_h, cumulative_mm}, ...]"
    )

    source = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Fuente de datos (DNM, IMFIA, sensor local, etc.)"
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Notas sobre el evento"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha de registro"
    )

    class Meta:
        ordering = ['-event_date']
        verbose_name = "Datos de Lluvia"
        verbose_name_plural = "Datos de Lluvia"
        indexes = [
            models.Index(fields=['watershed', 'event_date']),
        ]

    def __str__(self):
        return f"Lluvia {self.event_date} - {self.total_rainfall_mm}mm"
