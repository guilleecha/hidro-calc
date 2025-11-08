"""
Tests unitarios para el módulo del Método Racional.
"""

import pytest
from src.core.rational_method import (
    calculate_rational_flow,
    calculate_rational_flow_detailed,
    calculate_weighted_C
)


class TestRationalMethod:
    """Tests para el cálculo del Método Racional."""

    def test_basic_calculation(self):
        """Test cálculo básico del método racional."""
        # Q = C × I × A × 2.778
        # Q = 0.65 × 80 × 5 × 2.778 = 722.2 L/s
        Q = calculate_rational_flow(C=0.65, I_mmh=80, A_ha=5)
        assert pytest.approx(Q, rel=0.01) == 722.2

    def test_different_values(self):
        """Test con diferentes valores."""
        # Q = 0.85 × 100 × 10 × 2.778 = 2361.3 L/s
        Q = calculate_rational_flow(C=0.85, I_mmh=100, A_ha=10)
        assert pytest.approx(Q, rel=0.01) == 2361.3

    def test_zero_intensity(self):
        """Test con intensidad cero resulta en caudal cero."""
        Q = calculate_rational_flow(C=0.65, I_mmh=0, A_ha=5)
        assert Q == 0

    def test_zero_area(self):
        """Test con área cero debe lanzar ValueError."""
        with pytest.raises(ValueError, match="área.*debe ser positiva"):
            calculate_rational_flow(C=0.65, I_mmh=80, A_ha=0)

    def test_negative_area(self):
        """Test con área negativa debe lanzar ValueError."""
        with pytest.raises(ValueError, match="área.*debe ser positiva"):
            calculate_rational_flow(C=0.65, I_mmh=80, A_ha=-5)

    def test_negative_intensity(self):
        """Test con intensidad negativa debe lanzar ValueError."""
        with pytest.raises(ValueError, match="intensidad.*no puede ser negativa"):
            calculate_rational_flow(C=0.65, I_mmh=-80, A_ha=5)

    def test_invalid_C_below_zero(self):
        """Test con C < 0 debe lanzar ValueError."""
        with pytest.raises(ValueError, match="coeficiente.*debe estar entre 0 y 1"):
            calculate_rational_flow(C=-0.1, I_mmh=80, A_ha=5)

    def test_invalid_C_above_one(self):
        """Test con C > 1 debe lanzar ValueError."""
        with pytest.raises(ValueError, match="coeficiente.*debe estar entre 0 y 1"):
            calculate_rational_flow(C=1.5, I_mmh=80, A_ha=5)

    def test_C_limits(self):
        """Test con valores límite de C (0 y 1)."""
        # C = 0
        Q_zero = calculate_rational_flow(C=0, I_mmh=80, A_ha=5)
        assert Q_zero == 0

        # C = 1
        Q_one = calculate_rational_flow(C=1, I_mmh=80, A_ha=5)
        expected = (1 * 80 * 5) * 2.778
        assert pytest.approx(Q_one, rel=0.01) == expected

    def test_warnings_high_intensity(self):
        """Test que genera advertencia con intensidad alta."""
        with pytest.warns(UserWarning, match="Intensidad muy alta"):
            calculate_rational_flow(C=0.65, I_mmh=600, A_ha=5)

    def test_warnings_large_area(self):
        """Test que genera advertencia con área grande."""
        with pytest.warns(UserWarning, match="Área grande"):
            calculate_rational_flow(C=0.65, I_mmh=80, A_ha=300)

    def test_warnings_low_C(self):
        """Test que genera advertencia con C muy bajo."""
        with pytest.warns(UserWarning, match="Coeficiente.*muy bajo"):
            calculate_rational_flow(C=0.02, I_mmh=80, A_ha=5)


class TestRationalMethodDetailed:
    """Tests para el cálculo detallado del método racional."""

    def test_detailed_output_structure(self):
        """Test que la salida detallada tiene la estructura correcta."""
        result = calculate_rational_flow_detailed(C=0.65, I_mmh=80, A_ha=5)

        # Verificar claves principales
        assert 'Q_ls' in result
        assert 'Q_m3s' in result
        assert 'Q_m3h' in result
        assert 'inputs' in result
        assert 'description' in result
        assert 'warnings' in result

        # Verificar inputs
        assert 'C' in result['inputs']
        assert 'I_mmh' in result['inputs']
        assert 'A_ha' in result['inputs']
        assert 'A_m2' in result['inputs']
        assert 'A_km2' in result['inputs']

    def test_detailed_values(self):
        """Test que los valores detallados son correctos."""
        result = calculate_rational_flow_detailed(C=0.65, I_mmh=80, A_ha=5)

        # Verificar caudal
        assert pytest.approx(result['Q_ls'], rel=0.01) == 722.22

        # Verificar conversiones
        Q_m3s_expected = result['Q_ls'] / 1000
        assert pytest.approx(result['Q_m3s'], rel=0.01) == Q_m3s_expected

        Q_m3h_expected = Q_m3s_expected * 3600
        assert pytest.approx(result['Q_m3h'], rel=0.01) == Q_m3h_expected

        # Verificar área
        assert result['inputs']['A_m2'] == 50000
        assert pytest.approx(result['inputs']['A_km2'], rel=0.01) == 0.05

    def test_detailed_with_description(self):
        """Test con descripción."""
        desc = "Cuenca residencial"
        result = calculate_rational_flow_detailed(
            C=0.65,
            I_mmh=80,
            A_ha=5,
            description=desc
        )

        assert result['description'] == desc

    def test_detailed_captures_warnings(self):
        """Test que captura advertencias."""
        result = calculate_rational_flow_detailed(C=0.65, I_mmh=600, A_ha=5)

        assert len(result['warnings']) > 0
        assert any('Intensidad muy alta' in w for w in result['warnings'])


class TestWeightedC:
    """Tests para el cálculo del coeficiente ponderado."""

    def test_weighted_C_simple(self):
        """Test cálculo simple de C ponderado."""
        # 2 ha con C=0.90, 3 ha con C=0.85, 5 ha con C=0.20
        # C_pond = (2*0.90 + 3*0.85 + 5*0.20) / 10 = (1.8 + 2.55 + 1.0) / 10 = 5.35/10 = 0.535
        areas = [
            (2, 0.90),
            (3, 0.85),
            (5, 0.20)
        ]

        C_weighted = calculate_weighted_C(areas)
        assert pytest.approx(C_weighted, rel=0.01) == 0.535

    def test_weighted_C_single_surface(self):
        """Test con una sola superficie."""
        areas = [(10, 0.65)]
        C_weighted = calculate_weighted_C(areas)
        assert C_weighted == 0.65

    def test_weighted_C_uniform(self):
        """Test con coeficientes uniformes."""
        # Si todos los C son iguales, el resultado debe ser ese C
        areas = [
            (1, 0.75),
            (2, 0.75),
            (3, 0.75)
        ]
        C_weighted = calculate_weighted_C(areas)
        assert C_weighted == 0.75

    def test_weighted_C_empty_list(self):
        """Test con lista vacía debe lanzar ValueError."""
        with pytest.raises(ValueError, match="Debe proporcionar al menos un área"):
            calculate_weighted_C([])

    def test_weighted_C_negative_area(self):
        """Test con área negativa debe lanzar ValueError."""
        areas = [
            (2, 0.90),
            (-3, 0.85)
        ]
        with pytest.raises(ValueError, match="área debe ser positiva"):
            calculate_weighted_C(areas)

    def test_weighted_C_invalid_coefficient(self):
        """Test con coeficiente inválido debe lanzar ValueError."""
        areas = [
            (2, 0.90),
            (3, 1.5)  # C > 1
        ]
        with pytest.raises(ValueError, match="coeficiente C debe estar entre 0 y 1"):
            calculate_weighted_C(areas)

    def test_weighted_C_extreme_case(self):
        """Test caso extremo: áreas muy diferentes."""
        areas = [
            (0.1, 0.95),  # Pequeña área impermeable
            (99.9, 0.05)  # Gran área permeable
        ]
        C_weighted = calculate_weighted_C(areas)

        # Debe estar muy cerca de 0.05 por la diferencia de áreas
        assert pytest.approx(C_weighted, abs=0.01) == 0.059


class TestEdgeCases:
    """Tests de casos límite y especiales."""

    def test_very_small_area(self):
        """Test con área muy pequeña."""
        Q = calculate_rational_flow(C=0.65, I_mmh=80, A_ha=0.01)
        expected = (0.65 * 80 * 0.01) * 2.778
        assert pytest.approx(Q, rel=0.01) == expected

    def test_very_large_values(self):
        """Test con valores grandes pero válidos."""
        Q = calculate_rational_flow(C=0.95, I_mmh=200, A_ha=50)
        expected = (0.95 * 200 * 50) * 2.778
        assert pytest.approx(Q, rel=0.01) == expected

    def test_precision(self):
        """Test de precisión numérica."""
        # Usar valores que podrían causar problemas de precisión
        Q1 = calculate_rational_flow(C=0.333333, I_mmh=77.777, A_ha=4.444)
        Q2 = calculate_rational_flow(C=1/3, I_mmh=77.777, A_ha=4.444)

        # Deben ser aproximadamente iguales
        assert pytest.approx(Q1, rel=0.001) == Q2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
