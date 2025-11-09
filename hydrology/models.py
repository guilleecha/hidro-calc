"""
Hydrology Models - Modelos hidrológicos

Contiene los modelos para análisis hidrológico:
- DesignStorm: Tormentas de diseño
- Hydrograph: Hidrogramas calculados
- RainfallData: Datos de lluvia observados
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
