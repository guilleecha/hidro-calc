"""
Django Rest Framework Serializers para HidroCalc
Equivalente a Pydantic schemas en FastAPI
"""

from rest_framework import serializers
from core.models import Project, Watershed, DesignStorm, Hydrograph, RainfallData


# ============================================================================
# PROJECT SERIALIZERS
# ============================================================================

class ProjectSerializer(serializers.ModelSerializer):
    """Serializer básico para proyectos"""
    total_watersheds = serializers.ReadOnlyField()

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'location', 'country', 'region',
            'timezone', 'owner', 'is_active', 'created_at', 'updated_at',
            'total_watersheds'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'total_watersheds']


class ProjectCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear proyectos"""

    class Meta:
        model = Project
        fields = [
            'name', 'description', 'location', 'country', 'region', 'timezone'
        ]

    def validate_name(self, value):
        """Validar que el nombre no esté vacío"""
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío")
        return value


class ProjectDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado con cuencas incluidas"""
    watersheds = serializers.SerializerMethodField()
    total_watersheds = serializers.ReadOnlyField()

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'location', 'country', 'region',
            'timezone', 'owner', 'is_active', 'created_at', 'updated_at',
            'total_watersheds', 'watersheds'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_watersheds(self, obj):
        """Obtener cuencas del proyecto"""
        watersheds = obj.watersheds.all()
        return WatershedSerializer(watersheds, many=True).data


# ============================================================================
# WATERSHED SERIALIZERS
# ============================================================================

class WatershedSerializer(serializers.ModelSerializer):
    """Serializer básico para cuencas"""
    area_m2 = serializers.ReadOnlyField()
    tc_minutes = serializers.ReadOnlyField()

    class Meta:
        model = Watershed
        fields = [
            'id', 'project', 'name', 'description', 'area_hectareas', 'tc_horas',
            'nc_scs', 'latitude', 'longitude', 'elevation_m', 'c_racional',
            'extra_metadata', 'created_at', 'updated_at', 'area_m2', 'tc_minutes'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'area_m2', 'tc_minutes']

    def validate_area_hectareas(self, value):
        """Validar área positiva"""
        if value <= 0:
            raise serializers.ValidationError("El área debe ser mayor a 0")
        return value

    def validate_tc_horas(self, value):
        """Validar Tc positivo"""
        if value <= 0:
            raise serializers.ValidationError("El tiempo de concentración debe ser mayor a 0")
        return value

    def validate_nc_scs(self, value):
        """Validar NC entre 30 y 100"""
        if value is not None and (value < 30 or value > 100):
            raise serializers.ValidationError("El número de curva debe estar entre 30 y 100")
        return value

    def validate_c_racional(self, value):
        """Validar C entre 0 y 1"""
        if value is not None and (value < 0 or value > 1):
            raise serializers.ValidationError("El coeficiente de escorrentía debe estar entre 0 y 1")
        return value


class WatershedCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear cuencas"""

    class Meta:
        model = Watershed
        fields = [
            'project', 'name', 'description', 'area_hectareas', 'tc_horas',
            'nc_scs', 'latitude', 'longitude', 'elevation_m', 'c_racional',
            'extra_metadata'
        ]

    def validate_area_hectareas(self, value):
        if value <= 0:
            raise serializers.ValidationError("El área debe ser mayor a 0")
        return value

    def validate_tc_horas(self, value):
        if value <= 0:
            raise serializers.ValidationError("El tiempo de concentración debe ser mayor a 0")
        return value


class WatershedDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado con tormentas incluidas"""
    design_storms = serializers.SerializerMethodField()
    area_m2 = serializers.ReadOnlyField()
    tc_minutes = serializers.ReadOnlyField()

    class Meta:
        model = Watershed
        fields = [
            'id', 'project', 'name', 'description', 'area_hectareas', 'tc_horas',
            'nc_scs', 'latitude', 'longitude', 'elevation_m', 'c_racional',
            'extra_metadata', 'created_at', 'updated_at', 'area_m2', 'tc_minutes',
            'design_storms'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_design_storms(self, obj):
        """Obtener tormentas de diseño de la cuenca"""
        storms = obj.design_storms.all()
        return DesignStormSerializer(storms, many=True).data


# ============================================================================
# DESIGN STORM SERIALIZERS
# ============================================================================

class DesignStormSerializer(serializers.ModelSerializer):
    """Serializer básico para tormentas de diseño"""
    duration_minutes = serializers.ReadOnlyField()
    average_intensity_mm_h = serializers.ReadOnlyField()

    class Meta:
        model = DesignStorm
        fields = [
            'id', 'watershed', 'name', 'description', 'return_period_years',
            'duration_hours', 'total_rainfall_mm', 'distribution_type',
            'initial_abstraction_mm', 'storage_parameter_mm', 'time_step_minutes',
            'extra_metadata', 'created_at', 'updated_at', 'duration_minutes',
            'average_intensity_mm_h'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'duration_minutes', 'average_intensity_mm_h']

    def validate_return_period_years(self, value):
        """Validar Tr positivo"""
        if value <= 0:
            raise serializers.ValidationError("El período de retorno debe ser mayor a 0")
        return value

    def validate_duration_hours(self, value):
        """Validar duración positiva"""
        if value <= 0:
            raise serializers.ValidationError("La duración debe ser mayor a 0")
        return value

    def validate_total_rainfall_mm(self, value):
        """Validar lluvia positiva"""
        if value <= 0:
            raise serializers.ValidationError("La lluvia total debe ser mayor a 0")
        return value


class DesignStormCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear tormentas de diseño"""

    class Meta:
        model = DesignStorm
        fields = [
            'watershed', 'name', 'description', 'return_period_years',
            'duration_hours', 'total_rainfall_mm', 'distribution_type',
            'initial_abstraction_mm', 'storage_parameter_mm', 'time_step_minutes',
            'extra_metadata'
        ]

    def validate_return_period_years(self, value):
        if value <= 0:
            raise serializers.ValidationError("El período de retorno debe ser mayor a 0")
        return value

    def validate_duration_hours(self, value):
        if value <= 0:
            raise serializers.ValidationError("La duración debe ser mayor a 0")
        return value


class DesignStormDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado con hidrogramas incluidos"""
    hydrographs = serializers.SerializerMethodField()
    duration_minutes = serializers.ReadOnlyField()
    average_intensity_mm_h = serializers.ReadOnlyField()

    class Meta:
        model = DesignStorm
        fields = [
            'id', 'watershed', 'name', 'description', 'return_period_years',
            'duration_hours', 'total_rainfall_mm', 'distribution_type',
            'initial_abstraction_mm', 'storage_parameter_mm', 'time_step_minutes',
            'extra_metadata', 'created_at', 'updated_at', 'duration_minutes',
            'average_intensity_mm_h', 'hydrographs'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_hydrographs(self, obj):
        """Obtener hidrogramas de la tormenta"""
        hydrographs = obj.hydrographs.all()
        return HydrographSummarySerializer(hydrographs, many=True).data


# ============================================================================
# HYDROGRAPH SERIALIZERS
# ============================================================================

class HydrographSerializer(serializers.ModelSerializer):
    """Serializer completo para hidrogramas"""
    peak_discharge_lps_calculated = serializers.ReadOnlyField()
    time_to_peak_hours = serializers.ReadOnlyField()

    class Meta:
        model = Hydrograph
        fields = [
            'id', 'design_storm', 'name', 'method', 'peak_discharge_m3s',
            'peak_discharge_lps', 'time_to_peak_minutes', 'total_runoff_mm',
            'total_runoff_m3', 'volume_hm3', 'hydrograph_data',
            'rainfall_excess_mm', 'infiltration_total_mm', 'notes',
            'created_at', 'updated_at', 'peak_discharge_lps_calculated',
            'time_to_peak_hours'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'peak_discharge_lps_calculated', 'time_to_peak_hours']

    def validate_peak_discharge_m3s(self, value):
        """Validar caudal pico positivo"""
        if value <= 0:
            raise serializers.ValidationError("El caudal pico debe ser mayor a 0")
        return value

    def validate_hydrograph_data(self, value):
        """Validar formato de hydrograph_data"""
        if not isinstance(value, list):
            raise serializers.ValidationError("hydrograph_data debe ser una lista")

        for point in value:
            if not isinstance(point, dict):
                raise serializers.ValidationError("Cada punto debe ser un diccionario")

            required_keys = ['time_min', 'discharge_m3s', 'cumulative_volume_m3']
            missing_keys = [key for key in required_keys if key not in point]
            if missing_keys:
                raise serializers.ValidationError(f"Faltan claves: {missing_keys}")

        return value


class HydrographCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear hidrogramas"""

    class Meta:
        model = Hydrograph
        fields = [
            'design_storm', 'name', 'method', 'peak_discharge_m3s',
            'peak_discharge_lps', 'time_to_peak_minutes', 'total_runoff_mm',
            'total_runoff_m3', 'volume_hm3', 'hydrograph_data',
            'rainfall_excess_mm', 'infiltration_total_mm', 'notes'
        ]

    def validate_peak_discharge_m3s(self, value):
        if value <= 0:
            raise serializers.ValidationError("El caudal pico debe ser mayor a 0")
        return value


class HydrographSummarySerializer(serializers.ModelSerializer):
    """Serializer resumido para listas"""

    class Meta:
        model = Hydrograph
        fields = [
            'id', 'name', 'method', 'peak_discharge_m3s', 'peak_discharge_lps',
            'total_runoff_m3', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


# ============================================================================
# RAINFALL DATA SERIALIZERS
# ============================================================================

class RainfallDataSerializer(serializers.ModelSerializer):
    """Serializer para datos de lluvia"""

    class Meta:
        model = RainfallData
        fields = [
            'id', 'watershed', 'event_date', 'return_period_years',
            'duration_hours', 'total_rainfall_mm', 'rainfall_series',
            'source', 'notes', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def validate_total_rainfall_mm(self, value):
        """Validar lluvia positiva"""
        if value <= 0:
            raise serializers.ValidationError("La lluvia total debe ser mayor a 0")
        return value

    def validate_rainfall_series(self, value):
        """Validar formato de rainfall_series"""
        if not isinstance(value, list):
            raise serializers.ValidationError("rainfall_series debe ser una lista")

        for point in value:
            if not isinstance(point, dict):
                raise serializers.ValidationError("Cada punto debe ser un diccionario")

            required_keys = ['time_min', 'intensity_mm_h', 'cumulative_mm']
            missing_keys = [key for key in required_keys if key not in point]
            if missing_keys:
                raise serializers.ValidationError(f"Faltan claves: {missing_keys}")

        return value


class RainfallDataCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear datos de lluvia"""

    class Meta:
        model = RainfallData
        fields = [
            'watershed', 'event_date', 'return_period_years', 'duration_hours',
            'total_rainfall_mm', 'rainfall_series', 'source', 'notes'
        ]

    def validate_total_rainfall_mm(self, value):
        if value <= 0:
            raise serializers.ValidationError("La lluvia total debe ser mayor a 0")
        return value
