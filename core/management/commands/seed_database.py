"""
Management command para cargar datos de prueba en la base de datos
Equivalente a seed_db() de FastAPI

Uso: python manage.py seed_database
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Project, Watershed, DesignStorm, Hydrograph
from calculators.services.idf import calculate_intensity_idf


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

        # Crear tormentas de diseño de ejemplo usando curvas IDF reales de Uruguay
        storm_configs = [
            {'duration': 1, 'return_periods': [5, 10, 25]},
            {'duration': 2, 'return_periods': [5, 10, 25]},
            {'duration': 6, 'return_periods': [10, 25, 50]},
            {'duration': 12, 'return_periods': [10, 25, 50]},
            {'duration': 24, 'return_periods': [10, 25, 50]},
        ]

        # Parámetro P3_10 típico para Montevideo (mm)
        P3_10_montevideo = 70  # Valor típico de la zona costera de Uruguay

        storms_created = 0
        for watershed in watersheds:
            # Convertir área de hectáreas a km²
            area_km2 = watershed.area_hectareas / 100.0

            for config in storm_configs:
                duration = config['duration']

                for return_period in config['return_periods']:
                    # Calcular intensidad y precipitación usando curvas IDF reales
                    result = calculate_intensity_idf(
                        P3_10=P3_10_montevideo,
                        Tr=return_period,
                        d=duration,
                        Ac=area_km2
                    )

                    total_rainfall = result['P_mm']

                    storm = DesignStorm.objects.create(
                        watershed=watershed,
                        name=f"Tr={return_period}a, D={duration}h",
                        description=f"Tormenta de diseño para {watershed.name} (IDF Uruguay)",
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
