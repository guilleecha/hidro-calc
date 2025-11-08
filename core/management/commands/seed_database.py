"""
Management command para cargar datos de prueba en la base de datos
Equivalente a seed_db() de FastAPI

Uso: python manage.py seed_database
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Project, Watershed, DesignStorm, Hydrograph


class Command(BaseCommand):
    help = 'Carga datos de prueba en la base de datos de HidroCalc'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Eliminar todos los datos existentes antes de cargar',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Eliminando datos existentes...'))
            Hydrograph.objects.all().delete()
            DesignStorm.objects.all().delete()
            Watershed.objects.all().delete()
            Project.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Datos eliminados'))

        self.stdout.write(self.style.SUCCESS('Cargando datos de prueba...'))

        # Crear proyecto de ejemplo
        project = Project.objects.create(
            name="Sistema de Drenaje Montevideo",
            description="Análisis hidrológico del sistema de drenaje urbano de Montevideo",
            location="Montevideo, Uruguay",
            country="Uruguay",
            region="Montevideo",
            timezone="America/Montevideo",
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS(f'  Proyecto creado: {project.name}'))

        # Crear cuencas de ejemplo
        watersheds_data = [
            {
                'name': 'Arroyo Miguelete Alto',
                'description': 'Cuenca superior del Arroyo Miguelete',
                'area_hectareas': 250.0,
                'tc_horas': 1.8,
                'nc_scs': 72,
                'c_racional': 0.65,
                'latitude': -34.8667,
                'longitude': -56.1167,
                'elevation_m': 45.0
            },
            {
                'name': 'Arroyo Carrasco Medio',
                'description': 'Cuenca media del Arroyo Carrasco',
                'area_hectareas': 180.0,
                'tc_horas': 1.5,
                'nc_scs': 75,
                'c_racional': 0.70,
                'latitude': -34.8833,
                'longitude': -56.0500,
                'elevation_m': 38.0
            },
            {
                'name': 'Arroyo Pantanoso',
                'description': 'Cuenca del Arroyo Pantanoso',
                'area_hectareas': 320.0,
                'tc_horas': 2.1,
                'nc_scs': 68,
                'c_racional': 0.60,
                'latitude': -34.8500,
                'longitude': -56.1833,
                'elevation_m': 52.0
            }
        ]

        watersheds = []
        for ws_data in watersheds_data:
            watershed = Watershed.objects.create(project=project, **ws_data)
            watersheds.append(watershed)
            self.stdout.write(self.style.SUCCESS(f'  Cuenca creada: {watershed.name}'))

        # Crear tormentas de diseño de ejemplo
        storm_durations = [2, 6, 12, 24]  # horas
        return_period = 10  # años

        storms_created = 0
        for watershed in watersheds:
            for duration in storm_durations:
                # Cálculo simplificado de lluvia total usando IDF aproximado
                # P = a * Tr^b / (D + c)^d (fórmula genérica)
                # Valores aproximados para Uruguay
                a, b, c, d = 140, 0.25, 10, 0.8
                total_rainfall = a * (return_period ** b) / ((duration * 60 + c) ** d)

                storm = DesignStorm.objects.create(
                    watershed=watershed,
                    name=f"Tr={return_period}a, D={duration}h",
                    description=f"Tormenta de diseño para {watershed.name}",
                    return_period_years=return_period,
                    duration_hours=duration,
                    total_rainfall_mm=total_rainfall,
                    distribution_type='alternating_block',
                    time_step_minutes=5
                )
                storms_created += 1

        self.stdout.write(self.style.SUCCESS(f'  {storms_created} tormentas de diseño creadas'))

        # Estadísticas finales
        self.stdout.write(self.style.SUCCESS('\nEstadísticas de base de datos:'))
        self.stdout.write(f'  Proyectos: {Project.objects.count()}')
        self.stdout.write(f'  Cuencas: {Watershed.objects.count()}')
        self.stdout.write(f'  Tormentas de diseño: {DesignStorm.objects.count()}')
        self.stdout.write(f'  Hidrogramas: {Hydrograph.objects.count()}')

        self.stdout.write(self.style.SUCCESS('\nDatos de prueba cargados exitosamente'))
