"""
Tests unitarios para utilidades de conversión de unidades.
"""

import pytest
from calculators.utils.conversions import (
    ha_to_m2, m2_to_ha, ha_to_km2, km2_to_ha,
    ls_to_m3s, m3s_to_ls, m3s_to_m3h, m3h_to_m3s, ls_to_m3h, m3h_to_ls,
    mm_to_m, m_to_mm, km_to_m, m_to_km,
    ms_to_kmh, kmh_to_ms,
    mmh_to_ms, ms_to_mmh,
    convert_units,
    get_flow_in_multiple_units,
    get_area_in_multiple_units
)


class TestAreaConversions:
    """Tests para conversiones de área."""

    def test_ha_to_m2(self):
        """Test conversión de hectáreas a m²."""
        assert ha_to_m2(1) == 10000
        assert ha_to_m2(5) == 50000
        assert ha_to_m2(0.5) == 5000

    def test_m2_to_ha(self):
        """Test conversión de m² a hectáreas."""
        assert m2_to_ha(10000) == 1
        assert m2_to_ha(50000) == 5
        assert m2_to_ha(5000) == 0.5

    def test_ha_to_km2(self):
        """Test conversión de hectáreas a km²."""
        assert ha_to_km2(100) == 1
        assert ha_to_km2(50) == 0.5
        assert ha_to_km2(1) == 0.01

    def test_km2_to_ha(self):
        """Test conversión de km² a hectáreas."""
        assert km2_to_ha(1) == 100
        assert km2_to_ha(0.5) == 50
        assert km2_to_ha(0.01) == 1

    def test_area_round_trip_ha_m2(self):
        """Test conversión ida y vuelta ha ↔ m²."""
        original = 7.5
        converted = m2_to_ha(ha_to_m2(original))
        assert abs(converted - original) < 1e-10

    def test_area_round_trip_ha_km2(self):
        """Test conversión ida y vuelta ha ↔ km²."""
        original = 150
        converted = km2_to_ha(ha_to_km2(original))
        assert abs(converted - original) < 1e-10


class TestFlowConversions:
    """Tests para conversiones de caudal."""

    def test_ls_to_m3s(self):
        """Test conversión de L/s a m³/s."""
        assert ls_to_m3s(1000) == 1
        assert ls_to_m3s(500) == 0.5
        assert ls_to_m3s(1) == 0.001

    def test_m3s_to_ls(self):
        """Test conversión de m³/s a L/s."""
        assert m3s_to_ls(1) == 1000
        assert m3s_to_ls(0.5) == 500
        assert m3s_to_ls(0.001) == 1

    def test_m3s_to_m3h(self):
        """Test conversión de m³/s a m³/h."""
        assert m3s_to_m3h(1) == 3600
        assert m3s_to_m3h(0.5) == 1800

    def test_m3h_to_m3s(self):
        """Test conversión de m³/h a m³/s."""
        assert m3h_to_m3s(3600) == 1
        assert m3h_to_m3s(1800) == 0.5

    def test_ls_to_m3h(self):
        """Test conversión de L/s a m³/h."""
        assert ls_to_m3h(1000) == 3600
        assert ls_to_m3h(100) == 360

    def test_m3h_to_ls(self):
        """Test conversión de m³/h a L/s."""
        assert abs(m3h_to_ls(3600) - 1000) < 1e-10
        assert abs(m3h_to_ls(360) - 100) < 1e-10

    def test_flow_round_trip_ls_m3s(self):
        """Test conversión ida y vuelta L/s ↔ m³/s."""
        original = 250
        converted = m3s_to_ls(ls_to_m3s(original))
        assert abs(converted - original) < 1e-10


class TestLengthConversions:
    """Tests para conversiones de longitud."""

    def test_mm_to_m(self):
        """Test conversión de mm a m."""
        assert mm_to_m(1000) == 1
        assert mm_to_m(500) == 0.5
        assert mm_to_m(1) == 0.001

    def test_m_to_mm(self):
        """Test conversión de m a mm."""
        assert m_to_mm(1) == 1000
        assert m_to_mm(0.5) == 500
        assert m_to_mm(0.001) == 1

    def test_km_to_m(self):
        """Test conversión de km a m."""
        assert km_to_m(1) == 1000
        assert km_to_m(5) == 5000
        assert km_to_m(0.5) == 500

    def test_m_to_km(self):
        """Test conversión de m a km."""
        assert m_to_km(1000) == 1
        assert m_to_km(5000) == 5
        assert m_to_km(500) == 0.5


class TestVelocityConversions:
    """Tests para conversiones de velocidad."""

    def test_ms_to_kmh(self):
        """Test conversión de m/s a km/h."""
        assert ms_to_kmh(1) == 3.6
        assert abs(ms_to_kmh(10) - 36) < 1e-10
        assert abs(ms_to_kmh(27.78) - 100) < 0.1

    def test_kmh_to_ms(self):
        """Test conversión de km/h a m/s."""
        assert abs(kmh_to_ms(3.6) - 1) < 1e-10
        assert abs(kmh_to_ms(36) - 10) < 1e-10
        assert abs(kmh_to_ms(100) - 27.78) < 0.01

    def test_velocity_round_trip(self):
        """Test conversión ida y vuelta m/s ↔ km/h."""
        original = 15
        converted = kmh_to_ms(ms_to_kmh(original))
        assert abs(converted - original) < 1e-10


class TestIntensityConversions:
    """Tests para conversiones de intensidad de lluvia."""

    def test_mmh_to_ms(self):
        """Test conversión de mm/h a m/s."""
        # 1 mm/h = 1/(1000*3600) m/s
        result = mmh_to_ms(1)
        expected = 1 / (1000 * 3600)
        assert abs(result - expected) < 1e-12

    def test_ms_to_mmh(self):
        """Test conversión de m/s a mm/h."""
        # 1 m/s = 1000*3600 mm/h = 3,600,000 mm/h
        result = ms_to_mmh(1)
        expected = 1000 * 3600
        assert result == expected

    def test_intensity_round_trip(self):
        """Test conversión ida y vuelta mm/h ↔ m/s."""
        original = 80  # mm/h típico
        converted = ms_to_mmh(mmh_to_ms(original))
        assert abs(converted - original) < 1e-6


class TestUniversalConversion:
    """Tests para la función universal convert_units."""

    def test_area_conversions(self):
        """Test conversiones de área con convert_units."""
        assert convert_units(5, "ha", "m2") == 50000
        assert convert_units(50000, "m2", "ha") == 5
        assert convert_units(100, "ha", "km2") == 1
        assert convert_units(1, "km2", "ha") == 100

    def test_flow_conversions(self):
        """Test conversiones de caudal con convert_units."""
        assert convert_units(1000, "L/s", "m3/s") == 1
        assert convert_units(1, "m3/s", "L/s") == 1000
        assert convert_units(1, "m3/s", "m3/h") == 3600

    def test_case_insensitive(self):
        """Test que es case-insensitive."""
        assert convert_units(5, "HA", "M2") == 50000
        assert convert_units(5, "Ha", "m2") == 50000

    def test_same_unit(self):
        """Test conversión a la misma unidad."""
        assert convert_units(100, "ha", "ha") == 100
        assert convert_units(50, "L/s", "L/s") == 50

    def test_unsupported_conversion(self):
        """Test conversión no soportada (debe fallar)."""
        with pytest.raises(ValueError, match="no soportada"):
            convert_units(100, "ha", "L/s")  # Área a caudal

    def test_invalid_unit(self):
        """Test con unidad inválida (debe fallar)."""
        with pytest.raises(ValueError, match="no soportada"):
            convert_units(100, "invalid", "ha")


class TestGetFlowInMultipleUnits:
    """Tests para get_flow_in_multiple_units."""

    def test_flow_100_ls(self):
        """Test con 100 L/s."""
        result = get_flow_in_multiple_units(100)

        assert result['L/s'] == 100.0
        assert result['m3/s'] == 0.1
        assert result['m3/h'] == 360.0
        assert result['m3/day'] == 8640.0

    def test_flow_1000_ls(self):
        """Test con 1000 L/s."""
        result = get_flow_in_multiple_units(1000)

        assert result['L/s'] == 1000.0
        assert result['m3/s'] == 1.0
        assert result['m3/h'] == 3600.0
        assert result['m3/day'] == 86400.0

    def test_flow_contains_all_units(self):
        """Test que contiene todas las unidades esperadas."""
        result = get_flow_in_multiple_units(50)

        expected_keys = ['L/s', 'm3/s', 'm3/h', 'm3/day']
        for key in expected_keys:
            assert key in result

    def test_flow_values_are_numbers(self):
        """Test que todos los valores son numéricos."""
        result = get_flow_in_multiple_units(50)

        for value in result.values():
            assert isinstance(value, (int, float))


class TestGetAreaInMultipleUnits:
    """Tests para get_area_in_multiple_units."""

    def test_area_5_ha(self):
        """Test con 5 hectáreas."""
        result = get_area_in_multiple_units(5)

        assert result['ha'] == 5.0
        assert result['m2'] == 50000.0
        assert result['km2'] == 0.05

    def test_area_100_ha(self):
        """Test con 100 hectáreas (= 1 km²)."""
        result = get_area_in_multiple_units(100)

        assert result['ha'] == 100.0
        assert result['m2'] == 1000000.0
        assert result['km2'] == 1.0

    def test_area_contains_all_units(self):
        """Test que contiene todas las unidades esperadas."""
        result = get_area_in_multiple_units(10)

        expected_keys = ['ha', 'm2', 'km2']
        for key in expected_keys:
            assert key in result

    def test_area_values_are_numbers(self):
        """Test que todos los valores son numéricos."""
        result = get_area_in_multiple_units(10)

        for value in result.values():
            assert isinstance(value, (int, float))
