"""
Hydrograph Model - Hidrograma
"""

from django.db import models
from .design_storm import DesignStorm


class Hydrograph(models.Model):
    """Modelo para hidrogramas calculados"""

    METHOD_CHOICES = [
        ('rational', 'Método Racional'),
        ('scs_unit_hydrograph', 'SCS Unit Hydrograph'),
        ('synth_unit_hydro', 'Synthetic Unit Hydrograph'),
    ]

    design_storm = models.ForeignKey(
        DesignStorm,
        on_delete=models.CASCADE,
        related_name='hydrographs',
        db_index=True,
        help_text="Tormenta de diseño utilizada"
    )

    # Identificación
    name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Nombre descriptivo del hidrograma"
    )

    # Método de cálculo
    method = models.CharField(
        max_length=50,
        choices=METHOD_CHOICES,
        db_index=True,
        help_text="Método de cálculo utilizado"
    )

    # Resultados resumen
    peak_discharge_m3s = models.FloatField(
        db_index=True,
        help_text="Caudal máximo en m³/s"
    )
    peak_discharge_lps = models.FloatField(
        blank=True,
        null=True,
        help_text="Caudal máximo en L/s"
    )
    time_to_peak_minutes = models.FloatField(
        blank=True,
        null=True,
        help_text="Tiempo al pico en minutos"
    )

    # Escorrentía
    total_runoff_mm = models.FloatField(
        blank=True,
        null=True,
        help_text="Escorrentía total en mm"
    )
    total_runoff_m3 = models.FloatField(
        blank=True,
        null=True,
        help_text="Escorrentía total en m³"
    )
    volume_hm3 = models.FloatField(
        blank=True,
        null=True,
        help_text="Volumen total en hm³"
    )

    # Serie temporal del hidrograma (JSON)
    # Array de: {time_min, discharge_m3s, cumulative_volume_m3}
    hydrograph_data = models.JSONField(
        help_text="Serie temporal del hidrograma: [{time_min, discharge_m3s, cumulative_volume_m3}, ...]"
    )

    # Metadata del cálculo
    rainfall_excess_mm = models.FloatField(
        blank=True,
        null=True,
        help_text="Lluvia en exceso (lluvia neta) en mm"
    )
    infiltration_total_mm = models.FloatField(
        blank=True,
        null=True,
        help_text="Infiltración total en mm"
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Notas adicionales sobre el cálculo"
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
        verbose_name = "Hidrograma"
        verbose_name_plural = "Hidrogramas"
        indexes = [
            models.Index(fields=['design_storm', 'method']),
        ]

    def __str__(self):
        return f"{self.name or 'Hidrograma'} - {self.method} (Q={self.peak_discharge_m3s:.2f} m³/s)"

    @property
    def peak_discharge_lps_calculated(self):
        """Caudal pico en L/s (calculado si no existe)"""
        if self.peak_discharge_lps:
            return self.peak_discharge_lps
        return self.peak_discharge_m3s * 1000

    @property
    def time_to_peak_hours(self):
        """Tiempo al pico en horas"""
        if self.time_to_peak_minutes:
            return self.time_to_peak_minutes / 60
        return None
