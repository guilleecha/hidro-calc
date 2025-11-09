"""
Tests unitarios para el servicio de Método Racional.
"""

import pytest
from calculators.services.rational import (
    calculate_rational_flow,
    calculate_rational_flow_detailed,
    calculate_weighted_C,
    get_runoff_coefficients
)


class TestCalculateRationalFlow:
    """Tests para la función calculate_rational_flow."""

    def test_basic_calculation(self):
        """Test de cálculo básico con valores típicos."""
        Q = calculate_rational_flow(C=0.65, I_mmh=80, A_ha=5)
        # Q = 0.65 * 80 * 5 * 2.778 = 722.28 L/s
        assert round(Q, 2) == 722.28

    def test_calculation_with_integers(self):
        """Test con valores enteros."""
        Q = calculate_rational_flow(C=0.7, I_mmh=100, A_ha=10)
        # Q = 0.7 * 100 * 10 * 2.778 = 1944.6 L/s
        assert round(Q, 1) == 1944.6

    def test_small_area(self):
        """Test con área pequeña (1 ha)."""
        Q = calculate_rational_flow(C=0.8, I_mmh=50, A_ha=1)
        # Q = 0.8 * 50 * 1 * 2.778 = 111.12 L/s
        assert round(Q, 2) == 111.12

    def test_zero_coefficient(self):
        """Test con C=0 (sin escorrentía)."""
        Q = calculate_rational_flow(C=0, I_mmh=100, A_ha=10)
        assert Q == 0

    def test_maximum_coefficient(self):
        """Test con C=1 (100% escorrentía)."""
        Q = calculate_rational_flow(C=1.0, I_mmh=100, A_ha=10)
        # Q = 1.0 * 100 * 10 * 2.778 = 2778 L/s
        assert round(Q, 0) == 2778

    def test_invalid_coefficient_negative(self):
        """Test con C negativo (debe fallar)."""
        with pytest.raises(ValueError, match="entre 0 y 1"):
            calculate_rational_flow(C=-0.1, I_mmh=80, A_ha=5)

    def test_invalid_coefficient_too_high(self):
        """Test con C > 1 (debe fallar)."""
        with pytest.raises(ValueError, match="entre 0 y 1"):
            calculate_rational_flow(C=1.5, I_mmh=80, A_ha=5)

    def test_invalid_intensity_negative(self):
        """Test con intensidad negativa (debe fallar)."""
        with pytest.raises(ValueError, match="no puede ser negativa"):
            calculate_rational_flow(C=0.65, I_mmh=-10, A_ha=5)

    def test_invalid_area_zero(self):
        """Test con área cero (debe fallar)."""
        with pytest.raises(ValueError, match="debe ser positiva"):
            calculate_rational_flow(C=0.65, I_mmh=80, A_ha=0)

    def test_invalid_area_negative(self):
        """Test con área negativa (debe fallar)."""
        with pytest.raises(ValueError, match="debe ser positiva"):
            calculate_rational_flow(C=0.65, I_mmh=80, A_ha=-5)

    def test_warning_high_intensity(self):
        """Test que genera warning por intensidad muy alta."""
        with pytest.warns(UserWarning, match="Intensidad muy alta"):
            calculate_rational_flow(C=0.65, I_mmh=600, A_ha=5)

    def test_warning_large_area(self):
        """Test que genera warning por área grande."""
        with pytest.warns(UserWarning, match="Área grande"):
            calculate_rational_flow(C=0.65, I_mmh=80, A_ha=250)

    def test_warning_low_coefficient(self):
        """Test que genera warning por coeficiente muy bajo."""
        with pytest.warns(UserWarning, match="muy bajo"):
            calculate_rational_flow(C=0.02, I_mmh=80, A_ha=5)


class TestCalculateRationalFlowDetailed:
    """Tests para la función calculate_rational_flow_detailed."""

    def test_detailed_output_structure(self):
        """Test que verifica la estructura del output detallado."""
        result = calculate_rational_flow_detailed(
            C=0.65,
            I_mmh=80,
            A_ha=5,
            description="Test cuenca"
        )

        # Verificar que tiene todas las claves esperadas
        assert 'Q_ls' in result
        assert 'Q_m3s' in result
        assert 'Q_m3h' in result
        assert 'inputs' in result
        assert 'description' in result
        assert 'warnings' in result

    def test_detailed_output_values(self):
        """Test de valores en output detallado."""
        result = calculate_rational_flow_detailed(
            C=0.65,
            I_mmh=80,
            A_ha=5
        )

        # Verificar caudales
        assert result['Q_ls'] == 722.28
        assert result['Q_m3s'] == 0.7223
        assert result['Q_m3h'] == 2600.21

    def test_detailed_inputs(self):
        """Test de valores de entrada en el resultado."""
        result = calculate_rational_flow_detailed(
            C=0.65,
            I_mmh=80,
            A_ha=5
        )

        inputs = result['inputs']
        assert inputs['C'] == 0.65
        assert inputs['I_mmh'] == 80
        assert inputs['A_ha'] == 5
        assert inputs['A_m2'] == 50000.0
        assert inputs['A_km2'] == 0.05

    def test_detailed_with_description(self):
        """Test con descripción."""
        result = calculate_rational_flow_detailed(
            C=0.65,
            I_mmh=80,
            A_ha=5,
            description="Cuenca residencial norte"
        )

        assert result['description'] == "Cuenca residencial norte"

    def test_detailed_warnings_capture(self):
        """Test que captura warnings en el resultado."""
        result = calculate_rational_flow_detailed(
            C=0.65,
            I_mmh=600,  # Muy alta - genera warning
            A_ha=5
        )

        assert len(result['warnings']) > 0
        assert any('Intensidad muy alta' in w for w in result['warnings'])

    def test_detailed_no_warnings(self):
        """Test sin warnings."""
        result = calculate_rational_flow_detailed(
            C=0.65,
            I_mmh=80,
            A_ha=5
        )

        assert result['warnings'] == []


class TestCalculateWeightedC:
    """Tests para la función calculate_weighted_C."""

    def test_single_surface(self):
        """Test con una sola superficie."""
        areas = [(10, 0.5)]
        C_weighted = calculate_weighted_C(areas)
        assert C_weighted == 0.5

    def test_two_surfaces_equal_area(self):
        """Test con dos superficies de igual área."""
        areas = [(5, 0.8), (5, 0.2)]
        C_weighted = calculate_weighted_C(areas)
        # (5*0.8 + 5*0.2) / 10 = 5 / 10 = 0.5
        assert C_weighted == 0.5

    def test_multiple_surfaces(self):
        """Test con múltiples superficies (caso típico)."""
        areas = [
            (2, 0.90),  # Techos
            (3, 0.85),  # Pavimento
            (5, 0.20)   # Césped
        ]
        C_weighted = calculate_weighted_C(areas)
        # (2*0.9 + 3*0.85 + 5*0.2) / 10 = (1.8 + 2.55 + 1.0) / 10 = 5.35 / 10 = 0.535
        assert round(C_weighted, 3) == 0.535

    def test_weighted_impermeability(self):
        """Test con 70% impermeable, 30% permeable."""
        areas = [
            (7, 0.9),   # 70% impermeable
            (3, 0.1)    # 30% permeable
        ]
        C_weighted = calculate_weighted_C(areas)
        # (7*0.9 + 3*0.1) / 10 = 6.6 / 10 = 0.66
        assert round(C_weighted, 2) == 0.66

    def test_empty_list(self):
        """Test con lista vacía (debe fallar)."""
        with pytest.raises(ValueError, match="al menos un área"):
            calculate_weighted_C([])

    def test_negative_area(self):
        """Test con área negativa (debe fallar)."""
        with pytest.raises(ValueError, match="debe ser positiva"):
            calculate_weighted_C([(5, 0.8), (-2, 0.5)])

    def test_zero_area(self):
        """Test con área cero (debe fallar)."""
        with pytest.raises(ValueError, match="debe ser positiva"):
            calculate_weighted_C([(0, 0.8)])

    def test_invalid_coefficient_low(self):
        """Test con coeficiente < 0 (debe fallar)."""
        with pytest.raises(ValueError, match="entre 0 y 1"):
            calculate_weighted_C([(5, -0.1)])

    def test_invalid_coefficient_high(self):
        """Test con coeficiente > 1 (debe fallar)."""
        with pytest.raises(ValueError, match="entre 0 y 1"):
            calculate_weighted_C([(5, 1.5)])


class TestGetRunoffCoefficients:
    """Tests para la función get_runoff_coefficients."""

    def test_returns_dict(self):
        """Test que retorna un diccionario."""
        coeffs = get_runoff_coefficients()
        assert isinstance(coeffs, dict)

    def test_has_expected_keys(self):
        """Test que tiene las claves esperadas."""
        coeffs = get_runoff_coefficients()
        expected_keys = [
            'techos',
            'pavimento_asfalto',
            'cesped_plano_2pct',
            'comercial',
            'residencial_alta_densidad'
        ]
        for key in expected_keys:
            assert key in coeffs

    def test_coefficient_structure(self):
        """Test de estructura de cada coeficiente."""
        coeffs = get_runoff_coefficients()
        for key, data in coeffs.items():
            assert 'min' in data
            assert 'max' in data
            assert 'tipico' in data
            assert 'descripcion' in data
            # Verificar rangos válidos
            assert 0 <= data['min'] <= 1
            assert 0 <= data['max'] <= 1
            assert 0 <= data['tipico'] <= 1
            assert data['min'] <= data['tipico'] <= data['max']

    def test_typical_values(self):
        """Test de valores típicos específicos."""
        coeffs = get_runoff_coefficients()

        # Techos deben tener C alto
        assert coeffs['techos']['tipico'] >= 0.75

        # Césped plano debe tener C bajo
        assert coeffs['cesped_plano_2pct']['tipico'] <= 0.15

        # Comercial debe tener C alto
        assert coeffs['comercial']['tipico'] >= 0.70
