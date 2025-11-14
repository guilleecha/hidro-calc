"""
DesignStorm Forms - Tormentas de Diseño

Formularios para crear y editar tormentas de diseño.
"""

from django import forms
from hydrology.models import DesignStorm


class DesignStormCreateForm(forms.ModelForm):
    """Formulario para crear una nueva tormenta de diseño"""

    class Meta:
        model = DesignStorm
        fields = [
            'name',
            'description',
            'return_period_years',
            'duration_hours',
            'total_rainfall_mm',
            'distribution_type',
            'peak_position_ratio',
            'time_step_minutes',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Tormenta de diseño Tr=10 años',
                'maxlength': 255,
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción opcional de la tormenta',
            }),
            'return_period_years': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'step': 1,
                'placeholder': 'Ej: 10',
            }),
            'duration_hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0.1,
                'step': 0.1,
                'placeholder': 'Ej: 24.0',
            }),
            'total_rainfall_mm': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0.1,
                'step': 0.1,
                'placeholder': 'Ej: 127.0',
            }),
            'distribution_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'peak_position_ratio': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0.0,
                'max': 1.0,
                'step': 0.1,
                'placeholder': '0.5 (rango: 0.0-1.0)',
            }),
            'time_step_minutes': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'step': 1,
                'placeholder': 'Ej: 10',
            }),
        }
        labels = {
            'name': 'Nombre de la Tormenta',
            'description': 'Descripción',
            'return_period_years': 'Período de Retorno (años)',
            'duration_hours': 'Duración (horas)',
            'total_rainfall_mm': 'Lluvia Total (mm)',
            'distribution_type': 'Tipo de Distribución',
            'peak_position_ratio': 'Posición del Pico (0.0-1.0)',
            'time_step_minutes': 'Intervalo de Tiempo (minutos)',
        }
        help_texts = {
            'peak_position_ratio': '0.0=inicio, 0.5=centro, 1.0=final',
            'time_step_minutes': 'Paso temporal para cálculos (recomendado: 5-30 min)',
        }

    def __init__(self, watershed, *args, **kwargs):
        """Inicializar formulario con la cuenca"""
        super().__init__(*args, **kwargs)
        self.watershed = watershed
        self.fields['peak_position_ratio'].initial = 0.5

    def clean_return_period_years(self):
        """Validar período de retorno"""
        value = self.cleaned_data.get('return_period_years')
        if value and value < 1:
            raise forms.ValidationError('El período de retorno debe ser >= 1 año')
        return value

    def clean_duration_hours(self):
        """Validar duración"""
        value = self.cleaned_data.get('duration_hours')
        if value and value <= 0:
            raise forms.ValidationError('La duración debe ser > 0')
        return value

    def clean_total_rainfall_mm(self):
        """Validar lluvia total"""
        value = self.cleaned_data.get('total_rainfall_mm')
        if value and value <= 0:
            raise forms.ValidationError('La lluvia total debe ser > 0')
        return value

    def clean_peak_position_ratio(self):
        """Validar posición del pico"""
        value = self.cleaned_data.get('peak_position_ratio')
        if value is not None:
            if not (0.0 <= value <= 1.0):
                raise forms.ValidationError('La posición del pico debe estar entre 0.0 y 1.0')
        return value

    def clean_time_step_minutes(self):
        """Validar intervalo de tiempo"""
        value = self.cleaned_data.get('time_step_minutes')
        if value and value < 1:
            raise forms.ValidationError('El intervalo de tiempo debe ser >= 1 minuto')
        return value

    def save(self, commit=True):
        """Guardar tormenta asignando la cuenca"""
        instance = super().save(commit=False)
        instance.watershed = self.watershed
        if commit:
            instance.save()
        return instance


class DesignStormEditForm(forms.ModelForm):
    """Formulario para editar una tormenta de diseño existente"""

    class Meta:
        model = DesignStorm
        fields = [
            'name',
            'description',
            'return_period_years',
            'duration_hours',
            'total_rainfall_mm',
            'distribution_type',
            'peak_position_ratio',
            'time_step_minutes',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': 255,
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),
            'return_period_years': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'step': 1,
            }),
            'duration_hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0.1,
                'step': 0.1,
            }),
            'total_rainfall_mm': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0.1,
                'step': 0.1,
            }),
            'distribution_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'peak_position_ratio': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0.0,
                'max': 1.0,
                'step': 0.1,
            }),
            'time_step_minutes': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'step': 1,
            }),
        }
        labels = {
            'name': 'Nombre de la Tormenta',
            'description': 'Descripción',
            'return_period_years': 'Período de Retorno (años)',
            'duration_hours': 'Duración (horas)',
            'total_rainfall_mm': 'Lluvia Total (mm)',
            'distribution_type': 'Tipo de Distribución',
            'peak_position_ratio': 'Posición del Pico (0.0-1.0)',
            'time_step_minutes': 'Intervalo de Tiempo (minutos)',
        }
        help_texts = {
            'peak_position_ratio': '0.0=inicio, 0.5=centro, 1.0=final',
            'time_step_minutes': 'Paso temporal para cálculos (recomendado: 5-30 min)',
        }

    def clean_return_period_years(self):
        """Validar período de retorno"""
        value = self.cleaned_data.get('return_period_years')
        if value and value < 1:
            raise forms.ValidationError('El período de retorno debe ser >= 1 año')
        return value

    def clean_duration_hours(self):
        """Validar duración"""
        value = self.cleaned_data.get('duration_hours')
        if value and value <= 0:
            raise forms.ValidationError('La duración debe ser > 0')
        return value

    def clean_total_rainfall_mm(self):
        """Validar lluvia total"""
        value = self.cleaned_data.get('total_rainfall_mm')
        if value and value <= 0:
            raise forms.ValidationError('La lluvia total debe ser > 0')
        return value

    def clean_peak_position_ratio(self):
        """Validar posición del pico"""
        value = self.cleaned_data.get('peak_position_ratio')
        if value is not None:
            if not (0.0 <= value <= 1.0):
                raise forms.ValidationError('La posición del pico debe estar entre 0.0 y 1.0')
        return value

    def clean_time_step_minutes(self):
        """Validar intervalo de tiempo"""
        value = self.cleaned_data.get('time_step_minutes')
        if value and value < 1:
            raise forms.ValidationError('El intervalo de tiempo debe ser >= 1 minuto')
        return value
