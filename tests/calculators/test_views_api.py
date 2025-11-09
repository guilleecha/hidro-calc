"""
Tests de integración para las vistas y APIs de calculadoras.
"""

import pytest
import json
from django.test import Client
from django.urls import reverse


@pytest.fixture
def client():
    """Cliente de test de Django."""
    return Client()


class TestRationalCalculatorView:
    """Tests para la vista HTML de Método Racional."""

    def test_view_loads(self, client):
        """Test que la vista carga correctamente."""
        response = client.get('/calculators/rational/')
        assert response.status_code == 200

    def test_view_contains_title(self, client):
        """Test que contiene el título esperado."""
        response = client.get('/calculators/rational/')
        assert 'Método Racional' in response.content.decode()

    def test_view_contains_form(self, client):
        """Test que contiene el formulario."""
        response = client.get('/calculators/rational/')
        content = response.content.decode()
        assert 'rationalForm' in content
        assert 'calculateBtn' in content

    def test_view_uses_correct_template(self, client):
        """Test que usa el template correcto."""
        response = client.get('/calculators/rational/')
        assert 'calculators/rational.html' in [t.name for t in response.templates]


class TestIDFCalculatorView:
    """Tests para la vista HTML de Curvas IDF."""

    def test_view_loads(self, client):
        """Test que la vista carga correctamente."""
        response = client.get('/calculators/idf/')
        assert response.status_code == 200

    def test_view_contains_title(self, client):
        """Test que contiene el título esperado."""
        response = client.get('/calculators/idf/')
        assert 'IDF' in response.content.decode()

    def test_view_uses_correct_template(self, client):
        """Test que usa el template correcto."""
        response = client.get('/calculators/idf/')
        assert 'calculators/idf.html' in [t.name for t in response.templates]


class TestRationalCalculateAPI:
    """Tests para la API de cálculo de Método Racional."""

    def test_api_basic_calculation(self, client):
        """Test de cálculo básico."""
        data = {
            "C": 0.65,
            "I_mmh": 80,
            "A_ha": 5
        }
        response = client.post(
            '/calculators/api/rational/calculate',
            data=json.dumps(data),
            content_type='application/json'
        )

        assert response.status_code == 200
        result = json.loads(response.content)

        assert 'Q_ls' in result
        assert 'Q_m3s' in result
        assert 'Q_m3h' in result
        assert result['Q_ls'] == 722.28

    def test_api_with_description(self, client):
        """Test con descripción."""
        data = {
            "C": 0.65,
            "I_mmh": 80,
            "A_ha": 5,
            "description": "Test cuenca"
        }
        response = client.post(
            '/calculators/api/rational/calculate',
            data=json.dumps(data),
            content_type='application/json'
        )

        assert response.status_code == 200
        result = json.loads(response.content)
        assert result['description'] == "Test cuenca"

    def test_api_with_warnings(self, client):
        """Test que genera warnings."""
        data = {
            "C": 0.65,
            "I_mmh": 600,  # Muy alta - genera warning
            "A_ha": 5
        }
        response = client.post(
            '/calculators/api/rational/calculate',
            data=json.dumps(data),
            content_type='application/json'
        )

        assert response.status_code == 200
        result = json.loads(response.content)
        assert len(result['warnings']) > 0

    def test_api_invalid_coefficient(self, client):
        """Test con coeficiente inválido."""
        data = {
            "C": 1.5,  # > 1
            "I_mmh": 80,
            "A_ha": 5
        }
        response = client.post(
            '/calculators/api/rational/calculate',
            data=json.dumps(data),
            content_type='application/json'
        )

        assert response.status_code == 400
        result = json.loads(response.content)
        assert 'error' in result

    def test_api_negative_intensity(self, client):
        """Test con intensidad negativa."""
        data = {
            "C": 0.65,
            "I_mmh": -10,
            "A_ha": 5
        }
        response = client.post(
            '/calculators/api/rational/calculate',
            data=json.dumps(data),
            content_type='application/json'
        )

        assert response.status_code == 400
        result = json.loads(response.content)
        assert 'error' in result

    def test_api_zero_area(self, client):
        """Test con área cero."""
        data = {
            "C": 0.65,
            "I_mmh": 80,
            "A_ha": 0
        }
        response = client.post(
            '/calculators/api/rational/calculate',
            data=json.dumps(data),
            content_type='application/json'
        )

        assert response.status_code == 400
        result = json.loads(response.content)
        assert 'error' in result

    def test_api_missing_parameters(self, client):
        """Test con parámetros faltantes."""
        data = {
            "C": 0.65,
            "I_mmh": 80
            # Falta A_ha
        }
        response = client.post(
            '/calculators/api/rational/calculate',
            data=json.dumps(data),
            content_type='application/json'
        )

        assert response.status_code in [400, 500]


class TestRationalWeightedCAPI:
    """Tests para la API de coeficiente ponderado."""

    def test_api_multiple_surfaces(self, client):
        """Test con múltiples superficies."""
        data = {
            "surfaces": [
                {"area_ha": 2, "C": 0.90, "description": "Techos"},
                {"area_ha": 3, "C": 0.85, "description": "Pavimento"},
                {"area_ha": 5, "C": 0.20, "description": "Césped"}
            ]
        }
        response = client.post(
            '/calculators/api/rational/weighted-c',
            data=json.dumps(data),
            content_type='application/json'
        )

        assert response.status_code == 200
        result = json.loads(response.content)

        assert 'C_weighted' in result
        assert 'total_area_ha' in result
        assert 'surfaces' in result
        assert result['C_weighted'] == 0.535
        assert result['total_area_ha'] == 10.0

    def test_api_single_surface(self, client):
        """Test con una sola superficie."""
        data = {
            "surfaces": [
                {"area_ha": 10, "C": 0.5, "description": "Mixto"}
            ]
        }
        response = client.post(
            '/calculators/api/rational/weighted-c',
            data=json.dumps(data),
            content_type='application/json'
        )

        assert response.status_code == 200
        result = json.loads(response.content)
        assert result['C_weighted'] == 0.5

    def test_api_empty_surfaces(self, client):
        """Test con lista vacía (debe fallar)."""
        data = {
            "surfaces": []
        }
        response = client.post(
            '/calculators/api/rational/weighted-c',
            data=json.dumps(data),
            content_type='application/json'
        )

        assert response.status_code == 400
        result = json.loads(response.content)
        assert 'error' in result

    def test_api_percentages_calculated(self, client):
        """Test que calcula porcentajes."""
        data = {
            "surfaces": [
                {"area_ha": 7, "C": 0.9, "description": "Impermeable"},
                {"area_ha": 3, "C": 0.1, "description": "Permeable"}
            ]
        }
        response = client.post(
            '/calculators/api/rational/weighted-c',
            data=json.dumps(data),
            content_type='application/json'
        )

        assert response.status_code == 200
        result = json.loads(response.content)

        assert len(result['surfaces']) == 2
        assert result['surfaces'][0]['percentage'] == 70.0
        assert result['surfaces'][1]['percentage'] == 30.0


class TestIDFCalculateAPI:
    """Tests para la API de cálculo de Curvas IDF."""

    def test_api_basic_calculation(self, client):
        """Test de cálculo básico."""
        data = {
            "P3_10": 75,
            "Tr": 5,
            "d": 1
        }
        response = client.post(
            '/calculators/api/idf/calculate',
            data=json.dumps(data),
            content_type='application/json'
        )

        assert response.status_code == 200
        result = json.loads(response.content)

        assert 'I_mmh' in result
        assert 'P_mm' in result
        assert 'CT' in result
        assert 'CD' in result
        assert 'CA' in result
        assert 'warnings' in result

    def test_api_with_area_correction(self, client):
        """Test con corrección por área."""
        data = {
            "P3_10": 74,
            "Tr": 5,
            "d": 1,
            "Ac": 30
        }
        response = client.post(
            '/calculators/api/idf/calculate',
            data=json.dumps(data),
            content_type='application/json'
        )

        assert response.status_code == 200
        result = json.loads(response.content)

        # Verificar que CA < 1 (hay corrección)
        assert result['CA'] < 1.0
        assert result['Ac_km2'] == 30.0

    def test_api_without_area_correction(self, client):
        """Test sin corrección por área."""
        data = {
            "P3_10": 75,
            "Tr": 5,
            "d": 1
        }
        response = client.post(
            '/calculators/api/idf/calculate',
            data=json.dumps(data),
            content_type='application/json'
        )

        assert response.status_code == 200
        result = json.loads(response.content)

        # Sin corrección, CA = 1.0
        assert result['CA'] == 1.0
        assert result['Ac_km2'] is None

    def test_api_invalid_p3_10_low(self, client):
        """Test con P3_10 fuera de rango inferior."""
        data = {
            "P3_10": 40,
            "Tr": 5,
            "d": 1
        }
        response = client.post(
            '/calculators/api/idf/calculate',
            data=json.dumps(data),
            content_type='application/json'
        )

        assert response.status_code == 400
        result = json.loads(response.content)
        assert 'error' in result

    def test_api_invalid_tr(self, client):
        """Test con Tr < 2."""
        data = {
            "P3_10": 75,
            "Tr": 1,
            "d": 1
        }
        response = client.post(
            '/calculators/api/idf/calculate',
            data=json.dumps(data),
            content_type='application/json'
        )

        assert response.status_code == 400
        result = json.loads(response.content)
        assert 'error' in result

    def test_api_with_warnings(self, client):
        """Test que genera warnings."""
        data = {
            "P3_10": 95,   # Alto - genera warning
            "Tr": 150,     # Muy alto - genera warning
            "d": 30,       # Larga - genera warning
            "Ac": 350      # Grande - genera warning
        }
        response = client.post(
            '/calculators/api/idf/calculate',
            data=json.dumps(data),
            content_type='application/json'
        )

        assert response.status_code == 200
        result = json.loads(response.content)
        assert len(result['warnings']) >= 4


class TestRunoffCoefficientsAPI:
    """Tests para la API de coeficientes de escorrentía."""

    def test_api_returns_coefficients(self, client):
        """Test que retorna coeficientes."""
        response = client.get('/calculators/api/runoff-coefficients')

        assert response.status_code == 200
        result = json.loads(response.content)

        assert isinstance(result, dict)
        assert len(result) > 0

    def test_api_has_expected_surfaces(self, client):
        """Test que tiene superficies esperadas."""
        response = client.get('/calculators/api/runoff-coefficients')
        result = json.loads(response.content)

        expected = ['techos', 'pavimento_asfalto', 'cesped_plano_2pct', 'comercial']
        for surface in expected:
            assert surface in result

    def test_api_coefficient_structure(self, client):
        """Test de estructura de cada coeficiente."""
        response = client.get('/calculators/api/runoff-coefficients')
        result = json.loads(response.content)

        for key, data in result.items():
            assert 'min' in data
            assert 'max' in data
            assert 'tipico' in data
            assert 'descripcion' in data


class TestP310ValuesAPI:
    """Tests para la API de valores P3_10."""

    def test_api_returns_values(self, client):
        """Test que retorna valores."""
        response = client.get('/calculators/api/p3-10-values')

        assert response.status_code == 200
        result = json.loads(response.content)

        assert isinstance(result, dict)
        assert len(result) > 0

    def test_api_has_montevideo(self, client):
        """Test que incluye Montevideo."""
        response = client.get('/calculators/api/p3-10-values')
        result = json.loads(response.content)

        assert 'Montevideo' in result
        assert result['Montevideo'] == 75.0

    def test_api_has_major_cities(self, client):
        """Test que incluye ciudades principales."""
        response = client.get('/calculators/api/p3-10-values')
        result = json.loads(response.content)

        expected_cities = ['Montevideo', 'Salto', 'Paysandú', 'Rivera']
        for city in expected_cities:
            assert city in result

    def test_api_values_in_range(self, client):
        """Test que todos los valores están en rango válido."""
        response = client.get('/calculators/api/p3-10-values')
        result = json.loads(response.content)

        for city, value in result.items():
            assert 50 <= value <= 100, f"{city}: {value} fuera de rango"
