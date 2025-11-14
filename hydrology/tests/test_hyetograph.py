"""
Tests para el servicio de generación de hietogramas

Prueba la distribución temporal de lluvia usando diferentes métodos.
"""

import pytest
from hydrology.services.hyetograph import (
    generate_hyetograph,
    generate_hyetograph_alternating_block,
    generate_hyetograph_uniform,
    HyetographGenerationError
)


class TestHyetographUniform:
    """Tests para hietograma uniforme"""

    def test_basic_uniform(self):
        """Test hietograma uniforme básico"""
        result = generate_hyetograph(
            total_rainfall_mm=100.0,
            duration_hours=2.0,
            method='uniform',
            time_step_minutes=10.0
        )

        # Verificar estructura
        assert 'rainfall_mm' in result
        assert 'time_steps' in result
        assert 'method' in result
        assert 'total_rainfall_mm' in result
        assert 'duration_hours' in result

        # Verificar valores
        assert result['method'] == 'uniform'
        assert result['total_rainfall_mm'] == 100.0
        assert result['duration_hours'] == 2.0
        assert len(result['rainfall_mm']) > 0
        assert len(result['time_steps']) > 0

        # Verificar que suma total es correcta (con tolerancia para redondeos)
        assert abs(sum(result['rainfall_mm']) - 100.0) < 0.1

    def test_uniform_different_durations(self):
        """Test hietograma uniforme con diferentes duraciones"""
        for duration in [1.0, 2.0, 4.0, 24.0]:
            result = generate_hyetograph(
                total_rainfall_mm=50.0,
                duration_hours=duration,
                method='uniform',
                time_step_minutes=5.0
            )

            assert result['duration_hours'] == duration
            assert abs(sum(result['rainfall_mm']) - 50.0) < 0.1

    def test_uniform_different_timesteps(self):
        """Test hietograma uniforme con diferentes pasos de tiempo"""
        for time_step in [5, 10, 15, 30]:
            result = generate_hyetograph(
                total_rainfall_mm=80.0,
                duration_hours=2.0,
                method='uniform',
                time_step_minutes=float(time_step)
            )

            # Número de intervalos correcto
            expected_intervals = (2.0 * 60) // time_step
            assert len(result['rainfall_mm']) >= expected_intervals - 1
            assert abs(sum(result['rainfall_mm']) - 80.0) < 0.1

    def test_small_rainfall(self):
        """Test con lluvia pequeña"""
        result = generate_hyetograph(
            total_rainfall_mm=1.0,
            duration_hours=1.0,
            method='uniform',
            time_step_minutes=10.0
        )

        assert result['total_rainfall_mm'] == 1.0
        assert abs(sum(result['rainfall_mm']) - 1.0) < 0.01


class TestHyetographAlternatingBlock:
    """Tests para hietograma de bloque alternado"""

    def test_basic_alternating_block(self):
        """Test hietograma bloque alternado básico"""
        result = generate_hyetograph(
            total_rainfall_mm=100.0,
            duration_hours=2.0,
            method='alternating_block',
            time_step_minutes=10.0,
            P3_10=70.0,
            Tr=10.0
        )

        # Verificar estructura
        assert 'rainfall_mm' in result
        assert 'peak_index' in result
        assert 'peak_position_ratio' in result
        assert 'num_intervals' in result
        assert result['method'] == 'alternating_block'

        # Verificar que suma total es correcta
        assert abs(sum(result['rainfall_mm']) - 100.0) < 0.1

        # Verificar peak_index válido
        assert 0 <= result['peak_index'] < len(result['rainfall_mm'])

    def test_peak_position_ratio(self):
        """Test que peak_position_ratio afecta posición del pico"""
        rainfall_early = generate_hyetograph(
            total_rainfall_mm=100.0,
            duration_hours=2.0,
            method='alternating_block',
            time_step_minutes=10.0,
            peak_position_ratio=0.2,  # Pico temprano
            P3_10=70.0,
            Tr=10.0
        )

        rainfall_late = generate_hyetograph(
            total_rainfall_mm=100.0,
            duration_hours=2.0,
            method='alternating_block',
            time_step_minutes=10.0,
            peak_position_ratio=0.8,  # Pico tardío
            P3_10=70.0,
            Tr=10.0
        )

        # El pico temprano debe ocurrir antes
        assert rainfall_early['peak_index'] < rainfall_late['peak_index']

    def test_peak_position_ratio_boundaries(self):
        """Test peak_position_ratio en los límites"""
        # Pico al inicio (ratio=0.1)
        result_start = generate_hyetograph(
            total_rainfall_mm=100.0,
            duration_hours=2.0,
            method='alternating_block',
            time_step_minutes=10.0,
            peak_position_ratio=0.1,
            P3_10=70.0,
            Tr=10.0
        )

        # Pico al final (ratio=0.9)
        result_end = generate_hyetograph(
            total_rainfall_mm=100.0,
            duration_hours=2.0,
            method='alternating_block',
            time_step_minutes=10.0,
            peak_position_ratio=0.9,
            P3_10=70.0,
            Tr=10.0
        )

        # El índice del pico debe ser diferente
        assert result_start['peak_index'] != result_end['peak_index']
        # El inicio debe tener pico más temprano
        assert result_start['peak_index'] < result_end['peak_index']

    def test_alternating_block_idf_required(self):
        """Test que IDF es requerido para bloque alternado"""
        with pytest.raises((ValueError, HyetographGenerationError, TypeError)):
            # Sin P3_10 y Tr
            generate_hyetograph(
                total_rainfall_mm=100.0,
                duration_hours=2.0,
                method='alternating_block',
                time_step_minutes=10.0
            )

    def test_alternating_block_different_durations(self):
        """Test hietograma alternado con diferentes duraciones"""
        for duration in [1.0, 2.0, 6.0, 24.0]:
            result = generate_hyetograph(
                total_rainfall_mm=100.0,
                duration_hours=duration,
                method='alternating_block',
                time_step_minutes=10.0,
                P3_10=70.0,
                Tr=10.0
            )

            # Verificar suma total
            assert abs(sum(result['rainfall_mm']) - 100.0) < 0.1
            assert result['peak_index'] < len(result['rainfall_mm'])


class TestHyetographGenericFunction:
    """Tests para función genérica generate_hyetograph"""

    def test_invalid_method(self):
        """Test con método inválido"""
        with pytest.raises((ValueError, HyetographGenerationError)):
            generate_hyetograph(
                total_rainfall_mm=100.0,
                duration_hours=2.0,
                method='invalid_method',
                time_step_minutes=10.0
            )

    def test_invalid_rainfall(self):
        """Test con lluvia negativa"""
        with pytest.raises((ValueError, HyetographGenerationError)):
            generate_hyetograph(
                total_rainfall_mm=-50.0,
                duration_hours=2.0,
                method='uniform',
                time_step_minutes=10.0
            )

    def test_invalid_duration(self):
        """Test con duración inválida"""
        with pytest.raises((ValueError, HyetographGenerationError)):
            generate_hyetograph(
                total_rainfall_mm=100.0,
                duration_hours=-1.0,
                method='uniform',
                time_step_minutes=10.0
            )

    def test_invalid_timestep(self):
        """Test con paso de tiempo inválido"""
        with pytest.raises((ValueError, HyetographGenerationError)):
            generate_hyetograph(
                total_rainfall_mm=100.0,
                duration_hours=2.0,
                method='uniform',
                time_step_minutes=0  # Inválido
            )

    def test_default_peak_position(self):
        """Test que default peak_position_ratio es 0.5"""
        result = generate_hyetograph(
            total_rainfall_mm=100.0,
            duration_hours=2.0,
            method='alternating_block',
            time_step_minutes=10.0,
            P3_10=70.0,
            Tr=10.0
            # peak_position_ratio no especificado
        )

        assert result['peak_position_ratio'] == 0.5


class TestHyetographTimeConsistency:
    """Tests de consistencia temporal"""

    def test_time_steps_increasing(self):
        """Test que los pasos de tiempo son crecientes"""
        result = generate_hyetograph(
            total_rainfall_mm=100.0,
            duration_hours=2.0,
            method='uniform',
            time_step_minutes=10.0
        )

        time_steps = result['time_steps']
        for i in range(len(time_steps) - 1):
            assert time_steps[i] < time_steps[i + 1]

    def test_total_duration_match(self):
        """Test que la duración total coincide"""
        result = generate_hyetograph(
            total_rainfall_mm=100.0,
            duration_hours=3.0,
            method='uniform',
            time_step_minutes=15.0
        )

        # Último tiempo debe ser aproximadamente = duración * 60 minutos
        expected_duration_minutes = 3.0 * 60
        actual_last_time = result['time_steps'][-1]

        # Permitir algo de tolerancia por redondeo
        assert abs(actual_last_time - expected_duration_minutes) < 20

    def test_number_of_intervals(self):
        """Test que el número de intervalos es correcto"""
        duration_hours = 2.0
        time_step = 10.0

        result = generate_hyetograph(
            total_rainfall_mm=100.0,
            duration_hours=duration_hours,
            method='uniform',
            time_step_minutes=time_step
        )

        expected_intervals = int((duration_hours * 60) / time_step)
        actual_intervals = len(result['rainfall_mm'])

        # Permitir 1 intervalo de diferencia por redondeo
        assert abs(actual_intervals - expected_intervals) <= 1


class TestRealWorldScenarios:
    """Tests con escenarios realistas"""

    def test_urban_storm_1h(self):
        """Test tormenta urbana típica de 1 hora"""
        result = generate_hyetograph(
            total_rainfall_mm=50.0,
            duration_hours=1.0,
            method='alternating_block',
            time_step_minutes=5.0,
            peak_position_ratio=0.4,  # Pico temprano (típico)
            P3_10=70.0,
            Tr=10.0
        )

        assert result['total_rainfall_mm'] == 50.0
        assert result['duration_hours'] == 1.0
        assert result['peak_position_ratio'] == 0.4
        assert abs(sum(result['rainfall_mm']) - 50.0) < 0.1

    def test_design_storm_24h(self):
        """Test tormenta de diseño de 24 horas"""
        result = generate_hyetograph(
            total_rainfall_mm=127.0,  # Típico para Tr=10, Uruguay
            duration_hours=24.0,
            method='alternating_block',
            time_step_minutes=30.0,
            peak_position_ratio=0.5,
            P3_10=70.0,
            Tr=10.0
        )

        assert result['total_rainfall_mm'] == 127.0
        assert result['duration_hours'] == 24.0
        assert abs(sum(result['rainfall_mm']) - 127.0) < 0.2

    def test_small_rain_event(self):
        """Test evento de lluvia pequeña"""
        result = generate_hyetograph(
            total_rainfall_mm=5.0,
            duration_hours=0.5,
            method='uniform',
            time_step_minutes=5.0
        )

        assert result['total_rainfall_mm'] == 5.0
        assert abs(sum(result['rainfall_mm']) - 5.0) < 0.01
