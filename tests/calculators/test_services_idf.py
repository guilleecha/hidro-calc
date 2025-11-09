"""
Tests unitarios para el servicio de Curvas IDF Uruguay.
"""

import pytest
import math
from calculators.services.idf import (
    calculate_CT,
    calculate_CD,
    calculate_CA,
    calculate_intensity_idf,
    get_P3_10_reference_values,
    validate_inputs_and_warn
)


class TestCalculateCT:
    """Tests para el factor de corrección por período de retorno."""

    def test_tr_5_years(self):
        """Test para Tr=5 años."""
        CT = calculate_CT(5)
        assert round(CT, 4) == 0.8595

    def test_tr_10_years(self):
        """Test para Tr=10 años."""
        CT = calculate_CT(10)
        assert round(CT, 4) == 1.0000

    def test_tr_25_years(self):
        """Test para Tr=25 años."""
        CT = calculate_CT(25)
        assert round(CT, 4) == 1.1776

    def test_tr_50_years(self):
        """Test para Tr=50 años."""
        CT = calculate_CT(50)
        assert round(CT, 4) == 1.3093

    def test_tr_100_years(self):
        """Test para Tr=100 años."""
        CT = calculate_CT(100)
        assert round(CT, 4) == 1.4401

    def test_tr_minimum_2_years(self):
        """Test con Tr mínimo = 2 años."""
        CT = calculate_CT(2)
        assert CT > 0  # Debe dar un valor válido

    def test_tr_below_minimum(self):
        """Test con Tr < 2 años (debe fallar)."""
        with pytest.raises(ValueError, match="debe ser >= 2 años"):
            calculate_CT(1)

    def test_tr_zero(self):
        """Test con Tr=0 (debe fallar)."""
        with pytest.raises(ValueError):
            calculate_CT(0)

    def test_tr_negative(self):
        """Test con Tr negativo (debe fallar)."""
        with pytest.raises(ValueError):
            calculate_CT(-5)

    def test_ct_increases_with_tr(self):
        """Test que CT aumenta con Tr."""
        CT_5 = calculate_CT(5)
        CT_10 = calculate_CT(10)
        CT_25 = calculate_CT(25)
        assert CT_5 < CT_10 < CT_25


class TestCalculateCD:
    """Tests para el factor de corrección por duración."""

    def test_duration_1_hour(self):
        """Test para d=1 hora."""
        CD = calculate_CD(1)
        assert round(CD, 4) == 0.6161

    def test_duration_2_hours(self):
        """Test para d=2 horas."""
        CD = calculate_CD(2)
        assert round(CD, 4) == 0.8367

    def test_duration_3_hours(self):
        """Test para d=3 horas (transición de fórmula)."""
        CD = calculate_CD(3)
        assert 0.9 < CD < 1.1  # Verificar rango razonable (~1.0)

    def test_duration_6_hours(self):
        """Test para d=6 horas."""
        CD = calculate_CD(6)
        assert 1.2 < CD < 1.4  # Verificar rango razonable (~1.28)

    def test_duration_24_hours(self):
        """Test para d=24 horas."""
        CD = calculate_CD(24)
        assert 1.8 < CD < 1.9  # Verificar rango razonable (~1.83)

    def test_duration_0_5_hours(self):
        """Test para d=0.5 horas (30 min)."""
        CD = calculate_CD(0.5)
        assert CD > 0 and CD < 1

    def test_duration_zero(self):
        """Test con d=0 (debe fallar)."""
        with pytest.raises(ValueError, match="debe ser mayor a 0"):
            calculate_CD(0)

    def test_duration_negative(self):
        """Test con d negativa (debe fallar)."""
        with pytest.raises(ValueError, match="debe ser mayor a 0"):
            calculate_CD(-1)

    def test_cd_increases_with_duration(self):
        """Test que CD aumenta con la duración."""
        CD_1 = calculate_CD(1)
        CD_6 = calculate_CD(6)
        CD_24 = calculate_CD(24)
        assert CD_1 < CD_6 < CD_24

    def test_formula_transition_at_3hours(self):
        """Test de transición de fórmula en d=3 horas."""
        CD_before = calculate_CD(2.9)
        CD_at = calculate_CD(3.0)
        CD_after = calculate_CD(3.1)
        # Los valores deben ser continuos (sin saltos grandes)
        assert abs(CD_at - CD_before) < 0.5
        assert abs(CD_after - CD_at) < 0.5


class TestCalculateCA:
    """Tests para el factor de corrección por área."""

    def test_no_area_correction(self):
        """Test sin corrección de área (Ac=None)."""
        CA = calculate_CA(None, 1)
        assert CA == 1.0

    def test_zero_area(self):
        """Test con área cero."""
        CA = calculate_CA(0, 1)
        assert CA == 1.0

    def test_small_area_10km2(self):
        """Test con área pequeña (10 km²)."""
        CA = calculate_CA(10, 1)
        assert CA < 1.0  # Debe reducir la intensidad
        assert CA > 0.9  # Pero no mucho

    def test_medium_area_30km2(self):
        """Test con área mediana (30 km²)."""
        CA = calculate_CA(30, 1)
        assert round(CA, 4) == 0.9434

    def test_large_area_100km2(self):
        """Test con área grande (100 km²)."""
        CA = calculate_CA(100, 1)
        assert CA < 0.9  # Reducción más significativa

    def test_ca_decreases_with_area(self):
        """Test que CA disminuye al aumentar el área."""
        CA_10 = calculate_CA(10, 1)
        CA_30 = calculate_CA(30, 1)
        CA_100 = calculate_CA(100, 1)
        assert CA_10 > CA_30 > CA_100

    def test_ca_varies_with_duration(self):
        """Test que CA varía con la duración."""
        CA_1h = calculate_CA(30, 1)
        CA_24h = calculate_CA(30, 24)
        assert CA_1h != CA_24h


class TestCalculateIntensityIDF:
    """Tests para el cálculo completo de intensidad IDF."""

    def test_example_la_paloma(self):
        """Test del ejemplo del PDF - La Paloma."""
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

        # Verificar valores aproximados del ejemplo
        assert 36 < result['I_mmh'] < 38  # ~37.46 mm/h
        assert round(result['CT'], 2) == 0.86
        assert round(result['CD'], 2) == 0.62
        assert round(result['CA'], 2) == 0.94

    def test_montevideo_typical(self):
        """Test con valores típicos de Montevideo."""
        result = calculate_intensity_idf(
            P3_10=75,
            Tr=10,
            d=1,
            Ac=None  # Sin corrección por área
        )

        assert result['I_mmh'] > 0
        assert result['P_mm'] == result['I_mmh']  # Para d=1h
        assert result['CA'] == 1.0  # Sin corrección

    def test_without_area_correction(self):
        """Test sin corrección por área."""
        result = calculate_intensity_idf(
            P3_10=75,
            Tr=5,
            d=2,
            Ac=None
        )

        assert result['Ac_km2'] is None
        assert result['CA'] == 1.0

    def test_precipitation_equals_intensity_times_duration(self):
        """Test que P = I × d."""
        result = calculate_intensity_idf(
            P3_10=75,
            Tr=5,
            d=3
        )

        # P_mm debe ser igual a I_mmh * d_hours
        expected_P = result['I_mmh'] * result['d_hours']
        assert abs(result['P_mm'] - expected_P) < 0.01

    def test_p3_10_below_range(self):
        """Test con P3_10 fuera de rango inferior."""
        with pytest.raises(ValueError, match="entre 50 y 100"):
            calculate_intensity_idf(P3_10=40, Tr=5, d=1)

    def test_p3_10_above_range(self):
        """Test con P3_10 fuera de rango superior."""
        with pytest.raises(ValueError, match="entre 50 y 100"):
            calculate_intensity_idf(P3_10=110, Tr=5, d=1)

    def test_tr_below_minimum(self):
        """Test con Tr < 2 años."""
        with pytest.raises(ValueError, match="debe ser >= 2 años"):
            calculate_intensity_idf(P3_10=75, Tr=1, d=1)

    def test_duration_zero(self):
        """Test con duración cero."""
        with pytest.raises(ValueError, match="debe ser mayor a 0"):
            calculate_intensity_idf(P3_10=75, Tr=5, d=0)

    def test_negative_area(self):
        """Test con área negativa."""
        with pytest.raises(ValueError, match="no puede ser negativa"):
            calculate_intensity_idf(P3_10=75, Tr=5, d=1, Ac=-10)

    def test_intensity_decreases_with_duration(self):
        """Test que la intensidad disminuye con la duración."""
        result_1h = calculate_intensity_idf(P3_10=75, Tr=5, d=1)
        result_6h = calculate_intensity_idf(P3_10=75, Tr=5, d=6)
        result_24h = calculate_intensity_idf(P3_10=75, Tr=5, d=24)

        assert result_1h['I_mmh'] > result_6h['I_mmh'] > result_24h['I_mmh']

    def test_intensity_increases_with_tr(self):
        """Test que la intensidad aumenta con Tr."""
        result_5 = calculate_intensity_idf(P3_10=75, Tr=5, d=1)
        result_10 = calculate_intensity_idf(P3_10=75, Tr=10, d=1)
        result_25 = calculate_intensity_idf(P3_10=75, Tr=25, d=1)

        assert result_5['I_mmh'] < result_10['I_mmh'] < result_25['I_mmh']


class TestGetP310ReferenceValues:
    """Tests para valores de referencia de P3_10."""

    def test_returns_dict(self):
        """Test que retorna un diccionario."""
        values = get_P3_10_reference_values()
        assert isinstance(values, dict)

    def test_has_montevideo(self):
        """Test que incluye Montevideo."""
        values = get_P3_10_reference_values()
        assert 'Montevideo' in values

    def test_has_major_cities(self):
        """Test que incluye ciudades principales."""
        values = get_P3_10_reference_values()
        expected_cities = [
            'Montevideo', 'Salto', 'Paysandú',
            'Rivera', 'Colonia', 'Punta del Este'
        ]
        for city in expected_cities:
            assert city in values

    def test_values_in_valid_range(self):
        """Test que todos los valores están en rango válido."""
        values = get_P3_10_reference_values()
        for city, value in values.items():
            assert 50 <= value <= 100, f"{city}: {value} fuera de rango"

    def test_montevideo_value(self):
        """Test del valor específico de Montevideo."""
        values = get_P3_10_reference_values()
        assert values['Montevideo'] == 75.0


class TestValidateInputsAndWarn:
    """Tests para la función de validación y warnings."""

    def test_normal_values_no_warnings(self):
        """Test con valores normales (sin warnings)."""
        warnings = validate_inputs_and_warn(
            P3_10=75,
            Tr=10,
            d=6,
            Ac=50
        )
        assert len(warnings) == 0

    def test_p3_10_too_low(self):
        """Test con P3_10 bajo."""
        warnings = validate_inputs_and_warn(
            P3_10=55,
            Tr=10,
            d=6,
            Ac=50
        )
        assert len(warnings) > 0
        assert any('menor a 60' in w for w in warnings)

    def test_p3_10_too_high(self):
        """Test con P3_10 alto."""
        warnings = validate_inputs_and_warn(
            P3_10=95,
            Tr=10,
            d=6,
            Ac=50
        )
        assert len(warnings) > 0
        assert any('mayor a 90' in w for w in warnings)

    def test_tr_very_high(self):
        """Test con Tr muy alto."""
        warnings = validate_inputs_and_warn(
            P3_10=75,
            Tr=150,
            d=6,
            Ac=50
        )
        assert len(warnings) > 0
        assert any('>100 años' in w for w in warnings)

    def test_duration_very_long(self):
        """Test con duración muy larga."""
        warnings = validate_inputs_and_warn(
            P3_10=75,
            Tr=10,
            d=30,
            Ac=50
        )
        assert len(warnings) > 0
        assert any('mayor a 24 horas' in w for w in warnings)

    def test_area_very_large(self):
        """Test con área muy grande."""
        warnings = validate_inputs_and_warn(
            P3_10=75,
            Tr=10,
            d=6,
            Ac=350
        )
        assert len(warnings) > 0
        assert any('>300 km²' in w for w in warnings)

    def test_multiple_warnings(self):
        """Test que genera múltiples warnings."""
        warnings = validate_inputs_and_warn(
            P3_10=55,   # Bajo
            Tr=150,     # Alto
            d=30,       # Larga
            Ac=350      # Grande
        )
        assert len(warnings) >= 4

    def test_no_area_no_warning(self):
        """Test sin área (no debe generar warning de área)."""
        warnings = validate_inputs_and_warn(
            P3_10=75,
            Tr=10,
            d=6,
            Ac=None
        )
        assert not any('km²' in w for w in warnings)
