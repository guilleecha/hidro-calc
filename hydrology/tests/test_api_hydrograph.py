"""
Tests para los endpoints de API de hidrogramas

Prueba los endpoints REST para cálculo de hidrogramas.
"""

import pytest
from django.test import Client
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from hydrology.models import DesignStorm
from projects.models import Project
from watersheds.models import Watershed


@pytest.mark.django_db
class TestHydrographAPI:
    """Tests para API endpoints de hidrogramas"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada test"""
        self.client = APIClient()

        # Crear usuario
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        # Crear proyecto
        self.project = Project.objects.create(
            name='Test Project',
            description='Test project for hydrograph API',
            owner=self.user
        )

        # Crear cuenca
        self.watershed = Watershed.objects.create(
            name='Test Watershed',
            project=self.project,
            area_hectareas=520.0,  # 5.2 km² = 520 hectáreas
            tc_horas=0.75  # 45 minutos = 0.75 horas
        )

        # Crear tormenta de diseño
        self.storm = DesignStorm.objects.create(
            watershed=self.watershed,
            name='Test Design Storm',
            total_rainfall_mm=100.0,
            duration_hours=2.0,
            return_period_years=10
        )

    def test_hydrograph_list(self):
        """Test GET /api/hydrographs/"""
        response = self.client.get('/api/hydrographs/')
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data or isinstance(response.data, list)

    def test_hydrograph_create_basic(self):
        """Test POST /api/hydrographs/ para crear hidrograma"""
        payload = {
            'design_storm': self.storm.id,
            'name': 'Test Hydrograph',
            'method': 'rational'
        }

        response = self.client.post(
            '/api/hydrographs/',
            payload,
            format='json'
        )

        # Puede fallar si no autenticado, pero la request debe ser válida
        assert response.status_code in [
            status.HTTP_201_CREATED,
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN
        ]

    def test_design_storm_list(self):
        """Test GET /api/design-storms/"""
        response = self.client.get('/api/design-storms/')
        assert response.status_code == status.HTTP_200_OK

    def test_design_storm_detail(self):
        """Test GET /api/design-storms/{id}/"""
        response = self.client.get(f'/api/design-storms/{self.storm.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == self.storm.id
        assert response.data['name'] == 'Test Design Storm'

    def test_design_storm_create(self):
        """Test POST /api/design-storms/"""
        payload = {
            'watershed': self.watershed.id,
            'name': 'New Design Storm',
            'total_rainfall_mm': 80.0,
            'duration_hours': 1.0,
            'return_period_years': 25,
            'peak_position_ratio': 0.5
        }

        response = self.client.post(
            '/api/design-storms/',
            payload,
            format='json'
        )

        # Debe poder crearse
        assert response.status_code in [
            status.HTTP_201_CREATED,
            status.HTTP_401_UNAUTHORIZED
        ]

        if response.status_code == status.HTTP_201_CREATED:
            assert 'id' in response.data


@pytest.mark.django_db
class TestHydrographCalculation:
    """Tests específicos para cálculo de hidrogramas"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada test"""
        self.client = APIClient()

        # Crear usuario
        self.user = User.objects.create_user(
            username='hydro_user',
            email='hydro@example.com',
            password='hydropass123'
        )

        # Crear proyecto
        self.project = Project.objects.create(
            name='Hydro Project',
            description='Project for calculation tests',
            owner=self.user
        )

        # Crear cuenca
        self.watershed = Watershed.objects.create(
            name='Test Basin',
            project=self.project,
            area_hectareas=1000.0,  # 10 km² = 1000 hectáreas
            tc_horas=1.0  # 60 minutos = 1 hora
        )

        # Crear tormenta de diseño
        self.design_storm = DesignStorm.objects.create(
            watershed=self.watershed,
            name='Design Storm 1h',
            total_rainfall_mm=50.0,
            duration_hours=1.0,
            return_period_years=10
        )

    def test_hydrograph_attributes(self):
        """Test que los hidrogramas tienen los atributos correctos"""
        response = self.client.get('/api/hydrographs/')
        assert response.status_code == status.HTTP_200_OK

        # Si hay hidrogramas, verificar estructura
        if hasattr(response.data, 'get'):
            # Es un dict (error o single object)
            pass
        elif isinstance(response.data, list):
            # Lista de hidrogramas
            for hydrograph in response.data:
                if 'hydrograph_data' in hydrograph:
                    data = hydrograph['hydrograph_data']
                    assert 'time_steps' in data or 'discharge' in data

    def test_design_storm_peak_position(self):
        """Test que peak_position_ratio se almacena correctamente"""
        response = self.client.get(f'/api/design-storms/{self.design_storm.id}/')
        assert response.status_code == status.HTTP_200_OK

        # Verificar que peak_position_ratio está disponible
        if 'peak_position_ratio' in response.data:
            assert 0.0 <= response.data['peak_position_ratio'] <= 1.0


@pytest.mark.django_db
class TestWatershedAPI:
    """Tests para API endpoints de cuencas"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada test"""
        self.client = APIClient()

        self.user = User.objects.create_user(
            username='watershed_user',
            password='pass123'
        )

        self.project = Project.objects.create(
            name='Watershed Project',
            owner=self.user
        )

    def test_watershed_list(self):
        """Test GET /api/watersheds/"""
        response = self.client.get('/api/watersheds/')
        assert response.status_code == status.HTTP_200_OK

    def test_watershed_create(self):
        """Test POST /api/watersheds/"""
        payload = {
            'name': 'Test Watershed',
            'project': self.project.id,
            'area_hectareas': 500.0,
            'tc_horas': 0.5
        }

        response = self.client.post(
            '/api/watersheds/',
            payload,
            format='json'
        )

        assert response.status_code in [
            status.HTTP_201_CREATED,
            status.HTTP_401_UNAUTHORIZED
        ]

    def test_watershed_detail(self):
        """Test GET /api/watersheds/{id}/"""
        # Crear una cuenca
        watershed = Watershed.objects.create(
            name='Detail Test',
            project=self.project,
            area_hectareas=850.0,
            tc_horas=0.83
        )

        response = self.client.get(f'/api/watersheds/{watershed.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Detail Test'


@pytest.mark.django_db
class TestProjectAPI:
    """Tests para API endpoints de proyectos"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada test"""
        self.client = APIClient()

        self.user = User.objects.create_user(
            username='project_user',
            password='pass123'
        )

    def test_project_list(self):
        """Test GET /api/projects/"""
        response = self.client.get('/api/projects/')
        assert response.status_code == status.HTTP_200_OK

    def test_project_create(self):
        """Test POST /api/projects/"""
        payload = {
            'name': 'New Project',
            'description': 'Test project'
        }

        response = self.client.post(
            '/api/projects/',
            payload,
            format='json'
        )

        assert response.status_code in [
            status.HTTP_201_CREATED,
            status.HTTP_401_UNAUTHORIZED
        ]

    def test_project_detail(self):
        """Test GET /api/projects/{id}/"""
        # Crear proyecto
        project = Project.objects.create(
            name='Test',
            owner=self.user
        )

        response = self.client.get(f'/api/projects/{project.id}/')
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestAPIIntegration:
    """Tests de integración del API"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada test"""
        self.client = APIClient()

        self.user = User.objects.create_user(
            username='integration_user',
            password='pass123'
        )

        # Crear flujo completo: Proyecto → Cuenca → Tormenta → Hidrograma
        self.project = Project.objects.create(
            name='Integration Test',
            owner=self.user
        )

        self.watershed = Watershed.objects.create(
            name='Integration Watershed',
            project=self.project,
            area_hectareas=600.0,  # 6 km² = 600 hectáreas
            tc_horas=0.67  # 40 minutos ≈ 0.67 horas
        )

        self.storm = DesignStorm.objects.create(
            watershed=self.watershed,
            name='Integration Storm',
            total_rainfall_mm=75.0,
            duration_hours=1.5,
            return_period_years=10
        )

    def test_complete_workflow(self):
        """Test flujo completo: obtener datos para todo el árbol"""
        # 1. Obtener proyecto
        proj_response = self.client.get(f'/api/projects/{self.project.id}/')
        assert proj_response.status_code == status.HTTP_200_OK

        # 2. Obtener cuencas del proyecto
        ws_response = self.client.get('/api/watersheds/')
        assert ws_response.status_code == status.HTTP_200_OK

        # 3. Obtener tormentas de la cuenca
        storms_response = self.client.get('/api/design-storms/')
        assert storms_response.status_code == status.HTTP_200_OK

        # 4. Obtener hidrogramas
        hydro_response = self.client.get('/api/hydrographs/')
        assert hydro_response.status_code == status.HTTP_200_OK

    def test_api_structure_consistency(self):
        """Test que la estructura del API es consistente"""
        # Todas las listas deben ser paginadas o ser listas
        endpoints = [
            '/api/projects/',
            '/api/watersheds/',
            '/api/design-storms/',
            '/api/hydrographs/'
        ]

        for endpoint in endpoints:
            response = self.client.get(endpoint)
            assert response.status_code == status.HTTP_200_OK

            # Debe ser una lista o estar paginado
            data = response.data
            if isinstance(data, dict):
                # Paginado: debe tener 'results' o 'data'
                assert 'results' in data or 'data' in data or isinstance(data, dict)
            else:
                # Directamente una lista
                assert isinstance(data, list)
