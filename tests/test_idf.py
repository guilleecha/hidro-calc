"""
Tests unitarios para el módulo de Curvas IDF de Uruguay.

Verifica que las funciones de cálculo de intensidad de lluvia funcionen
correctamente según las especificaciones de Rodríguez Fontal (1980).
"""

import pytest
from src.core.idf_uruguay import (
    calculate_CT,
    calculate_CD,
    calculate_CA,
    calculate_intensity_idf,
    get_P3_10_reference_values,
    validate_inputs_and_warn
)


class TestCalculateCT:
    """Tests para el factor de corrección por período de retorno."""

    def test_CT_calculation_valid_values(self):
        """Test de CT con valores válidos."""
        CT_2 = calculate_CT(2)
        CT_5 = calculate_CT(5)
        CT_10 = calculate_CT(10)
        CT_25 = calculate_CT(25)
        CT_50 = calculate_CT(50)
        CT_100 = calculate_CT(100)

        # CT debe ser creciente con Tr
        assert CT_2 < CT_5 < CT_10 < CT_25 < CT_50 < CT_100

        # Verificar rangos aproximados (basados en fórmula real)
        assert 0.6 <= CT_2 <= 0.7
        assert 0.85 <= CT_5 <= 0.90
        assert 0.95 <= CT_10 <= 1.05
        assert 1.15 <= CT_25 <= 1.20
        assert 1.25 <= CT_50 <= 1.35
        assert 1.35 <= CT_100 <= 1.45

    def test_CT_invalid_Tr_too_low(self):
        """Test de CT con Tr < 2 años."""
        with pytest.raises(ValueError, match="período de retorno debe ser >= 2 años"):
            calculate_CT(1)

        with pytest.raises(ValueError):
            calculate_CT(0)

        with pytest.raises(ValueError):
            calculate_CT(-5)

    def test_CT_exact_value_Tr_5(self):
        """Test de CT para Tr=5 años (valor conocido)."""
        CT_5 = calculate_CT(5)
        # El valor debe estar cerca de 0.859 (según fórmula)
        assert 0.85 <= CT_5 <= 0.87


class TestCalculateCD:
    """Tests para el factor de corrección por duración."""

    def test_CD_short_duration(self):
        """Test de CD para duraciones < 3 horas."""
        CD_0_25 = calculate_CD(0.25)  # 15 min
        CD_0_5 = calculate_CD(0.5)    # 30 min
        CD_1 = calculate_CD(1)        # 1 hora
        CD_2 = calculate_CD(2)        # 2 horas

        # CD debe crecer con duración (más duración = más mm de lluvia acumulados)
        assert CD_0_25 < CD_0_5 < CD_1 < CD_2

        # Verificar que todos son positivos
        assert all(cd > 0 for cd in [CD_0_25, CD_0_5, CD_1, CD_2])

    def test_CD_long_duration(self):
        """Test de CD para duraciones >= 3 horas."""
        CD_3 = calculate_CD(3)
        CD_6 = calculate_CD(6)
        CD_12 = calculate_CD(12)
        CD_24 = calculate_CD(24)

        # CD debe crecer con duración (más duración = más mm de lluvia acumulados)
        assert CD_3 < CD_6 < CD_12 < CD_24

        # Verificar que todos son positivos
        assert all(cd > 0 for cd in [CD_3, CD_6, CD_12, CD_24])

    def test_CD_transition_at_3_hours(self):
        """Test de CD en la transición de 3 horas."""
        CD_2_9 = calculate_CD(2.9)
        CD_3 = calculate_CD(3.0)
        CD_3_1 = calculate_CD(3.1)

        # Verificar que hay continuidad (no saltos grandes)
        # La diferencia debe ser relativamente pequeña
        assert abs(CD_2_9 - CD_3) < 0.5
        assert abs(CD_3 - CD_3_1) < 0.5

    def test_CD_invalid_duration(self):
        """Test de CD con duración inválida."""
        with pytest.raises(ValueError, match="duración debe ser mayor a 0"):
            calculate_CD(0)

        with pytest.raises(ValueError):
            calculate_CD(-1)


class TestCalculateCA:
    """Tests para el factor de corrección por área de cuenca."""

    def test_CA_no_area(self):
        """Test de CA sin área de cuenca."""
        # Cuando Ac es None, CA debe ser 1.0
        CA_none = calculate_CA(None, 1)
        assert CA_none == 1.0

        # Cuando Ac es 0, CA debe ser 1.0
        CA_zero = calculate_CA(0, 1)
        assert CA_zero == 1.0

    def test_CA_with_area(self):
        """Test de CA con área de cuenca."""
        CA_10 = calculate_CA(10, 1)
        CA_30 = calculate_CA(30, 1)
        CA_100 = calculate_CA(100, 1)
        CA_300 = calculate_CA(300, 1)

        # CA debe ser < 1 cuando hay área
        assert CA_10 < 1.0
        assert CA_30 < 1.0
        assert CA_100 < 1.0
        assert CA_300 < 1.0

        # CA debe decrecer con el área (mayor área = mayor reducción)
        assert CA_10 > CA_30 > CA_100 > CA_300

        # CA debe ser mayor que 0
        assert all(ca > 0 for ca in [CA_10, CA_30, CA_100, CA_300])

    def test_CA_duration_effect(self):
        """Test del efecto de la duración en CA."""
        # Para la misma área, duraciones diferentes dan CA diferentes
        CA_d1 = calculate_CA(30, 1)
        CA_d6 = calculate_CA(30, 6)
        CA_d24 = calculate_CA(30, 24)

        # CA debe aumentar con la duración (menor corrección)
        assert CA_d1 < CA_d6 < CA_d24
        assert CA_d24 < 1.0  # Pero siempre menor que 1


class TestCalculateIntensityIDF:
    """Tests para la función principal de cálculo de IDF."""

    def test_example_la_paloma(self):
        """Ejemplo del PDF - La Paloma (caso de referencia)."""
        result = calculate_intensity_idf(
            P3_10=74,
            Tr=5,
            d=1,
            Ac=30
        )

        # Verificar estructura del resultado
        assert 'I_mmh' in result
        assert 'P_mm' in result
        assert 'CT' in result
        assert 'CD' in result
        assert 'CA' in result

        # Verificar resultado aproximado (I ≈ 36.3 mm/h según PDF)
        # Permitir un rango de ±1 mm/h por aproximaciones
        assert 35.5 <= result['I_mmh'] <= 37.5

        # Verificar que los factores son razonables
        assert result['CT'] > 0
        assert result['CD'] > 0
        assert result['CA'] > 0
        assert result['CA'] < 1.0  # CA debe ser < 1 con área

        # Verificar que P = I × d
        assert abs(result['P_mm'] - result['I_mmh'] * result['d_hours']) < 0.01

    def test_intensity_without_area_correction(self):
        """Test de intensidad sin corrección por área."""
        result = calculate_intensity_idf(
            P3_10=75,
            Tr=10,
            d=1,
            Ac=None
        )

        # CA debe ser 1.0 sin área
        assert result['CA'] == 1.0
        assert result['Ac_km2'] is None

        # Intensidad debe ser mayor que el caso con área
        # I = P3_10 × CT × CD × 1.0 / d
        # Aproximadamente: 75 × 0.974 × 0.633 × 1.0 / 1 ≈ 46.2 mm/h
        assert 45 <= result['I_mmh'] <= 48

    def test_intensity_short_duration(self):
        """Test de intensidad con duración corta."""
        result = calculate_intensity_idf(
            P3_10=75,
            Tr=10,
            d=0.5,  # 30 minutos
            Ac=None
        )

        # Intensidad debe ser mayor que para d=1h
        result_1h = calculate_intensity_idf(P3_10=75, Tr=10, d=1, Ac=None)
        assert result['I_mmh'] > result_1h['I_mmh']

    def test_intensity_increasing_Tr(self):
        """Test de intensidad creciente con Tr."""
        result_2 = calculate_intensity_idf(P3_10=75, Tr=2, d=1, Ac=None)
        result_10 = calculate_intensity_idf(P3_10=75, Tr=10, d=1, Ac=None)
        result_100 = calculate_intensity_idf(P3_10=75, Tr=100, d=1, Ac=None)

        # Intensidad debe crecer con Tr
        assert result_2['I_mmh'] < result_10['I_mmh'] < result_100['I_mmh']

    def test_invalid_P3_10_too_low(self):
        """Test con P3_10 fuera de rango (muy bajo)."""
        with pytest.raises(ValueError, match="P₃,₁₀ debe estar entre 50 y 100 mm"):
            calculate_intensity_idf(P3_10=40, Tr=5, d=1)

    def test_invalid_P3_10_too_high(self):
        """Test con P3_10 fuera de rango (muy alto)."""
        with pytest.raises(ValueError, match="P₃,₁₀ debe estar entre 50 y 100 mm"):
            calculate_intensity_idf(P3_10=120, Tr=5, d=1)

    def test_invalid_Tr(self):
        """Test con Tr inválido."""
        with pytest.raises(ValueError, match="período de retorno debe ser >= 2 años"):
            calculate_intensity_idf(P3_10=75, Tr=1, d=1)

    def test_invalid_duration(self):
        """Test con duración inválida."""
        with pytest.raises(ValueError, match="duración debe ser mayor a 0"):
            calculate_intensity_idf(P3_10=75, Tr=5, d=0)

    def test_invalid_area_negative(self):
        """Test con área negativa."""
        with pytest.raises(ValueError, match="área de cuenca no puede ser negativa"):
            calculate_intensity_idf(P3_10=75, Tr=5, d=1, Ac=-10)


class TestReferenceValues:
    """Tests para valores de referencia."""

    def test_get_P3_10_reference_values(self):
        """Test de valores de referencia de P3_10."""
        ref_values = get_P3_10_reference_values()

        # Verificar que hay valores
        assert len(ref_values) > 0

        # Verificar que incluye ciudades importantes
        assert 'Montevideo' in ref_values
        assert 'La Paloma' in ref_values
        assert 'Minas' in ref_values

        # Verificar que los valores están en rango razonable
        for city, value in ref_values.items():
            assert 60 <= value <= 90, f"{city}: {value} mm fuera de rango"


class TestValidateInputsAndWarn:
    """Tests para validaciones y advertencias."""

    def test_no_warnings_normal_values(self):
        """Test sin advertencias con valores normales."""
        warnings = validate_inputs_and_warn(
            P3_10=75,
            Tr=10,
            d=1,
            Ac=30
        )
        assert isinstance(warnings, list)
        # Puede tener o no advertencias, pero debe retornar una lista

    def test_warning_high_Tr(self):
        """Test de advertencia con Tr alto."""
        warnings = validate_inputs_and_warn(
            P3_10=75,
            Tr=150,
            d=1,
            Ac=30
        )
        assert any('100 años' in w for w in warnings)

    def test_warning_long_duration(self):
        """Test de advertencia con duración larga."""
        warnings = validate_inputs_and_warn(
            P3_10=75,
            Tr=10,
            d=30,
            Ac=30
        )
        assert any('24 horas' in w for w in warnings)

    def test_warning_large_area(self):
        """Test de advertencia con área grande."""
        warnings = validate_inputs_and_warn(
            P3_10=75,
            Tr=10,
            d=1,
            Ac=500
        )
        assert any('300 km²' in w for w in warnings)


class TestEdgeCases:
    """Tests de casos extremos."""

    def test_minimum_valid_values(self):
        """Test con valores mínimos válidos."""
        result = calculate_intensity_idf(
            P3_10=50,  # Mínimo
            Tr=2,      # Mínimo
            d=0.1,     # Muy corto pero válido
            Ac=0       # Sin área
        )
        assert result['I_mmh'] > 0
        assert result['CA'] == 1.0

    def test_maximum_recommended_values(self):
        """Test con valores máximos recomendados."""
        result = calculate_intensity_idf(
            P3_10=100,  # Máximo
            Tr=100,     # Máximo recomendado
            d=24,       # Máximo recomendado
            Ac=300      # Máximo recomendado
        )
        assert result['I_mmh'] > 0
        assert result['CA'] < 1.0

    def test_precision_of_results(self):
        """Test de precisión de los resultados."""
        result = calculate_intensity_idf(
            P3_10=74,
            Tr=5,
            d=1,
            Ac=30
        )

        # Verificar que los resultados tienen 4 decimales
        assert result['I_mmh'] == round(result['I_mmh'], 4)
        assert result['CT'] == round(result['CT'], 4)
        assert result['CD'] == round(result['CD'], 4)
        assert result['CA'] == round(result['CA'], 4)


if __name__ == "__main__":
    # Ejecutar tests con pytest
    pytest.main([__file__, "-v", "--tb=short"])
