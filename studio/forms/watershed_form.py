"""
Watershed Form - HidroStudio Professional
Formulario para crear y editar cuencas hidrográficas
"""

from django import forms
from watersheds.models import Watershed


class WatershedCreateForm(forms.ModelForm):
    """Formulario para crear una nueva cuenca"""

    class Meta:
        model = Watershed
        fields = [
            'name', 'description', 'area_hectareas', 'tc_horas',
            'c_racional', 'nc_scs', 'latitude', 'longitude', 'elevation_m'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Arroyo Miguelete Alto',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción de la cuenca (opcional)',
                'rows': 3
            }),
            'area_hectareas': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 250.5',
                'step': '0.01',
                'min': '0.01',
                'required': True
            }),
            'tc_horas': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 1.5',
                'step': '0.01',
                'min': '0.01',
                'required': True
            }),
            'c_racional': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 0.65 (0.0-1.0)',
                'step': '0.01',
                'min': '0.0',
                'max': '1.0'
            }),
            'nc_scs': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 80 (30-100)',
                'min': '30',
                'max': '100'
            }),
            'latitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: -34.9011 (grados decimales)',
                'step': '0.0001'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: -56.1645 (grados decimales)',
                'step': '0.0001'
            }),
            'elevation_m': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 25.5 (metros)',
                'step': '0.1'
            }),
        }
        labels = {
            'name': 'Nombre de la Cuenca',
            'description': 'Descripción',
            'area_hectareas': 'Área (hectáreas)',
            'tc_horas': 'Tiempo de Concentración (horas)',
            'c_racional': 'Coeficiente de Escorrentía (C) - Método Racional',
            'nc_scs': 'Número de Curva (NC) - Método SCS',
            'latitude': 'Latitud',
            'longitude': 'Longitud',
            'elevation_m': 'Elevación (metros)',
        }
        help_texts = {
            'name': 'Nombre descriptivo para identificar la cuenca',
            'description': 'Información adicional sobre la cuenca',
            'area_hectareas': 'Área de la cuenca en hectáreas',
            'tc_horas': 'Tiempo de concentración en horas (tiempo que tarda el agua en recorrer la cuenca)',
            'c_racional': 'Coeficiente de escorrentía (0.0-1.0). Valores típicos: Urbano=0.7-0.9, Rural=0.3-0.5',
            'nc_scs': 'Número de curva SCS (30-100). Valores típicos: Bosques=65-75, Pastos=70-85, Urbano=80-95',
            'latitude': 'Latitud en grados decimales (negativo para Sur)',
            'longitude': 'Longitud en grados decimales (negativo para Oeste)',
            'elevation_m': 'Elevación promedio de la cuenca sobre el nivel del mar',
        }

    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)

    def clean_area_hectareas(self):
        """Validar que el área sea positiva"""
        area = self.cleaned_data.get('area_hectareas')
        if area and area <= 0:
            raise forms.ValidationError('El área debe ser mayor a 0 hectáreas')
        return area

    def clean_tc_horas(self):
        """Validar que el tiempo de concentración sea positivo"""
        tc = self.cleaned_data.get('tc_horas')
        if tc and tc <= 0:
            raise forms.ValidationError('El tiempo de concentración debe ser mayor a 0 horas')
        return tc

    def clean_c_racional(self):
        """Validar que el coeficiente esté entre 0 y 1"""
        c = self.cleaned_data.get('c_racional')
        if c is not None and (c < 0 or c > 1):
            raise forms.ValidationError('El coeficiente de escorrentía debe estar entre 0.0 y 1.0')
        return c

    def clean_nc_scs(self):
        """Validar que el NC esté entre 30 y 100"""
        nc = self.cleaned_data.get('nc_scs')
        if nc is not None and (nc < 30 or nc > 100):
            raise forms.ValidationError('El número de curva debe estar entre 30 y 100')
        return nc

    def clean_latitude(self):
        """Validar que la latitud esté entre -90 y 90"""
        lat = self.cleaned_data.get('latitude')
        if lat is not None and (lat < -90 or lat > 90):
            raise forms.ValidationError('La latitud debe estar entre -90 y 90 grados')
        return lat

    def clean_longitude(self):
        """Validar que la longitud esté entre -180 y 180"""
        lon = self.cleaned_data.get('longitude')
        if lon is not None and (lon < -180 or lon > 180):
            raise forms.ValidationError('La longitud debe estar entre -180 y 180 grados')
        return lon

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.project:
            instance.project = self.project
        if commit:
            instance.save()
        return instance


class WatershedEditForm(WatershedCreateForm):
    """Formulario para editar una cuenca existente"""

    class Meta(WatershedCreateForm.Meta):
        fields = WatershedCreateForm.Meta.fields
