"""
Project Form - HidroStudio Professional
Formulario para crear y editar proyectos
"""

from django import forms
from projects.models import Project


class ProjectCreateForm(forms.ModelForm):
    """Formulario para crear un nuevo proyecto"""

    class Meta:
        model = Project
        fields = ['name', 'description', 'location', 'country', 'region']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Sistema de Drenaje Montevideo',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción del proyecto (opcional)',
                'rows': 3
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Montevideo, Uruguay',
                'required': True
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Uruguay',
                'value': 'Uruguay'
            }),
            'region': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Montevideo (opcional)'
            }),
        }
        labels = {
            'name': 'Nombre del Proyecto',
            'description': 'Descripción',
            'location': 'Ubicación',
            'country': 'País',
            'region': 'Región/Departamento',
        }
        help_texts = {
            'name': 'Nombre descriptivo para identificar el proyecto',
            'description': 'Información adicional sobre el proyecto',
            'location': 'Ubicación geográfica del proyecto',
            'country': 'País donde se encuentra el proyecto',
            'region': 'Región, departamento o provincia',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.owner = self.user
        instance.is_active = True
        if commit:
            instance.save()
        return instance
