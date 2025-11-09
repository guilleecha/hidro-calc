"""
DesignStorm Model - Tormenta de Diseño
"""

from django.db import models
from watersheds.models import Watershed


class DesignStorm(models.Model):
    """Modelo para tormentas de diseño parametrizadas"""

    DISTRIBUTION_CHOICES = [
        ('alternating_block', 'Alternating Block'),
        ('chicago', 'Chicago'),
        ('sidle', 'Sidle'),
        ('custom', 'Custom'),
    ]

    watershed = models.ForeignKey(
        Watershed,
        on_delete=models.CASCADE,
        related_name='design_storms',
        db_index=True,
        help_text="Cuenca a la que pertenece la tormenta"
    )

    name = models.CharField(
        max_length=255,
        help_text="Nombre de la tormenta"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Descripción de la tormenta"
    )

    # Parámetros básicos
    return_period_years = models.IntegerField(
        db_index=True,
        help_text="Período de retorno (Tr) en años"
    )
    duration_hours = models.FloatField(
        db_index=True,
        help_text="Duración de la tormenta en horas"
    )

    # Lluvia total
    total_rainfall_mm = models.FloatField(
        help_text="Lluvia total en milímetros"
    )

    # Método de distribución
    distribution_type = models.CharField(
        max_length=50,
        choices=DISTRIBUTION_CHOICES,
        default='alternating_block',
        help_text="Tipo de distribución temporal de la lluvia"
    )

    # Parámetros SCS
    initial_abstraction_mm = models.FloatField(
        blank=True,
        null=True,
        help_text="Abstracción inicial (Ia) en mm, típicamente 0.2*S"
    )
    storage_parameter_mm = models.FloatField(
        blank=True,
        null=True,
        help_text="Parámetro de almacenamiento (S) en mm, calculado como (25400/NC - 254)"
    )

    # Intervalo de tiempo
    time_step_minutes = models.IntegerField(
        default=5,
        help_text="Intervalo de tiempo en minutos"
    )

    # Metadata
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
        verbose_name = "Tormenta de Diseño"
        verbose_name_plural = "Tormentas de Diseño"
        indexes = [
            models.Index(fields=['watershed', 'return_period_years']),
        ]

    def __str__(self):
        return f"{self.name} (Tr={self.return_period_years}a, D={self.duration_hours}h)"

    @property
    def duration_minutes(self):
        """Duración en minutos"""
        return self.duration_hours * 60

    @property
    def average_intensity_mm_h(self):
        """Intensidad promedio en mm/h"""
        return self.total_rainfall_mm / self.duration_hours
