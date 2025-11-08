"""
Tests para los endpoints de la API.
"""

import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


class TestHealthEndpoint:
    """Tests para el endpoint de salud."""

    def test_health_check(self):
        """Test que el servidor responde correctamente."""
        response = client.get("/api/health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "healthy"
        assert "project" in data
        assert "version" in data


class TestRationalEndpoint:
    """Tests para el endpoint del Método Racional."""

    def test_rational_valid_input(self):
        """Test con entrada válida."""
        payload = {
            "C": 0.65,
            "I_mmh": 80.0,
            "A_ha": 5.0,
            "description": "Test cuenca"
        }

        response = client.post("/api/rational", json=payload)
        assert response.status_code == 200

        data = response.json()
        assert "Q_ls" in data
        assert "Q_m3s" in data
        assert "Q_m3h" in data
        assert data["Q_ls"] == pytest.approx(722.22, rel=0.01)

    def test_rational_without_description(self):
        """Test sin descripción (campo opcional)."""
        payload = {
            "C": 0.65,
            "I_mmh": 80.0,
            "A_ha": 5.0
        }

        response = client.post("/api/rational", json=payload)
        assert response.status_code == 200

    def test_rational_invalid_C_low(self):
        """Test con C inválido (< 0)."""
        payload = {
            "C": -0.1,
            "I_mmh": 80.0,
            "A_ha": 5.0
        }

        response = client.post("/api/rational", json=payload)
        assert response.status_code == 422  # Validation error

    def test_rational_invalid_C_high(self):
        """Test con C inválido (> 1)."""
        payload = {
            "C": 1.5,
            "I_mmh": 80.0,
            "A_ha": 5.0
        }

        response = client.post("/api/rational", json=payload)
        assert response.status_code == 422

    def test_rational_invalid_intensity(self):
        """Test con intensidad negativa."""
        payload = {
            "C": 0.65,
            "I_mmh": -80.0,
            "A_ha": 5.0
        }

        response = client.post("/api/rational", json=payload)
        assert response.status_code == 422

    def test_rational_invalid_area(self):
        """Test con área negativa."""
        payload = {
            "C": 0.65,
            "I_mmh": 80.0,
            "A_ha": -5.0
        }

        response = client.post("/api/rational", json=payload)
        assert response.status_code == 422

    def test_rational_missing_fields(self):
        """Test con campos faltantes."""
        payload = {
            "C": 0.65,
            "I_mmh": 80.0
            # Falta A_ha
        }

        response = client.post("/api/rational", json=payload)
        assert response.status_code == 422

    def test_rational_warnings(self):
        """Test que retorna advertencias cuando corresponde."""
        payload = {
            "C": 0.65,
            "I_mmh": 600.0,  # Intensidad muy alta
            "A_ha": 5.0
        }

        response = client.post("/api/rational", json=payload)
        assert response.status_code == 200

        data = response.json()
        assert "warnings" in data
        assert len(data["warnings"]) > 0


class TestWeightedCEndpoint:
    """Tests para el endpoint de coeficiente ponderado."""

    def test_weighted_c_valid(self):
        """Test con entrada válida."""
        payload = {
            "surfaces": [
                {"area_ha": 2.0, "C": 0.90, "description": "Techos"},
                {"area_ha": 3.0, "C": 0.85, "description": "Pavimento"},
                {"area_ha": 5.0, "C": 0.20, "description": "Césped"}
            ]
        }

        response = client.post("/api/weighted-c", json=payload)
        assert response.status_code == 200

        data = response.json()
        assert "C_weighted" in data
        assert "total_area_ha" in data
        assert "surfaces" in data

        assert data["C_weighted"] == pytest.approx(0.535, rel=0.01)
        assert data["total_area_ha"] == 10.0

        # Verificar porcentajes
        assert data["surfaces"][0]["percentage"] == 20.0
        assert data["surfaces"][1]["percentage"] == 30.0
        assert data["surfaces"][2]["percentage"] == 50.0

    def test_weighted_c_single_surface(self):
        """Test con una sola superficie."""
        payload = {
            "surfaces": [
                {"area_ha": 10.0, "C": 0.65}
            ]
        }

        response = client.post("/api/weighted-c", json=payload)
        assert response.status_code == 200

        data = response.json()
        assert data["C_weighted"] == 0.65

    def test_weighted_c_empty_surfaces(self):
        """Test con lista vacía."""
        payload = {
            "surfaces": []
        }

        response = client.post("/api/weighted-c", json=payload)
        assert response.status_code == 422

    def test_weighted_c_invalid_area(self):
        """Test con área inválida."""
        payload = {
            "surfaces": [
                {"area_ha": -2.0, "C": 0.90}
            ]
        }

        response = client.post("/api/weighted-c", json=payload)
        assert response.status_code == 422

    def test_weighted_c_invalid_coefficient(self):
        """Test con coeficiente inválido."""
        payload = {
            "surfaces": [
                {"area_ha": 2.0, "C": 1.5}
            ]
        }

        response = client.post("/api/weighted-c", json=payload)
        assert response.status_code == 422


class TestRunoffCoefficientsEndpoint:
    """Tests para el endpoint de coeficientes de referencia."""

    def test_get_coefficients(self):
        """Test obtener coeficientes de referencia."""
        response = client.get("/api/runoff-coefficients")
        assert response.status_code == 200

        data = response.json()
        assert "coefficients" in data
        assert "note" in data

        coefficients = data["coefficients"]
        assert "techos" in coefficients
        assert "pavimento_asfalto" in coefficients

        # Verificar estructura de un coeficiente
        techos = coefficients["techos"]
        assert "min" in techos
        assert "max" in techos
        assert "tipico" in techos
        assert "descripcion" in techos


class TestFrontendRoutes:
    """Tests para las rutas del frontend."""

    def test_index_page(self):
        """Test que la página principal carga."""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_rational_page(self):
        """Test que la página del método racional carga."""
        response = client.get("/rational")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
