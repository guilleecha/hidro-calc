"""
Tests para operaciones CRUD de DesignStorm en HidroStudio

Prueba los views, formularios y rutas para gestión de tormentas de diseño.
"""

import pytest
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from projects.models import Project
from watersheds.models import Watershed
from hydrology.models import DesignStorm


@pytest.mark.django_db
class TestDesignStormCreate:
    """Tests para creación de tormentas de diseño"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada test"""
        self.client = Client()

        # Crear usuario
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        # Crear proyecto
        self.project = Project.objects.create(
            name='Test Project',
            description='Test project for design storm CRUD',
            owner=self.user
        )

        # Crear cuenca
        self.watershed = Watershed.objects.create(
            name='Test Watershed',
            project=self.project,
            area_hectareas=520.0,
            tc_horas=0.75
        )

    def test_design_storm_create_page_requires_login(self):
        """Test que la página de creación requiere login"""
        url = reverse('studio:design_storm_create', args=[self.watershed.id])
        response = self.client.get(url)

        # Debe redirigir al login
        assert response.status_code == 302
        assert '/accounts/login/' in response.url

    def test_design_storm_create_page_loads(self):
        """Test que la página de creación carga correctamente"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('studio:design_storm_create', args=[self.watershed.id])
        response = self.client.get(url)

        assert response.status_code == 200
        assert 'form' in response.context
        assert response.context['watershed'] == self.watershed
        assert response.context['project'] == self.project

    def test_design_storm_create_valid_form(self):
        """Test crear tormenta con formulario válido"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('studio:design_storm_create', args=[self.watershed.id])

        data = {
            'name': 'Test Design Storm',
            'description': 'Test storm description',
            'return_period_years': 10,
            'duration_hours': 2.0,
            'total_rainfall_mm': 100.0,
            'distribution_type': 'alternating_block',
            'peak_position_ratio': 0.5,
            'time_step_minutes': 10,
        }

        response = self.client.post(url, data)

        # Debe redirigir al dashboard del proyecto
        assert response.status_code == 302
        assert reverse('studio:dashboard_project', args=[self.project.id]) in response.url

        # Verificar que se creó la tormenta
        storm = DesignStorm.objects.get(name='Test Design Storm')
        assert storm.watershed == self.watershed
        assert storm.total_rainfall_mm == 100.0
        assert storm.return_period_years == 10

    def test_design_storm_create_invalid_return_period(self):
        """Test validación de período de retorno negativo"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('studio:design_storm_create', args=[self.watershed.id])

        data = {
            'name': 'Test Design Storm',
            'description': 'Test storm',
            'return_period_years': -1,  # Inválido
            'duration_hours': 2.0,
            'total_rainfall_mm': 100.0,
            'distribution_type': 'alternating_block',
            'peak_position_ratio': 0.5,
            'time_step_minutes': 10,
        }

        response = self.client.post(url, data)

        # Debe volver a mostrar el formulario con error
        assert response.status_code == 200
        assert 'form' in response.context
        assert response.context['form'].errors

    def test_design_storm_create_invalid_peak_position(self):
        """Test validación de posición del pico fuera de rango"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('studio:design_storm_create', args=[self.watershed.id])

        data = {
            'name': 'Test Design Storm',
            'description': 'Test storm',
            'return_period_years': 10,
            'duration_hours': 2.0,
            'total_rainfall_mm': 100.0,
            'distribution_type': 'alternating_block',
            'peak_position_ratio': 1.5,  # Inválido (debe estar entre 0.0 y 1.0)
            'time_step_minutes': 10,
        }

        response = self.client.post(url, data)

        # Debe volver a mostrar el formulario con error
        assert response.status_code == 200
        assert 'form' in response.context
        assert response.context['form'].errors

    def test_design_storm_create_wrong_project_access(self):
        """Test que usuario no puede crear en proyecto que no es suyo"""
        # Crear otro usuario
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )

        # Crear otro proyecto
        other_project = Project.objects.create(
            name='Other Project',
            owner=other_user
        )

        # Crear cuenca en otro proyecto
        other_watershed = Watershed.objects.create(
            name='Other Watershed',
            project=other_project,
            area_hectareas=100.0,
            tc_horas=0.5
        )

        self.client.login(username='testuser', password='testpass123')
        url = reverse('studio:design_storm_create', args=[other_watershed.id])

        response = self.client.get(url)

        # Debe redirigir al index (sin permiso)
        assert response.status_code == 302
        assert reverse('studio:index') in response.url or 'studio' in response.url


@pytest.mark.django_db
class TestDesignStormEdit:
    """Tests para edición de tormentas de diseño"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada test"""
        self.client = Client()

        # Crear usuario
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        # Crear proyecto
        self.project = Project.objects.create(
            name='Test Project',
            owner=self.user
        )

        # Crear cuenca
        self.watershed = Watershed.objects.create(
            name='Test Watershed',
            project=self.project,
            area_hectareas=520.0,
            tc_horas=0.75
        )

        # Crear tormenta de diseño
        self.storm = DesignStorm.objects.create(
            watershed=self.watershed,
            name='Original Storm',
            description='Original description',
            total_rainfall_mm=80.0,
            duration_hours=1.5,
            return_period_years=5,
            peak_position_ratio=0.5,
            time_step_minutes=10
        )

    def test_design_storm_edit_page_loads(self):
        """Test que la página de edición carga correctamente"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('studio:design_storm_edit', args=[self.storm.id])
        response = self.client.get(url)

        assert response.status_code == 200
        assert 'form' in response.context
        assert response.context['design_storm'] == self.storm

    def test_design_storm_edit_update_fields(self):
        """Test actualizar campos de tormenta de diseño"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('studio:design_storm_edit', args=[self.storm.id])

        data = {
            'name': 'Updated Storm',
            'description': 'Updated description',
            'return_period_years': 25,
            'duration_hours': 3.0,
            'total_rainfall_mm': 150.0,
            'distribution_type': 'alternating_block',
            'peak_position_ratio': 0.4,
            'time_step_minutes': 15,
        }

        response = self.client.post(url, data)

        # Debe redirigir al dashboard del proyecto
        assert response.status_code == 302

        # Verificar que se actualizó la tormenta
        self.storm.refresh_from_db()
        assert self.storm.name == 'Updated Storm'
        assert self.storm.total_rainfall_mm == 150.0
        assert self.storm.return_period_years == 25

    def test_design_storm_edit_wrong_project_access(self):
        """Test que usuario no puede editar tormenta de otro proyecto"""
        # Crear otro usuario
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )

        self.client.login(username='otheruser', password='otherpass123')
        url = reverse('studio:design_storm_edit', args=[self.storm.id])

        response = self.client.get(url)

        # Debe redirigir al index (sin permiso)
        assert response.status_code == 302
        assert reverse('studio:index') in response.url or 'studio' in response.url


@pytest.mark.django_db
class TestDesignStormDelete:
    """Tests para eliminación de tormentas de diseño"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada test"""
        self.client = Client()

        # Crear usuario
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        # Crear proyecto
        self.project = Project.objects.create(
            name='Test Project',
            owner=self.user
        )

        # Crear cuenca
        self.watershed = Watershed.objects.create(
            name='Test Watershed',
            project=self.project,
            area_hectareas=520.0,
            tc_horas=0.75
        )

        # Crear tormenta de diseño
        self.storm = DesignStorm.objects.create(
            watershed=self.watershed,
            name='Test Storm',
            total_rainfall_mm=100.0,
            duration_hours=2.0,
            return_period_years=10
        )

    def test_design_storm_delete_page_loads(self):
        """Test que la página de eliminación carga correctamente"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('studio:design_storm_delete', args=[self.storm.id])
        response = self.client.get(url)

        assert response.status_code == 200
        assert 'design_storm' in response.context
        assert response.context['design_storm'] == self.storm

    def test_design_storm_delete_confirmation(self):
        """Test eliminar tormenta de diseño"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('studio:design_storm_delete', args=[self.storm.id])
        storm_id = self.storm.id

        response = self.client.post(url)

        # Debe redirigir al dashboard del proyecto
        assert response.status_code == 302

        # Verificar que se eliminó la tormenta
        assert not DesignStorm.objects.filter(id=storm_id).exists()

    def test_design_storm_delete_wrong_project_access(self):
        """Test que usuario no puede eliminar tormenta de otro proyecto"""
        # Crear otro usuario
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )

        self.client.login(username='otheruser', password='otherpass123')
        url = reverse('studio:design_storm_delete', args=[self.storm.id])

        response = self.client.get(url)

        # Debe redirigir al index (sin permiso)
        assert response.status_code == 302
        assert reverse('studio:index') in response.url or 'studio' in response.url

        # Verificar que la tormenta NO se eliminó
        assert DesignStorm.objects.filter(id=self.storm.id).exists()


@pytest.mark.django_db
class TestDesignStormWorkflow:
    """Tests de flujo completo de CRUD de tormentas de diseño"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada test"""
        self.client = Client()

        # Crear usuario
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        # Crear proyecto
        self.project = Project.objects.create(
            name='Test Project',
            owner=self.user
        )

        # Crear cuenca
        self.watershed = Watershed.objects.create(
            name='Test Watershed',
            project=self.project,
            area_hectareas=520.0,
            tc_horas=0.75
        )

    def test_complete_design_storm_workflow(self):
        """Test flujo completo: crear, editar, eliminar tormenta"""
        self.client.login(username='testuser', password='testpass123')

        # 1. Crear tormenta
        create_url = reverse('studio:design_storm_create', args=[self.watershed.id])
        create_data = {
            'name': 'Workflow Storm',
            'description': 'Testing workflow',
            'return_period_years': 10,
            'duration_hours': 2.0,
            'total_rainfall_mm': 100.0,
            'distribution_type': 'alternating_block',
            'peak_position_ratio': 0.5,
            'time_step_minutes': 10,
        }
        response = self.client.post(create_url, create_data)
        assert response.status_code == 302

        # Obtener la tormenta creada
        storm = DesignStorm.objects.get(name='Workflow Storm')
        assert storm.total_rainfall_mm == 100.0

        # 2. Editar tormenta
        edit_url = reverse('studio:design_storm_edit', args=[storm.id])
        edit_data = {
            'name': 'Updated Workflow Storm',
            'description': 'Updated testing workflow',
            'return_period_years': 25,
            'duration_hours': 3.0,
            'total_rainfall_mm': 120.0,
            'distribution_type': 'alternating_block',
            'peak_position_ratio': 0.6,
            'time_step_minutes': 15,
        }
        response = self.client.post(edit_url, edit_data)
        assert response.status_code == 302

        # Verificar actualización
        storm.refresh_from_db()
        assert storm.name == 'Updated Workflow Storm'
        assert storm.total_rainfall_mm == 120.0

        # 3. Eliminar tormenta
        delete_url = reverse('studio:design_storm_delete', args=[storm.id])
        storm_id = storm.id
        response = self.client.post(delete_url)
        assert response.status_code == 302

        # Verificar eliminación
        assert not DesignStorm.objects.filter(id=storm_id).exists()
